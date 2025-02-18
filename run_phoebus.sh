#!/usr/bin/env bash




UUT=$1

if [ -z "$UUT" ]; then
    echo "Usage: $0 <UUT NAME>"
    exit 1
fi

ROOT_DIR=$(dirname "$(realpath "$0")")

JAVA_EXE="java -Dlog.level=DEBUG"
PHOEBUS_JAR="$ROOT_DIR/product-4.7.3/product-4.7.3.jar"
SETTINGS="$ROOT_DIR/src/settings.ini"
PROTOCOL="file://"
LAUNCHER="$ROOT_DIR/src/acq400_launcher.bob"
RESOURCE="${PROTOCOL}${LAUNCHER}?UUT=${UUT}"
WORKSPACE="$ROOT_DIR/workspaces/$UUT"
MEMENTO="$WORKSPACE/memento"

if [ ! -f "$MEMENTO" ]; then
    echo "Creating new workspace $WORKSPACE"
    mkdir -p $WORKSPACE
    TARGET="-resource $RESOURCE -layout null"
else
    echo "Using existing workspace $WORKSPACE"
    TARGET="-layout $MEMENTO"
fi

CMD="$JAVA_EXE -Dphoebus.user=$WORKSPACE -jar $PHOEBUS_JAR -nosplash -settings $SETTINGS $TARGET"
echo "Running cmd: $CMD"

$CMD
