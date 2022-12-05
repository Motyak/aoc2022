#!/usr/bin/env bash

set -o nounset

function log {
    local msg=${1:-} # authorize logging only time, when no msg is passed

    time=$(date +"%H:%M:%S")
    printf "[%s] %s\n" "$time" "$msg"
}

# this function is likely to never change (only the sub functions are required to change -- much like in the template method pattern)
function build_source {
    local src_filename=$1

    # get the build command line from the source file #
    get_build_cmd_script_filename=".get_build_cmd.sh"
    build_cmd="$(./$get_build_cmd_script_filename "$src_filename")"

    # execute the build command #
    log "Executing '''$build_cmd'''"
    eval "$build_cmd" && log "Build successful" || log "Build failed"
    echo # additional empty new line
}

# main #

SRC_FILE=$1

build_source "$SRC_FILE"
