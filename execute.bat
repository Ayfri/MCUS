@echo off
setlocal enabledelayedexpansion

:: Get username from argument or use saved one
if "%~1" neq "" (
    set "USERNAME=%~1"
    :: Save username to the batch file for next time
    powershell -Command "(Get-Content '%~f0') -replace 'set \"SAVED_USERNAME=.*\"', 'set \"SAVED_USERNAME=%~1\"' | Set-Content '%~f0'"
) else (
    :: Use saved username if no argument provided
    set "SAVED_USERNAME=username"
    set "USERNAME=!SAVED_USERNAME!"
)

IF NOT EXIST .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

python check_minecraft_username.py --username "%USERNAME%"

pause
