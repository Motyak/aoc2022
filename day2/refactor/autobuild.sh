#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$(realpath -s "$0")")

BUILD_SRC_SCRIPT_FILENAME=".build_src.sh"
MAIN_SRC_FILENAME="c.cpp"

ls *.cpp | entr -pc bash -c "cd $SCRIPT_PATH && ./$BUILD_SRC_SCRIPT_FILENAME $MAIN_SRC_FILENAME"
