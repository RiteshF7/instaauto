@echo off
echo ============================================================
echo   Starting InstaAuto Server...
echo ============================================================
echo.
echo Server will be available at:
echo   http://localhost:8000
echo   http://127.0.0.1:8000
echo.
echo Opening browser in 3 seconds...
echo.
timeout /t 3 /nobreak >nul
start http://localhost:8000
echo.
cd /d "%~dp0\.."
python scripts\start_server.py
pause


