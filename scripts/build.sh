#!/usr/bin/env bash
# Quick build wrapper for the parallel orchestrator
# Usage:
#   ./scripts/build.sh              # Full build
#   ./scripts/build.sh --reset      # Full rebuild (drop DB)
#   ./scripts/build.sh --resume     # Resume from last failure
#   ./scripts/build.sh profiles,characters  # Specific stages

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$(dirname "$SCRIPT_DIR")"  # Go to project root

# Default: full build
ARGS=""

# Process arguments
for arg in "$@"; do
    case "$arg" in
        --reset)
            ARGS="$ARGS --reset"
            ;;
        --resume)
            ARGS="$ARGS --resume"
            ;;
        --dry-run)
            ARGS="$ARGS --dry-run"
            ;;
        --json)
            ARGS="$ARGS --json"
            ;;
        *)
            # Assume it's a stage list
            ARGS="$ARGS --stages=$arg"
            ;;
    esac
done

python scripts/build_orchestrator.py $ARGS
