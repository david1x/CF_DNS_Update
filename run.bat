@echo off
REM Set variables
set PYTHON_EXE=C:\Python38\python.exe
set SCRIPT_PATH=D:\Code\Python\CloudFlare_DNS_Update\main.py
set LOG_PATH=D:\Code\Python\CloudFlare_DNS_Update\dns-update.log
set TIMESTAMP=%DATE:/=-%_%TIME::=-%

REM Navigate to the directory containing the Python script
pushd %SCRIPT_PATH%\..

REM Check if Python executable exists
if not exist "%PYTHON_EXE%" (
    echo Error: Python executable not found: %PYTHON_EXE%
    echo Error: Python executable not found: %PYTHON_EXE% >> "%LOG_PATH%"
    exit /b 1
)

REM Check if Python script exists
if not exist "%SCRIPT_PATH%" (
    echo Error: Python script not found: %SCRIPT_PATH%
    echo Error: Python script not found: %SCRIPT_PATH% >> "%LOG_PATH%"
    exit /b 1
)

REM Run the Python script
echo [%TIMESTAMP%] Running script: %SCRIPT_PATH%
echo [%TIMESTAMP%] Running script: %SCRIPT_PATH% >> "%LOG_PATH%"
"%PYTHON_EXE%" "%SCRIPT_PATH%" >> "%LOG_PATH%" 2>&1

REM Check Python script exit code
if %ERRORLEVEL% neq 0 (
    echo Error: Python script failed with exit code %ERRORLEVEL%
    echo Error: Python script failed with exit code %ERRORLEVEL% >> "%LOG_PATH%"
    exit /b %ERRORLEVEL%
)

REM Script execution successful
echo [%TIMESTAMP%] Script execution successful
echo [%TIMESTAMP%] Script execution successful >> "%LOG_PATH%"

popd
exit /b 0
