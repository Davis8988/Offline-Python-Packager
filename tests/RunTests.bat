@echo off

:: Tests Offline-Python-Packager.exe
::

:: Defines
set packagerExe=%~dp0..\Offline-Python-Packager.exe
set appName=Offline-Python-Packager
set defaultOfflinePackagesDir=exported_packages
set packagesToExport=cffi, future, tornado
set packagesFile=%~dp0test_packages.txt



title Testing %appName%

echo.
echo Testing %appName%

:: Check
if not exist "%packagerExe%" echo Error - Missing or unreachable "%packagerExe%" && echo Please first compile an exe using pyinstaller && compiling script at: %~dp0..\pyinstaller\Compile_Exe.bat && pause && exit 1
where pip || echo Error - Missing pip from system path && echo Cannot start tests without it && echo please install python first && pause && exit 1

:: Pre
if exist "%~dp0%defaultOfflinePackagesDir%" echo Removing old exported packages dir: "%~dp0%defaultOfflinePackagesDir%" &&  rmdir /q /s "%~dp0%defaultOfflinePackagesDir%"
if exist "%~dp0%defaultOfflinePackagesDir%" rmdir /q /s "%~dp0%defaultOfflinePackagesDir%"  && REM Sometimes you need to run 'rmdir' twice for it to actually work....


:: Test
echo Exporting packages: %packagesToExport%

"%packagerExe%" -ep "%packagesToExport%" -v
if %errorlevel% neq 0 echo Error - Failed to export "%packagesToExport%" by executing && echo "%packagerExe%" -ep "%packagesToExport%" && echo See log above && pause && exit 1

echo Checking index-simple dir exists: 
if not exist "%~dp0%defaultOfflinePackagesDir%\simple" echo Error - Missing index-simple dir: "%~dp0%defaultOfflinePackagesDir%\simple" && echo dir2pi didn't work properly && pause && exit 1


echo Using pip to remove %packagesToExport% packages..
pip uninstall future -y
if %errorlevel% neq 0 echo Error - Failed executing && echo pip uninstall future -y && echo See log above && pause &&  exit 1
pip uninstall cffi -y
if %errorlevel% neq 0 echo Error - Failed executing && echo pip uninstall cffi -y && echo See log above && pause &&  exit 1
pip uninstall tornado -y
if %errorlevel% neq 0 echo Error - Failed executing && echo pip uninstall tornado -y && echo See log above && pause &&  exit 1


echo Making sure packages are removed
pip show future
if %errorlevel% equ 0 echo Error - Failed to remove future package using pip && echo It still exists && pause && exit 1
pip show cffi
if %errorlevel% equ 0 echo Error - Failed to remove cffi package using pip && echo It still exists && pause && exit 1
pip show tornado
if %errorlevel% equ 0 echo Error - Failed to remove tornado package using pip && echo It still exists && pause && exit 1


echo Now trying to re-install it using %appName%
"%packagerExe%" -ip "%packagesToExport%" -v
if %errorlevel% neq 0 echo Error - Failed to import "future" by executing && echo "%packagerExe%" -ip "future" && echo See log above && pause && exit 1


echo Making sure future is imported
pip show future
if %errorlevel% neq 0 echo Error - Failed to import future package using %appName% && echo It doesn't exist && pause && exit 1

echo Finished testing..

echo Cleaning:
if exist "%~dp0%defaultOfflinePackagesDir%" echo Removing exported packages dir: "%~dp0%defaultOfflinePackagesDir%" &&  rmdir /q /s "%~dp0%defaultOfflinePackagesDir%"
if exist "%~dp0%defaultOfflinePackagesDir%" rmdir /q /s "%~dp0%defaultOfflinePackagesDir%"  && REM Sometimes you need to run 'rmdir' twice for it to actually work....


echo.
echo Done
echo.
pause





