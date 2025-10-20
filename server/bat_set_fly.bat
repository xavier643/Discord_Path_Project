@echo off
setlocal
if not exist .env (
  echo .env file not found!
  exit /b 1
)
echo Importing secrets from .env ...
REM This reads .env via stdin so special chars are preserved
type .env | fly secrets import
endlocal
