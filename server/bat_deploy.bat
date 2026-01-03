@echo off
REM ================================
REM Safe Fly.io redeploy
REM - Does NOT set or modify secrets
REM - Uses existing Fly.io secrets
REM ================================

fly status

echo.
echo Redeploying app using existing Fly secrets...
echo.

fly deploy --local-only

echo.
echo Done.
pause
