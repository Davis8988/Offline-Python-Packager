@echo off

set silent=%~1

rem Vars
set pythonScriptName=Offline-Python-Packager
set iconFile=%~dp0Icons\%pythonScriptName%.ico
set outputDir=%~dp0..
set pythonScriptFilePath=%~dp0..\main.py
set pyinstallerArgs=-i "%iconFile%" --name "%pythonScriptName%" --distpath "%outputDir%" --console --onefile --noconfirm --clean "%pythonScriptFilePath%"
set confFile=%~dp0..\Conf.ini

rem Checks
where pyinstaller || echo Error - Cannot compile your script to an exe without 'pyinstaller.exe' in the path variable of this machine && echo Install it by executing: 'pip install pyinstaller' && pause && exit 1
if not exist "%iconFile%" echo Error - Missing or unreachable: "%iconFile%" && pause && exit 1
if not exist "%pythonScriptFilePath%" echo Error - Missing or unreachable: "%pythonScriptFilePath%" && pause && exit 1

rem Ask before continuing
if not defined silent CHOICE /C YN /M "Do you want to compile %pythonScriptName%.py to an exe?"
if %errorlevel% equ 2 exit 0

REM Compile
echo Compiling..
pyinstaller %pyinstallerArgs%
if %errorlevel% neq 0 echo Error - Failed to compile %pythonScriptName%.py to an exe file && pause && exit 1

REM Clean up
echo Cleaning..
if exist "%~dp0build" rmdir /q /s "%~dp0build"
if exist "%~dp0..\__pycache__" rmdir /q /s "%~dp0..\__pycache__"
if exist "%~dp0%pythonScriptName%.spec" del /q "%~dp0%pythonScriptName%.spec"
if exist "build" rmdir /q /s "build"
if exist "%pythonScriptName%.spec" del /q "%pythonScriptName%.spec"

rem Finish
echo.
echo Finished compiling python exe successfully
echo.

timeout 1