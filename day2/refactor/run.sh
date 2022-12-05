#!/usr/bin/env bash

set -o nounset

function log {
    local msg=${1:-} # authorize logging only time, when no msg is passed

    time=$(date +"%H:%M:%S")
    printf "[%s] %s\n" "$time" "$msg"
}

function print_separator {
    local separator_char=${1:-"="}

    term_width=$(stty -a | grep -Po '(?<=columns )\d+')
    printf "$separator_char%.0s" $(seq "$term_width")
}

function run {
    local src_filenames=$1
    local output_filename=$2
    local build_cmd=$3
    
    # execute build command if output file is too old #
    should_rebuild=false
    for src_filename in $src_filenames; do
        [ "$output_filename" -ot "$src_filename" ] && should_rebuild=true
    done

    [ "$should_rebuild" == true ] && {
        log "Compiling src.."
        eval "$build_cmd"
        log "Done"
    }

    # run output program #
    ./"$output_filename"
}

# main #
SRC_FILENAME="c.cpp"
OUTPUT_FILENAME="a.out"

# get the build command line from the source file #
GET_BUILD_CMD_SCRIPT_FILENAME=".get_build_cmd.sh"
BUILD_CMD="$(./$GET_BUILD_CMD_SCRIPT_FILENAME "$SRC_FILENAME")"

# loop behavior, pass any arg to script to trigger it #
[ $# -eq 0 ] || {
    while true; do
        run "*.cpp" $OUTPUT_FILENAME "$BUILD_CMD"
        read
        print_separator
    done
}

# run once behavior #
run "*.cpp" $OUTPUT_FILENAME "$BUILD_CMD"
