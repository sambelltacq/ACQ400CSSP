#!/usr/bin/env bash

UUT=$1

if [ -z "$UUT" ]; then
    echo -e "\n[ACQ400CSSP]"
    read -p "Connect to UUT : " UUT
fi

if [ ${#UUT} -lt 8 ]; then
    echo "Invalid UUT"
    exit 1
fi

ROOT_DIR=$(dirname "$(realpath "$0")")
PHOEBUS_JAR="$ROOT_DIR/product-4.7.3/product-4.7.3.jar" #CHANGE ME

# Attempt to locate a phobus jar if not found
if ! [ -f "$PHOEBUS_JAR" ]; then
    shopt -s nullglob
    PHOEBUS_JAR=($ROOT_DIR/product-*/*.jar)
    if [ ${#PHOEBUS_JAR[@]} -eq 0 ]; then
        echo "Error: Unable to locate phoebus jar"
        exit 1
    fi
    PHOEBUS_JAR="${PHOEBUS_JAR[0]}"
    echo "Found phobus jar ${PHOEBUS_JAR}"
fi

JAVA_EXE="java -Dlog.level=DEBUG"
SETTINGS_BASE="$ROOT_DIR/src/settings_base.ini"
LAUNCHER="$ROOT_DIR/src/acq400_launcher.bob"
RESOURCE="${LAUNCHER}"
WORKSPACE="$ROOT_DIR/workspaces/$UUT"

JAVA_PREFS="-Dphoebus.user=${WORKSPACE} -Dphoebus.folder.name.preference="
SETTINGS="$WORKSPACE/settings.ini"
MEMENTO="$WORKSPACE/memento"

export EPICS_PVA_ADDR_LIST="${UUT}"
export EPICS_CA_ADDR_LIST="${UUT}"

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