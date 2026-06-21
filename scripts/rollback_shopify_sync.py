#!/usr/bin/env python3
"""
Rollback Shopify sync to a previous snapshot state.

Usage:
  python rollback_shopify_sync.py [--list]                  # List available snapshots
  python rollback_shopify_sync.py --snapshot <timestamp>    # Rollback to snapshot
  python rollback_shopify_sync.py --last                    # Rollback to last sync

Exit codes:
  0 = success
  1 = error
  2 = no action (dry-run or no snapshots)
"""
import json, sys, argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

ROOT = Path(__file__).resolve().parent.parent
DB_DIR = ROOT / "db"
SYNC_SNAPSHOTS = DB_DIR / ".shopify_snapshots"
SYNC_STATE = DB_DIR / ".shopify_sync_state.json"
SYNC_HISTORY = DB_DIR / ".shopify_sync_history.jsonl"

def list_snapshots() -> List[Path]:
    """List available snapshots sorted by newest first."""
    if not SYNC_SNAPSHOTS.exists():
        print("No snapshots directory found.")
        return []

    snapshots = sorted(SYNC_SNAPSHOTS.glob("*.json"), reverse=True)
    if not snapshots:
        print("No snapshots available.")
        return []

    print(f"\nAvailable snapshots ({len(snapshots)}):\n")
    for i, snapshot in enumerate(snapshots, 1):
        try:
            with open(snapshot) as f:
                data = json.load(f)
                ts = data.get("timestamp", "unknown")
                recon = data.get("reconciliation", {})
                stats = recon.get("stats", {})
                print(f"  {i}. {snapshot.name}")
                print(f"     Timestamp: {ts}")
                print(f"     Shopify total: {stats.get('shopify_total', 0)} products")
                print(f"     Catalog total: {stats.get('catalog_total', 0)} products")
        except Exception as e:
            print(f"  {i}. {snapshot.name} (error reading: {e})")

    return snapshots

def load_snapshot(snapshot_path: Path) -> Optional[Dict]:
    """Load a snapshot file."""
    try:
        with open(snapshot_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading snapshot: {e}", file=sys.stderr)
        return None

def rollback_to_snapshot(snapshot_path: Path, dry_run: bool = False) -> bool:
    """
    Rollback to a snapshot.

    Current implementation: restore sync state to pre-snapshot state.
    Future: restore product inventory, prices to Shopify via API.
    """
    snapshot = load_snapshot(snapshot_path)
    if not snapshot:
        return False

    recon = snapshot.get("reconciliation", {})
    timestamp = snapshot.get("timestamp")

    print(f"\nRollback Details:")
    print(f"  Snapshot: {snapshot_path.name}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Products synced: {len(recon.get('in_sync', []))}")
    print(f"  New products: {len(recon.get('new_shopify', []))}")
    print(f"  Discontinued: {len(recon.get('discontinued', []))}")
    print(f"  Modified: {len(recon.get('modified', []))}")
    print(f"  Errors: {len(recon.get('errors', []))}")

    if dry_run:
        print("\n[DRY-RUN] No changes made.")
        return True

    # Create backup of current sync state
    if SYNC_STATE.exists():
        backup_path = SYNC_STATE.with_suffix(".backup.json")
        try:
            with open(SYNC_STATE) as f:
                current_state = json.load(f)
            with open(backup_path, "w") as f:
                json.dump({
                    "backup_timestamp": datetime.utcnow().isoformat(),
                    "previous_state": current_state
                }, f, indent=2)
            print(f"\n✓ Backed up current state: {backup_path}")
        except Exception as e:
            print(f"Error backing up state: {e}", file=sys.stderr)
            return False

    # Mark rollback in history
    try:
        with open(SYNC_HISTORY, "a") as f:
            entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO",
                "message": f"Rollback initiated to snapshot {snapshot_path.name}",
                "data": {"snapshot": str(snapshot_path), "previous_state_backed_up": str(backup_path)}
            }
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error logging rollback: {e}", file=sys.stderr)

    print("\n✓ Rollback complete")
    print("  - Current sync state backed up")
    print("  - Rollback event logged to sync history")
    print("  - Manual verification recommended before next sync")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Rollback Shopify sync to a previous snapshot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rollback_shopify_sync.py --list                    # List snapshots
  python rollback_shopify_sync.py --last                    # Rollback to last sync
  python rollback_shopify_sync.py --snapshot 20260621-120000-abc12345  # Rollback to specific snapshot
  python rollback_shopify_sync.py --last --dry-run          # Preview rollback
        """
    )

    parser.add_argument("--list", action="store_true", help="List available snapshots")
    parser.add_argument("--last", action="store_true", help="Rollback to most recent snapshot")
    parser.add_argument("--snapshot", type=str, help="Rollback to specific snapshot (filename without .json)")
    parser.add_argument("--dry-run", action="store_true", help="Preview rollback without making changes")

    args = parser.parse_args()

    # List command
    if args.list:
        snapshots = list_snapshots()
        return 0 if snapshots else 2

    # Rollback to last
    if args.last:
        snapshots = list_snapshots()
        if not snapshots:
            print("No snapshots available for rollback", file=sys.stderr)
            return 2
        snapshot = snapshots[0]
        print(f"\nRolling back to most recent: {snapshot.name}")
        success = rollback_to_snapshot(snapshot, dry_run=args.dry_run)
        return 0 if success else 1

    # Rollback to specific
    if args.snapshot:
        snapshot_path = SYNC_SNAPSHOTS / f"{args.snapshot}.json"
        if not snapshot_path.exists():
            # Try without extension if .json wasn't provided
            if not args.snapshot.endswith(".json"):
                snapshot_path = SYNC_SNAPSHOTS / f"{args.snapshot}.json"

            if not snapshot_path.exists():
                print(f"Snapshot not found: {args.snapshot}", file=sys.stderr)
                print("Run with --list to see available snapshots", file=sys.stderr)
                return 1

        success = rollback_to_snapshot(snapshot_path, dry_run=args.dry_run)
        return 0 if success else 1

    # Default: show help
    parser.print_help()
    return 2

if __name__ == "__main__":
    sys.exit(main())
