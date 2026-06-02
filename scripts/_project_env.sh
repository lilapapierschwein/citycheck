# _project_env.sh - provide utilites and variables for project scripts
#
# Warning:
#   This script should not be executed directly! It is meant to be sourced by
#   other scripts, providing them a set of env variables and utility functions.
#
# Dependencies:
#   {realpath, dirname} (coreutils)
#
# Author: Kai Elsässer <kai.elsaesser@posteo.de>
# Version: 0.1.0

# check a dependency and print a helpful message if it's missing
#
# Usage:
#  check_dep "command"
#  check_dep "command::package"
check_dep() {
    [[ -z $1 ]] && {
        printf "No command provided to check_dep function.\n"
        exit 1
    }
    if [[ "$1" = *"::"* ]]; then
        local cmd="${1%%::*}"
        local pkg="${1##*::}"
        command -v "$cmd" >/dev/null 2>&1 || {
            printf "Missing required command: '%s' (part of '%s')\n" $cmd $pkg
            printf "Please install '%s' via your package manager and try again.\n" $pkg
            exit 1
        }
    else
        command -v "$1" >/dev/null 2>&1 || {
            printf "Missing required command: '%s'\n" $1
            printf "Please install '%s' via your package manager and try again.\n" $1
            exit 1
        }
    fi
}

check_dep "realpath::coreutils"

_file="$(realpath "${0}")"

# establish paths
SCRIPTS_DIR="$(dirname "$_file")"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
PROJECT_NAME="${PROJECT_ROOT##*/}"

PROJECT_VERSION="$(sed -n "3p" pyproject.toml | awk '{gsub(/"/,"");print$3}')"

# we don't want this variable to interfere elsewhere
unset _file
