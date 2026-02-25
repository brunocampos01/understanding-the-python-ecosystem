#!/bin/bash
set -euo pipefail
# Description:   Create a requirements file from notebooks
# Author:        brunocampos01
# Input:         N/A
# Output:        requirements.txt
# ----------------------------------- #

NOTEBOOKS_DIR="notebooks"

if [ ! -d "$NOTEBOOKS_DIR" ]; then
    echo "Error: Directory '$NOTEBOOKS_DIR' not found."
    exit 1
fi

command -v jupyter >/dev/null 2>&1 || { echo "Error: jupyter is not installed."; exit 1; }
command -v pipreqs >/dev/null 2>&1 || { echo "Error: pipreqs is not installed."; exit 1; }

rm -f requirements.txt
touch requirements.txt

# Convert files .ipynb to python
jupyter nbconvert --to python "$NOTEBOOKS_DIR"/*.ipynb

# Generate requirements
pipreqs "$NOTEBOOKS_DIR/" --force --savepath requirements.txt

# Remove converted files
rm -f "$NOTEBOOKS_DIR"/*.py

# Show requirements
echo -e "Requirements for this project:\n"
cat requirements.txt
