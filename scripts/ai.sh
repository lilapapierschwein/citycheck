#!/usr/bin/env bash
# ai.sh - start or resume a claude code session
#
# Description:
#   Start or resume a claude code session in the projects root directory.
#
# Dependencies:
#   {basename, dirname, realpath} (coreutils)
#
# Usage:
#   ./ai.sh [option]
#
# Example:
#   ./ai.sh --resume
#
# Author: Kai Elsässer <kai.elsaesser@posteo.de>
# Version: 0.1.0

SCRIPT="$(realpath "${0}")"
NAME="$(basename -s ".sh" "$SCRIPT")"

# get $SCRIPTS_DIR, $PROJECT_ROOT, $PROJECT_NAME, $PROJECT_VERSION
. $(dirname "$SCRIPT")/_project_env.sh

VERSION="0.1.0"
DESCRIPTION="A script to bump the version of the project using uv."

OPTS=$(getopt -o hVrn --long help,version,resume,new -n "$NAME" -- "$@")
if [ $? -ne 0 ]; then
    exit 1
fi
eval set -- "$OPTS"

SESSION_NAME="$PROJECT_NAME"
RESUME=1
while [ : ]; do
    case "${1}" in
    -h | --help)
        printf '%s v.%s\n' $NAME $VERSION
        exit 0
        ;;
    -V | --version)
        printf "error: notimplemented"
        exit 1
        ;;
    -r | --resume)
        RESUME=1
        shift
        ;;
    -n | --new)
        RESUME=0
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        printf 'unknown option: "%s"\n' "${1}"
        exit 1
        ;;
    esac
done

[[ ! -z "$@" ]] && SESSION_NAME="$@"

# cd into project root if not cwd
[[ "$PWD" != "$PROJECT_ROOT" ]] && cd $PROJECT_ROOT

claude --resume "$SESSION_NAME"
