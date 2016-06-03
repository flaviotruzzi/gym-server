#!/usr/bin/env bash

set -x
set -e

kill_descendant_processes() {
    local pid="$1"
    local and_self="${2:-false}"
    if children="$(pgrep -P "$pid")"; then
        for child in $children; do
            kill_descendant_processes "$child" true
        done
    fi
    if [[ "$and_self" == true ]]; then
        kill "$pid"
    fi
}

trap cleanup INT

cleanup() {
    kill_descendant_processes $$ true
}


if [ -v ON_DOCKER ]
then
    (cd monitor && python -m SimpleHTTPServer) & xvfb-run -s "-screen 0 1400x900x24" python gym_server.py
else
    (cd monitor && python -m SimpleHTTPServer) & python gym_server.py
fi

