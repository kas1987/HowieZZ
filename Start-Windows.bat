@echo off
REM ============================================================
REM  Zelex Collector's Gallery - Windows launcher
REM
REM  This starts a small local web server (best quality) if
REM  Python is installed. If Python isn't found, it falls back
REM  to simply opening the page directly in your browser.
REM
REM  Just double-click this file.
REM ============================================================

cd /d "%~dp0"

REM Try the 'py' launcher first, then 'python'.
where py >nul 2>nul
if %errorlevel%==0 (
    echo Starting local server with Python...
    py serve.py
    goto :eof
)

where python >nul 2>nul
if %errorlevel%==0 (
    echo Starting local server with Python...
    python serve.py
    goto :eof
)

echo Python was not found - opening the page directly instead.
echo (For best results - looping video etc. - install Python from python.org
echo  and run this file again.)
start "" "index.html"
