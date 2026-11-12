#!/bin/bash
# One-time setup for this project: creates .venv inside this folder and
# installs the packages into it. Run from the project folder:  ./setup.sh
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo ""
echo "Done. Open this folder in VS Code, open the notebook, and check the"
echo "kernel (top right) says .venv — then run the first two cells."
