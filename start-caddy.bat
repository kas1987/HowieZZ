@echo off
setlocal

:: ─── Self-elevate if not admin ───────────────────────────────────────────────
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: ─── Ensure working directory is the repo root (elevation resets cwd) ────────
cd /d "%~dp0"

set "HOSTS=C:\Windows\System32\drivers\etc\hosts"
set "ENTRY=127.0.0.1  howiez.local"
set "CADDYFILE=%~dp0Caddyfile"

:: ─── Add hosts entry if missing ──────────────────────────────────────────────
findstr /c:"howiez.local" "%HOSTS%" >nul 2>&1
if %errorlevel% neq 0 (
    echo Adding howiez.local to hosts file...
    echo.>> "%HOSTS%"
    echo %ENTRY%>> "%HOSTS%"
    echo Done.
) else (
    echo howiez.local already in hosts — skipping.
)

:: ─── Trust Caddy local CA (once) ─────────────────────────────────────────────
echo Trusting Caddy local CA...
caddy trust
if %errorlevel% neq 0 (
    echo WARNING: caddy trust failed — HTTPS may show a cert warning.
)

:: ─── Start Caddy ─────────────────────────────────────────────────────────────
echo.
echo Starting Caddy...
echo Site will be available at https://howiez.local
echo Press Ctrl+C to stop.
echo.
caddy run --config "%CADDYFILE%"

endlocal
