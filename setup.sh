#!/bin/bash
echo Setting up virtual environment, please wait!
echo Do not close this window until you are told to do so!

# Constants
PWD=`pwd`

echo Generating venv folder...
# Generate VENV in project dir
python3 -m venv $PWD/venv

echo Installing dependencies...
# Activate the VENV
activate () {
	. $PWD/venv/bin/activate
}
activate

# Install requirements
pip install wheel
pip install -r requirements.txt
echo Sequence completed! You may now close this window:
read -rsp $'Press any key to continue...\n' -n1 key