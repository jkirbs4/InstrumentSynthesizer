#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <json-file>"
    exit 1
fi

./.venv/Scripts/python.exe -m src.main "$1"

