@echo off
setlocal EnableDelayedExpansion

set UUT=%1

if not defined UUT (
    echo.
    echo [ACQ400CSSP]
    set /p UUT="Connect to UUT : "
)

if "%UUT:~8%"=="" (
    echo "Invalid hostname"
    exit /b 1
)

set "ROOT_DIR=%~dp0"
set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "PHOEBUS_JAR=%ROOT_DIR%\phoebus-4.7.4-SNAPSHOT\product-4.7.4-SNAPSHOT.jar" & :: CHANGE ME

:: Attempt to locate a phobus jar if not found
if exist "%PHOEBUS_JAR%" (
    goto :end
) 
set "PHOEBUS_JAR="
for /r "%ROOT_DIR%" %%F in (*.jar) do (
    set "PHOEBUS_JAR=%%F"
    goto :found
)
echo "Error: Unable to locate Phoebus jar"
exit /b 1
:found
if defined PHOEBUS_JAR (
    echo Found Phoebus jar: "!PHOEBUS_JAR!"
)
:end

set "JAVA_EXE=java"
set "SETTINGS_BASE=%ROOT_DIR%\src\settings_base.ini"
set "LAUNCHER=%ROOT_DIR%\src\acq400_launcher.bob"
set "RESOURCE=%LAUNCHER%"
set "WORKSPACE=%ROOT_DIR%\workspaces\%UUT%"

set "JAVA_PREFS=-Dphoebus.user=%WORKSPACE% -Dphoebus.folder.name.preference="
set "SETTINGS=%WORKSPACE%\settings.ini"
set "MEMENTO=%WORKSPACE%\memento"

set "EPICS_PVA_ADDR_LIST=%UUT%"
set "EPICS_CA_ADDR_LIST=%UUT%"

if not exist "%MEMENTO%" (
    echo Creating new workspace %WORKSPACE%
    mkdir "%WORKSPACE%" 2>nul
    copy "%SETTINGS_BASE%" "%SETTINGS%" >nul
    echo org.csstudio.display.builder.model/macros=^<UUT^>%UUT%^</UUT^> >> "%SETTINGS%"
    set TARGET=-resource "%RESOURCE%" -layout null
) else (
    echo Using existing workspace %WORKSPACE%
    set TARGET=-layout "%MEMENTO%"
)

set CMD=%JAVA_EXE% %JAVA_PREFS% -jar "%PHOEBUS_JAR%" -nosplash -settings "%SETTINGS%" %TARGET%
echo Running cmd: %CMD%
%CMD% >nul 2>&1
echo "Done"