@echo off
REM ZELEX Development Environment Launcher (Windows)
REM Usage:
REM   start-dev.bat              - Start dev server
REM   start-dev.bat caddy        - Start Caddy server
REM   start-dev.bat rebuild      - Force rebuild
REM   start-dev.bat shell        - Interactive shell
REM

setlocal enabledelayedexpansion
cd /d "%~dp0"

set DOCKER_COMPOSE=docker-compose
set ACTION=%1
if "%ACTION%"=="" set ACTION=start

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Docker not found. Install Docker Desktop:
    echo https://www.docker.com/products/docker-desktop
    echo.
    exit /b 1
)

if "%ACTION%"=="caddy" (
    echo [*] Starting ZELEX dev server (Caddy)...
    %DOCKER_COMPOSE% -f docker-compose.yml --profile caddy up -d zelex caddy
    echo [+] Caddy running at http://localhost:2015
    echo [*] Stop: docker-compose down
    exit /b 0
)

if "%ACTION%"=="rebuild" (
    echo [*] Rebuilding Docker image...
    %DOCKER_COMPOSE% -f docker-compose.yml build --no-cache
    echo [+] Image rebuilt. Run: start-dev.bat
    exit /b 0
)

if "%ACTION%"=="shell" (
    echo [*] Starting interactive shell...
    %DOCKER_COMPOSE% -f docker-compose.yml run --rm zelex /bin/bash
    exit /b 0
)

if "%ACTION%"=="test" (
    echo [*] Running test suite...
    %DOCKER_COMPOSE% -f docker-compose.yml run --rm zelex bash -c "npm test && python -m pytest --tb=short -q"
    exit /b 0
)

if "%ACTION%"=="build" (
    echo [*] Running build pipeline...
    %DOCKER_COMPOSE% -f docker-compose.yml run --rm zelex python scripts/build_orchestrator.py --full
    exit /b 0
)

if "%ACTION%"=="stop" (
    echo [*] Stopping ZELEX containers...
    %DOCKER_COMPOSE% -f docker-compose.yml down
    exit /b 0
)

REM Default: start dev server
echo [*] Starting ZELEX dev server (Python, port 9000)...
echo [*] Open in browser: http://localhost:9000
%DOCKER_COMPOSE% -f docker-compose.yml up zelex
