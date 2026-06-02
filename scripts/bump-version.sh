#!/usr/bin/env bash
#
# bump-version.sh - bump the version of a python3 project project using uv.
#
# Description:
#   This script provides a simple way to automatically bump the version of a
#   uv-managed python project by automating these tasks:
#       *running tests
#       *creating git commits and -tags and pushing them upstream
#       *building and publishing
#
# Dependencies:
#   {basename, dirname, realpath} (coreutils), getopt (util-linux), git, uv
#
# Usage:
#   ./bump-version.sh [options]
#
# Example:
#   ./backup_logs.sh --patch
#
# Author: Kai Elsässer <kai.elsaesser@posteo.de>
# Version: 0.1.0

# establish paths
SCRIPT="$(realpath "${0}")"
NAME="$(basename -s ".sh" "$SCRIPT_PATH")"

. $(dirname "$SCRIPT")/_project_env.sh

DEPENDENCIES=("getopt::util-linux" "git" "uv")

for dep in "$DEPENDENCIES"; do
    check_dep "$dep"
done

VERSION="0.1.0"
DESCRIPTION="A script to bump the version of the project using uv."
USAGE="Usage: $NAME [options]"
OPTIONS="\
Options:
    -h, --help            Show this help message and exit
    -V, --version         Show script version and exit
    -p, --patch           Bump patch version, 1.0.0 → 1.0.1 (default)
    -m, --minor           Bump minor version, 1.0.0 → 1.1.0
    -M, --major           Bump major version, 1.0.0 → 2.0.0
    -e, --explicit \"{X.Y.Z}\"       
                          Bump to an explicit version, e.g. "1.2.3"
    -c, --commit-message \"{message}\" (optional)
                          Commit message. (default: \"chore: bump version to X.Y.Z\", 
                          where patch is the type of version bump)\
"
EXAMPLE="Example: $NAME --minor"
EXAMPLE2="Example: $NAME --explicit 1.2.3"
EXAMPLE3="Example: $NAME --explicit 1.2.3 --commit-message \"chore: bump version to 1.2.3\""

print_help() {
    printf "%s\n\n" "$DESCRIPTION"
    printf "%s\n\n" "$USAGE"
    printf "%s\n" "$OPTIONS"
    printf "\n%s\n" "$EXAMPLE"
    printf "%s\n" "$EXAMPLE2"
    printf "%s\n" "$EXAMPLE3"
}

# cd into project root if not cwd
[[ "$PWD" != "$PROJECT_ROOT" ]] && cd $PROJECT_ROOT

# parse sys args
OPTS=$(getopt -o hVpmMe:c:d --long help,version,patch,minor,major,explicit:,commit-message,dry-run -n "$NAME" -- "$@")
if [ $? -ne 0 ]; then
    exit 1
fi
eval set -- "$OPTS"

while [ : ]; do
    case "${1}" in
    -h | --help)
        print_help
        exit 0
        ;;
    -V | --version)
        printf '%s v.%s\n' $NAME $VERSION
        exit 0
        ;;
    -v | --verbose)
        VERBOSITY+=1
        shift
        ;;
    -p | --patch)
        action="patch"
        shift
        ;;
    -m | --minor)
        action="minor"
        shift
        ;;
    -M | --major)
        action="major"
        shift
        ;;
    -d | --dry-run)
        dry_run=1
        shift
        ;;
    -e | --explicit)
        action="explicit"
        if [[ -z "$2" ]]; then
            printf "Error: --explicit requires a version argument\n"
            exit 1
        elif [[ ! "$2" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            printf "Error: Invalid version format. Expected \"X.Y.Z\"\n"
            exit 1
        fi
        target_version="${2}"
        shift 2
        ;;
    -c | --commit-message)
        commit_message="${2}"
        shift 2
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

# set default action to patch if no action specified
[[ ! -v action ]] && action="patch"

# get target version via dry-run to set commit message
if [[ "$action" != "explicit" ]]; then
    cmd="uv version --bump $action"
    target_version="$(eval "$cmd" --dry-run | rev | cut -d' ' -f1 | rev)"
else
    cmd="uv version --set $target_version"
fi
commit_message="chore: bump version to $target_version"

# ask user for confirmation before executing
if [[ -v dry_run ]]; then
    printf "Dry run mode enabled with the following parameters:\n"
    printf "  Action: %s\n" "${action^^}"
    printf "  Commit Message: \"%s\"\n" "$commit_message"
    printf "The following commands would be executed:\n\n"

    printf "%s\n...\n\n" "-- uv run pytest --"

    printf "%s\n" "-- $cmd --"
    eval "$cmd" --dry-run
    printf "\n"

    printf "%s\n" "-- git add pyproject.toml --"
    eval "git add --dry-run pyproject.toml"
    printf "\n"

    printf "%s\n" "-- git commit -m \"$commit_message\" --"
    eval 'git commit --quiet --dry-run -m "$commit_message"'
    printf "\n"

    printf "%s\n...\n\n" "-- git tag v\$(uv version) --"
    printf "%s\n...\n\n" "-- git push && git push --tags --"
    printf "%s\n...\n\n" "-- uv build --"
    printf "%s\n...\n\n" "-- uv publish --"

    printf "Dry run complete. No changes have been made.\n"
    exit 0
else
    printf "This will bump the version using uv with the following parameters:\n"
    printf "  Action: %s\n" "${action^^}"
    printf "  Commit Message: \"%s\"\n" "$commit_message"

    printf "Do you want to proceed? (y/N) "
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        printf "Aborting version bump.\n"
        exit 0
    fi
fi
printf "\n"

# run tests before bumping version
uv run pytest

# bump version
eval "$cmd"

# commit changes
git add pyproject.toml
git commit -m "$commit_message"

# set git tag
git tag "v$(uv version)"
eval git push && git push --tags

# build & publish package
uv build
uv publish
