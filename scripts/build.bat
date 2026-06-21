@echo off
REM Quick build wrapper for the parallel orchestrator
REM Usage:
REM   build.bat              REM Full build
REM   build.bat --reset      REM Full rebuild (drop DB)
REM   build.bat --resume     REM Resume from last failure
REM   build.bat profiles,characters  REM Specific stages

setlocal enabledelayedexpansion

cd /d "%~dp0.."

set ARGS=

:parse_args
if "%~1"=="" goto :run
if "%~1"=="--reset" (
    set ARGS=!ARGS! --reset
    shift
    goto :parse_args
)
if "%~1"=="--resume" (
    set ARGS=!ARGS! --resume
    shift
    goto :parse_args
)
if "%~1"=="--dry-run" (
    set ARGS=!ARGS! --dry-run
    shift
    goto :parse_args
)
if "%~1"=="--json" (
    set ARGS=!ARGS! --json
    shift
    goto :parse_args
)
REM Assume it's a stage list
set ARGS=!ARGS! --stages=%~1
shift
goto :parse_args

:run
python scripts/build_orchestrator.py %ARGS%
exit /b %ERRORLEVEL%
