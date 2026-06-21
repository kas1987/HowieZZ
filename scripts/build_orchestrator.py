#!/usr/bin/env python3
"""
ZELEX Build Orchestrator
Parallel pipeline executor with idempotence, resume, and retry logic.

Usage:
    python scripts/build_orchestrator.py              # Run full pipeline
    python scripts/build_orchestrator.py --resume     # Resume from last failure
    python scripts/build_orchestrator.py --stages stage1,stage2,...  # Run specific stages
    python scripts/build_orchestrator.py --reset      # Full rebuild (drop DB, start fresh)
    python scripts/build_orchestrator.py --dry-run    # Show what would run
    python scripts/build_orchestrator.py --json       # Output JSON status (for CI/CD)

Exit codes:
    0 = success
    1 = fatal error (unrecoverable)
    2 = skipped (no work or already complete)
    3 = partial failure (some stages failed but build continued)
"""

import sys
import json
import time
import subprocess
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Tuple
import traceback

# ── Configuration ─────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DB_DIR = ROOT / "db"
ASSETS = ROOT / "assets"
STATE_DIR = DB_DIR / ".orchestrator"  # Idempotence + state tracking

STATE_DIR.mkdir(parents=True, exist_ok=True)

# Status cache: tracks which stages have completed, their hashes, output files
STATE_FILE = STATE_DIR / "state.json"
STATE_LOCK = STATE_DIR / ".lock"

# Stage registry: (name, script, inputs[], outputs[], parallel_safe, retry_count)
# parallel_safe=True means the stage can run concurrently with others
STAGES = [
    ("db",          "build_db.py",           ["assets/Measure", "assets/I-Series", "assets/K-Series", "assets/Fusion-Series", "assets/SLE-Series"],
                                             ["db/catalog.db", "db/catalog.json", "assets/data"],
                                             True, 3),
    ("profiles",    "build_profiles.py",     ["db/catalog.db", "db/body_measurements.json"],
                                             ["db/body_profiles.json", "docs/character-profiles.md"],
                                             True, 2),
    ("characters",  "build_characters.py",   ["db/catalog.db", "db/body_profiles.json"],
                                             ["db/characters.json", "db/body_types.json"],
                                             True, 2),
    ("merge_stories", "merge_stories.py",   ["db/characters.json"],
                                             ["db/character_stories.json"],
                                             False, 1),  # Must run after characters
    ("thumbs",      "make_thumbs.py",        ["db/body_profiles.json", "db/characters.json", "assets/data"],
                                             ["assets/thumbs"],
                                             False, 1),  # Must run after profiles/characters
    ("pages",       "generate_pages.py",     ["db/pages_config.json", "db/characters.json", "db/family_taxonomy.json"],
                                             ["db/pages_manifest.json"],
                                             True, 1),  # Parallel-safe; runs after catalog finalized
]

# Parallel groups: stages that can run together
# Group ordering is sequential, within each group stages are parallel
PARALLEL_GROUPS = [
    ["db"],                          # Group 0: Initialize DB
    ["profiles", "characters"],      # Group 1: Parallel analysis
    ["merge_stories", "thumbs"],     # Group 2: Post-processing
    ["pages"],                       # Group 3: Page inventory and manifest
]

# ── State tracking ─────────────────────────────────────────────────────────────

@dataclass
class StageState:
    name: str
    status: str  # 'pending', 'running', 'complete', 'failed', 'skipped'
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration_secs: float = 0.0
    error: Optional[str] = None
    input_hash: Optional[str] = None  # Hash of input files
    output_hash: Optional[str] = None  # Hash of output files (if complete)
    retry_count: int = 0
    max_retries: int = 1
    exit_code: Optional[int] = None

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return StageState(**d)

@dataclass
class OrchestrationState:
    timestamp: str
    pipeline_start: Optional[float] = None
    pipeline_end: Optional[float] = None
    total_duration_secs: float = 0.0
    stages: Dict[str, StageState] = field(default_factory=dict)
    reset_requested: bool = False
    resume_mode: bool = False
    exit_code: int = 0
    summary: str = ""

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "pipeline_start": self.pipeline_start,
            "pipeline_end": self.pipeline_end,
            "total_duration_secs": self.total_duration_secs,
            "stages": {k: v.to_dict() for k, v in self.stages.items()},
            "reset_requested": self.reset_requested,
            "resume_mode": self.resume_mode,
            "exit_code": self.exit_code,
            "summary": self.summary,
        }

    @staticmethod
    def from_dict(d):
        state = OrchestrationState(
            timestamp=d["timestamp"],
            pipeline_start=d.get("pipeline_start"),
            pipeline_end=d.get("pipeline_end"),
            total_duration_secs=d.get("total_duration_secs", 0.0),
            reset_requested=d.get("reset_requested", False),
            resume_mode=d.get("resume_mode", False),
            exit_code=d.get("exit_code", 0),
            summary=d.get("summary", ""),
        )
        for name, stage_dict in d.get("stages", {}).items():
            state.stages[name] = StageState.from_dict(stage_dict)
        return state

