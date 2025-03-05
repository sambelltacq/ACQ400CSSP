@echo off
setlocal EnableDelayedExpansion

set "UUT=%1"

if "!UUT!"=="" (
    echo Usage: %0 ^<UUT NAME^>
    exit /b 1
)

set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

set "JAVA_EXE=java -Dlog.level=DEBUG"
set "PHOEBUS_JAR=%ROOT_DIR%\phoebus-4.7.4-SNAPSHOT\product-4.7.4-SNAPSHOT.jar"
set "SETTINGS=%ROOT_DIR%\src\settings.ini"
set "PROTOCOL=file://"
set "LAUNCHER=%ROOT_DIR%\src\acq400_launcher.bob"
set "RESOURCE=%PROTOCOL%%LAUNCHER%?UUT=%UUT%"
set "WORKSPACE=%ROOT_DIR%\workspaces\%UUT%"
set "MEMENTO=%WORKSPACE%\memento"

if not exist "!MEMENTO!" (
    echo Creating new workspace !WORKSPACE!
    mkdir "!WORKSPACE!"
    set "TARGET=-resource !RESOURCE! -layout null"
) else (
    echo Using existing workspace !WORKSPACE!
    set "TARGET=-layout !MEMENTO!"
)

set "CMD=%JAVA_EXE% -Dphoebus.user=%WORKSPACE% -jar "%PHOEBUS_JAR%" -nosplash -settings "%SETTINGS%" %TARGET%"
echo Running cmd: %CMD%

%CMD%