#!/bin/bash

# path
CURRENT_DIR="$(dirname (readlink -f $0)"
VENV_PATH=$CURRENT_DIR/venv/
REQUIREMENTS=$CURRENT_DIR/requirements.txt

# check if requirements.txt exits
if [ ! -f $REQUIREMENTS ]; then
    echo "File requirements.txt doesn't exist at directory " $CURRENT_DIR
    exit
fi

# Virtual Environment
if [ -e $VENV_PATH ]
then
    echo $VENV_PATH
else
    echo 'Virtualenv' $VENV_PATH 'does not exist!'
    echo -e "Creating virtualenv"
    virtualenv -p python3 venv
fi

# Run virtualenv
source venv/bin/activate
pip install -r requirements.txt

# Run script Python in venv
python3 python_code.py