def load_state() -> OrchestrationState:
    """Load previous orchestration state or create new."""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return OrchestrationState.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"  [warn] Could not parse state file: {e}; starting fresh")
    return OrchestrationState(timestamp=datetime.now().isoformat())

def save_state(state: OrchestrationState):
    """Persist orchestration state."""
    STATE_FILE.write_text(
        json.dumps(state.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def hash_files(paths: List[str]) -> str:
    """Compute hash of a set of files/directories. Used to detect changes."""
    hasher = hashlib.sha256()
    sorted_paths = sorted(paths)
    for path_str in sorted_paths:
        p = Path(path_str)
        if not p.exists():
            hasher.update(b"MISSING:")
            hasher.update(path_str.encode())
            continue
        if p.is_file():
            try:
                hasher.update(p.read_bytes())
            except (OSError, IOError):
                hasher.update(f"ERROR:{path_str}".encode())
        elif p.is_dir():
            # For directories, hash all file paths and mtimes (not contents, for speed)
            for f in sorted(p.rglob("*")):
                if f.is_file():
                    hasher.update(str(f.relative_to(p)).encode())
                    try:
                        hasher.update(str(int(f.stat().st_mtime)).encode())
                    except OSError:
                        pass
    return hasher.hexdigest()[:16]

def inputs_changed(stage_name: str, input_paths: List[str], prev_state: Optional[StageState]) -> bool:
    """Check if input files have changed since last run."""
    if prev_state is None or prev_state.status != "complete":
        return True  # No previous state or incomplete = must run
    current_hash = hash_files(input_paths)
    return current_hash != prev_state.input_hash

# ── Execution ─────────────────────────────────────────────────────────────────

def run_stage(stage_name: str, script: str, inputs: List[str], outputs: List[str],
              max_retries: int, dry_run: bool = False) -> Tuple[int, Optional[str]]:
    """
    Execute a single build stage.
    Returns (exit_code, error_msg or None)
    """
    script_path = SCRIPTS / script
    if not script_path.exists():
        return 1, f"Script not found: {script_path}"

    cmd = [sys.executable, str(script_path)]

    # Pass --reset to db stage if full reset requested
    # (captured via global state, check env or use a flag file)
    if stage_name == "db" and RESET_DB:
        cmd.append("--reset")

    if dry_run:
        print(f"  [dry-run] Would execute: {' '.join(cmd)}")
        return 0, None

    print(f"  [{stage_name}] Running: {script}")
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300  # 5-minute timeout per stage
        )
        duration = time.time() - start
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or f"Exit code {result.returncode}"
            return result.returncode, error_msg
        print(f"  [{stage_name}] OK ({duration:.1f}s)")
        return 0, None
    except subprocess.TimeoutExpired:
        return 1, f"Timeout after 300s"
    except Exception as e:
        return 1, f"{type(e).__name__}: {e}"

def execute_group(group: List[str], stage_map: Dict[str, Tuple], state: OrchestrationState,
                  dry_run: bool = False, max_workers: int = 3) -> bool:
    """
    Execute a group of stages in parallel.
    Returns True if all succeeded, False if any failed.
    """
    futures = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for stage_name in group:
            script, inputs, outputs, _, max_retries = stage_map[stage_name]
            prev_state = state.stages.get(stage_name)

            # Skip if already complete and inputs haven't changed
            if prev_state and prev_state.status == "complete" and not inputs_changed(stage_name, inputs, prev_state):
                print(f"  [{stage_name}] Skipping (up-to-date)")
                state.stages[stage_name].status = "skipped"
                continue

            # Mark as running
            stage_state = StageState(
                name=stage_name,
                status="running",
                start_time=time.time(),
                max_retries=max_retries,
                input_hash=hash_files(inputs)
            )
            state.stages[stage_name] = stage_state

            future = executor.submit(run_stage, stage_name, script, inputs, outputs, max_retries, dry_run)
            futures[future] = (stage_name, script, inputs, outputs, max_retries)

        # Collect results
        failed_stages = []
        for future in as_completed(futures):
            stage_name, script, inputs, outputs, max_retries = futures[future]
            stage_state = state.stages[stage_name]

            try:
                exit_code, error_msg = future.result()
                stage_state.end_time = time.time()
                stage_state.duration_secs = stage_state.end_time - stage_state.start_time
                stage_state.exit_code = exit_code

                if exit_code == 0:
                    stage_state.status = "complete"
                    stage_state.output_hash = hash_files(outputs)
                    print(f"  [{stage_name}] Complete ({stage_state.duration_secs:.1f}s)")
                else:
                    stage_state.status = "failed"
                    stage_state.error = error_msg
                    stage_state.retry_count += 1

                    if stage_state.retry_count < max_retries:
                        print(f"  [{stage_name}] FAILED: {error_msg} (retry {stage_state.retry_count}/{max_retries})")
                        # Retry
                        retry_exit_code, retry_error = run_stage(stage_name, script, inputs, outputs, max_retries, dry_run)
                        if retry_exit_code == 0:
                            stage_state.status = "complete"
                            stage_state.output_hash = hash_files(outputs)
                            print(f"  [{stage_name}] Recovered on retry")
                        else:
                            failed_stages.append((stage_name, retry_error))
                    else:
                        failed_stages.append((stage_name, error_msg))
            except Exception as e:
                stage_state.status = "failed"
                stage_state.error = f"{type(e).__name__}: {e}"
                stage_state.end_time = time.time()
                stage_state.duration_secs = stage_state.end_time - stage_state.start_time
                failed_stages.append((stage_name, stage_state.error))

    # Report failures
    if failed_stages:
        for stage_name, error_msg in failed_stages:
            print(f"  [ERROR] {stage_name}: {error_msg}")
        return False
    return True

def filter_stages(requested: Optional[List[str]]) -> List[List[str]]:
    """Filter PARALLEL_GROUPS to only include requested stages."""
    if requested is None:
        return PARALLEL_GROUPS
    requested_set = set(requested)
    return [
        [s for s in group if s in requested_set]
        for group in PARALLEL_GROUPS
        if any(s in requested_set for s in group)
    ]

# ── Main ──────────────────────────────────────────────────────────────────────

RESET_DB = False
RESUME_MODE = False
REQUESTED_STAGES = None
DRY_RUN = False
OUTPUT_JSON = False

def parse_args():
    global RESET_DB, RESUME_MODE, REQUESTED_STAGES, DRY_RUN, OUTPUT_JSON
    for arg in sys.argv[1:]:
        if arg == "--reset":
            RESET_DB = True
        elif arg == "--resume":
            RESUME_MODE = True
        elif arg == "--dry-run":
            DRY_RUN = True
        elif arg == "--json":
            OUTPUT_JSON = True
        elif arg.startswith("--stages="):
            REQUESTED_STAGES = arg.split("=", 1)[1].split(",")
        elif arg.startswith("--stages"):
            # Next arg is the stages
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                REQUESTED_STAGES = sys.argv[idx + 1].split(",")

def main():
    parse_args()

    # Load or create state
    state = load_state()
    state.timestamp = datetime.now().isoformat()
    state.reset_requested = RESET_DB
    state.resume_mode = RESUME_MODE
    state.pipeline_start = time.time()

    # Build stage map
    stage_map = {name: (script, inputs, outputs, is_parallel, retries)
                 for name, script, inputs, outputs, is_parallel, retries in STAGES}

    # Determine which groups to run
    groups_to_run = filter_stages(REQUESTED_STAGES)

    if not groups_to_run:
        print("No stages to run.")
        state.exit_code = 2
        state.summary = "No stages matched."
        if OUTPUT_JSON:
            print(json.dumps(state.to_dict(), indent=2))
        sys.exit(2)

    print(f"\n{'='*70}")
    print(f"ZELEX Build Orchestrator")
    print(f"Timestamp: {state.timestamp}")
    if RESET_DB:
        print(f"Mode: FULL RESET (database drop + rebuild)")
    elif RESUME_MODE:
        print(f"Mode: RESUME (continue from last failure)")
    else:
        print(f"Mode: INCREMENTAL")
    if DRY_RUN:
        print(f"DRY-RUN MODE (no actual execution)")
    print(f"Groups to execute: {len(groups_to_run)}")
    print(f"{'='*70}\n")

    # Execute groups sequentially (to respect dependencies)
    all_success = True
    for group_idx, group in enumerate(groups_to_run):
        print(f"[Group {group_idx}] Executing {len(group)} stages in parallel: {', '.join(group)}")
        success = execute_group(group, stage_map, state, dry_run=DRY_RUN, max_workers=len(group))
        if not success:
            all_success = False
            if not RESUME_MODE:
                print(f"\n[ERROR] Group {group_idx} failed. Use --resume to retry.")
                break

    # Summarize
    state.pipeline_end = time.time()
    state.total_duration_secs = state.pipeline_end - state.pipeline_start

    complete_count = sum(1 for s in state.stages.values() if s.status == "complete")
    failed_count = sum(1 for s in state.stages.values() if s.status == "failed")
    skipped_count = sum(1 for s in state.stages.values() if s.status == "skipped")

    print(f"\n{'='*70}")
    print(f"Pipeline Summary")
    print(f"  Total stages: {len(state.stages)}")
    print(f"  Complete: {complete_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Duration: {state.total_duration_secs:.1f}s")

    if all_success:
        print(f"Status: SUCCESS")
        state.exit_code = 0
        state.summary = f"All {complete_count} stages completed successfully in {state.total_duration_secs:.1f}s"
    elif failed_count == 0:
        print(f"Status: NO WORK (all stages skipped or pending)")
        state.exit_code = 2
        state.summary = "No work to do"
    else:
        print(f"Status: PARTIAL FAILURE ({failed_count} failed)")
        state.exit_code = 3
        state.summary = f"{complete_count} complete, {failed_count} failed"

    print(f"{'='*70}\n")

    # Save state and output
    save_state(state)

    if OUTPUT_JSON:
        print(json.dumps(state.to_dict(), indent=2))
    else:
        print(f"State saved to: {STATE_FILE}")

    sys.exit(state.exit_code)

if __name__ == "__main__":
    main()
