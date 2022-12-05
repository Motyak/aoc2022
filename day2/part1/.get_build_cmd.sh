#!/usr/bin/env bash

set -o nounset

function read_source_file {
    local source_file=$1

    cat "$source_file"
}

function parse_build_line {
    grep "g++"
}

# we suppose redirected output as input is a commented build command (with a space between the '//' and the command)
function parse_build_cmd {
    cut -f 2- -d ' '
}

function get_build_cmd {
    read_source_file "$SRC_FILENAME" |
    parse_build_line |
    parse_build_cmd
}

# main #

SRC_FILENAME=$1

get_build_cmd "$SRC_FILENAME"
