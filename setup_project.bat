@echo off
cls
echo ========================================
echo CD/DVD Issuance System Setup Start
echo ========================================

REM Clone GitHub repo (agar pehle se nahi kiya)
IF NOT EXIST "media_issuance_system" (
    echo Cloning GitHub repository...
    git clone https://github.com/sameermurtaza11/media_issuance_system.git
) ELSE (
    echo Repository already exists.
)

cd media_issuance_system

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Install it first and try again.
    pause
    exit /b
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing Python libraries...
pip install --upgrade pip
pip install -r requirements.txt

REM Run the app
echo Running Flask app...
python app.py

pause
