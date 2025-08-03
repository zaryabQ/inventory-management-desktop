@echo off
echo Building Inventory Management System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import flet, PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
)

REM Build the application
echo.
echo Starting build process...
python build.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
) else (
    echo.
    echo Build completed successfully!
    echo The executable is located in the 'dist' folder.
    echo.
    pause
) 