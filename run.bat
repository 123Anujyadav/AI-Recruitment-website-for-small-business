@echo off
setlocal
echo Starting TalentAI MVP Server...

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment 'venv' not found.
    echo Please run install.bat first to set up the environment.
    pause
    exit /b 1
)

:: Activate environment and open browser in 3 seconds
echo Server starting... browser will open in 3 seconds.
start "" powershell -Command "Start-Sleep 3; Start-Process 'http://127.0.0.1:8000'"

:: Run server using explicit venv python
echo Launching Django server...
venv\Scripts\python.exe manage.py runserver

:: Keep window open if server stops (likely an error or user closed it)
if %ERRORLEVEL% neq 0 (
    echo [!] Server stopped unexpectedly with error code %ERRORLEVEL%.
    pause
) else (
    echo.
    echo Server has stopped.
    pause
)
