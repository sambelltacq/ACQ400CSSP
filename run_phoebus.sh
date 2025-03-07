#!/usr/bin/env bash

UUT=$1

if [ -z "$UUT" ]; then
    echo "Usage: $0 <UUT NAME>"
    exit 1
fi

ROOT_DIR=$(dirname "$(realpath "$0")")
PHOEBUS_JAR="$ROOT_DIR/product-4.7.3/product-4.7.3.jar"
PHOEBUS_JAR=($ROOT_DIR/product-?.?.?/*.jar) #find all Jars
PHOEBUS_JAR="${PHOEBUS_JAR[0]}" # Get First Jar

JAVA_EXE="java -Dlog.level=DEBUG"
SETTINGS_BASE="$ROOT_DIR/src/settings_base.ini"
LAUNCHER="$ROOT_DIR/src/acq400_launcher.bob"
RESOURCE="${LAUNCHER}"
WORKSPACE="$ROOT_DIR/workspaces/$UUT"

JAVA_PREFS="-Dphoebus.user=${WORKSPACE} -Dphoebus.folder.name.preference="
SETTINGS="$WORKSPACE/settings.ini"
MEMENTO="$WORKSPACE/memento"

if [ ! -f "$MEMENTO" ]; then
    echo "Creating new workspace $WORKSPACE"
    mkdir -p $WORKSPACE
    cp $SETTINGS_BASE $SETTINGS
    echo "org.csstudio.display.builder.model/macros=<UUT>${UUT}</UUT>" >> $SETTINGS
    TARGET="-resource $RESOURCE -layout null"
else
    echo "Using existing workspace $WORKSPACE"
    TARGET="-layout $MEMENTO"
fi

CMD="$JAVA_EXE $JAVA_PREFS -jar $PHOEBUS_JAR -nosplash -settings $SETTINGS $TARGET"
echo "Running cmd: $CMD"
$CMD &> /dev/null
echo "Done"