#!/usr/bin/env bash
# run.sh - run a script
#
# Description:
#   This script provides a simple way to run other scripts in the same directory
#   by just providing the name of the script (without .sh) as an argument.
#   It also checks if the script exists and prints a helpful message if it
#   doesn't, along with a list of available scripts.
#
# Dependencies:
#   {basename, dirname, realpath} (coreutils)
#
# Usage:
#   ./run.sh {name} [option]
#
# Example:
#   ./run.sh bump-version [options]
#
# Author: Kai Elsässer <kai.elsaesser@posteo.de>
# Version: 0.1.0

SCRIPT="$(realpath "${0}")"
DIR="$(dirname "$SCRIPT")"

[[ -z "$@" ]] && {
    printf "error: no command provided\n"
    exit 1
}

cmd="$1"
shift

available=()
for n in $DIR/*; do
    script="$(basename "$n")"
    [[ "$script" =~ ^_ || ! "$script" =~ \.sh$ || "$script" =~ ^run\.sh$ ]] && {
        continue
    }

    name="${script%.*}"
    if [[ "$name" = "$cmd" ]]; then
        target="$n"
        break
    fi
    available+=("'$name' => $script")
done

[[ ! -v target || -z $target ]] && {
    printf "script not found: '%s' (%s)\n" $cmd "$cmd.sh"
    printf "available scripts:\n"
    printf " *%s\n" "${available[@]}"
    exit 1
}

sh $target "$@"
