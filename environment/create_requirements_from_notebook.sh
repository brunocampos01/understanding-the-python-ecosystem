#!/bin/bash
# Description:   Create file with requirements
# Author:        brunocampos01
# Input:         N/A
# Output:        requirements.txt
# ----------------------------------- #
PROJECT_DIR="$(dirname $(readlink -f $0))"

rm -f requirements.txt
touch requirements.txt

# Convert files .ipynb to python
jupyter nbconvert --to python notebooks/*.ipynb

# Generate requirements
pipreqs notebooks/ --force --savepath requirements.txt

# Remove converted files
rm -rf notebooks/*.py

# Show requirements
echo -e "Requirements this project:\n"
cat requirements.txt
