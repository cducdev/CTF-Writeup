#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: ./setup.sh level-XX-YY" >&2
    exit 1
fi

level_name="$1"
level_path="levels/$level_name"

mkdir -p "$level_path/assets"
cp TEMPLATE.md "$level_path/README.md"
touch "$level_path/password.txt"
