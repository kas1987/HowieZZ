#!/bin/bash
#
# ZELEX Development Environment Launcher
# Fast-track: ~5 min setup, ~1 hour complete onboarding
#
# Usage:
#   ./start-dev.sh              # Start dev server (Python + tests)
#   ./start-dev.sh caddy        # Start Caddy server instead
#   ./start-dev.sh rebuild      # Force rebuild Docker image
#   ./start-dev.sh shell        # Drop into container shell
#

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
DOCKER_IMAGE="zelex-dev"
CONTAINER_NAME="zelex-dev"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}→${NC} $1"
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Docker availability
if ! command -v docker &> /dev/null; then
    warn "Docker not found. Install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Handle subcommands
case "${1:-start}" in
    caddy)
        log "Starting ZELEX dev server (Caddy)"
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" --profile caddy up -d zelex caddy
        info "Caddy running at http://localhost:2015"
        info "Stop: docker-compose down"
        ;;
    rebuild)
        log "Rebuilding Docker image..."
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" build --no-cache
        log "Image rebuilt. Run: ./start-dev.sh"
        ;;
    shell)
        log "Dropping into container shell..."
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" run --rm zelex /bin/bash
        ;;
    test)
        log "Running test suite..."
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" run --rm zelex bash -c "npm test && python -m pytest --tb=short -q"
        ;;
    build)
        log "Running build pipeline..."
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" run --rm zelex python scripts/build_orchestrator.py --full
        ;;
    stop)
        log "Stopping ZELEX containers..."
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" down
        ;;
    *)
        log "Starting ZELEX dev server (Python, port 9000)"

        # Clean up if container already exists
        if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            warn "Existing container found. Removing..."
            docker-compose -f "$PROJECT_ROOT/docker-compose.yml" down
        fi

        # Start the dev server
        docker-compose -f "$PROJECT_ROOT/docker-compose.yml" up zelex
        ;;
esac
