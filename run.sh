#!/usr/bin/env bash
this_dir="$( cd "$( dirname "$0" )" && pwd )"

source "${this_dir}/.venv/bin/activate"
python3 "${this_dir}/main.py"
