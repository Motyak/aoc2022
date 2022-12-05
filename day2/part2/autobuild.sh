#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$(realpath -s "$0")")

BUILD_SRC_SCRIPT_FILENAME=".build_src.sh"
SRC_FILENAME="c.cpp"

echo "$SRC_FILENAME" | entr -pc bash -c "cd $SCRIPT_PATH && ./$BUILD_SRC_SCRIPT_FILENAME $SRC_FILENAME"
