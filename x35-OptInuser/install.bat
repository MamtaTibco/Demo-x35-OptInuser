@echo off
:: Define the Python version
set PYTHON_VERSION= 3.13.5

:: Display the Python version being used
echo Using Python version %PYTHON_VERSION%

:: Create virtual environment
python -m venv venv

:: Check if venv creation was successful
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate

:: Check if activation was successful
if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

:: Install dependencies


:: Check if dependencies were installed successfully
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)

:: Setup complete
echo Installation complete!
pause



