@echo off
setlocal enabledelayedexpansion

REM ----- config -----
set "APP=discord-path-api"
set "FLY=C:\Users\xavie\.fly\bin\flyctl.exe"
set "ENVFILE=.env.production"
set "TMP=.fly.env"
set "NOUPDATE=1"
REM -------------------

if not exist "%FLY%" (
  echo [ERROR] flyctl not found: %FLY%
  echo Install/repair Fly CLI or fix the path above.
  exit /b 1
)

REM Stop the updater from nuking the binary
if "%NOUPDATE%"=="1" set FLY_NO_UPDATE_CHECK=1

REM Ensure we are in server\
pushd %~dp0

if not exist "%ENVFILE%" (
  echo [ERROR] %ENVFILE% not found in %CD%
  exit /b 1
)

REM Build a clean secrets file from .env (skip blanks and comments)
> "%TMP%" (
  for /f "usebackq tokens=1,* delims==" %%A in ("%ENVFILE%") do (
    set "k=%%A"
    set "v=%%B"
    if defined k if "!k:~0,1!" NEQ "#" echo !k!=!v!
  )
)

REM Import secrets
"%FLY%" secrets import -a "%APP%" < "%TMP%"
if errorlevel 1 (
  echo [ERROR] secrets import failed
  del "%TMP%" >nul 2>&1
  exit /b 1
)

REM Deploy (fly.toml already points to Dockerfile and process)
"%FLY%" deploy -a "%APP%" --local-only
if errorlevel 1 (
  echo [ERROR] deploy failed
  del "%TMP%" >nul 2>&1
  exit /b 1
)

REM Show status/log hints
"%FLY%" status -a "%APP%"
echo.
echo If something looks off: "%FLY%" logs -a "%APP%"

del "%TMP%" >nul 2>&1
popd
endlocal
