@echo off
REM Build script for Windows
REM ==============================================================================
REM
REM Description:
REM   - This script builds the Matematicke priklady converter application for
REM       Windows using PyInstaller.
REM   - It checks for PyInstaller, installs it if necessary, and then builds the
REM       application.
REM
REM Requirements:
REM   - Python 3.x installed and in PATH.
REM   - PyInstaller must be installed.
REM      - If not, the script will attempt to install it.
REM   - The script should be run from the build_script directory. It will
REM       navigate to the project root directory automatically.
REM
REM Note:
REM   - This script is intended for Windows systems.
REM   - Ensure you have the necessary permissions to run scripts and install
REM       packages.
REM
REM Usage:
REM   build_win.bat
REM
REM Exit codes:
REM   0 - Success
REM   1 - Failure (e.g., PyInstaller not installed, build failed, etc.)
REM
REM ==============================================================================

echo ### Starting build process for Windows...

REM Ensure the script is run from the project root directory
cd /d "%~dp0\.."

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ### PyInstaller is not installed. Try to install it using 'pip install pyinstaller'.
    REM Attempt to install PyInstaller
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ### Failed to install PyInstaller. Please check your Python environment.
        exit /b 1
    ) else (
        echo ### PyInstaller installed successfully. Proceeding with the build...
    )
) else (
    echo ### PyInstaller is installed. Proceeding with the build...
)

REM Run PyInstaller to create the Windows application
REM --noconfirm: Overwrite existing files without confirmation
REM --onedir: Create a directory with the application files
REM --windowed: Suppress the terminal window for GUI applications
REM src/gui.py: The main script to build

pyinstaller --noconfirm --onefile --windowed src/gui.py

REM Check if the build was successful
if %errorlevel% neq 0 (
    echo ### PyInstaller build failed. Please check the output for errors.
    exit /b 1
) else (
    echo ### PyInstaller build completed successfully.
)

exit /b 0
