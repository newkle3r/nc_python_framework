#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python 3 is installed
if command_exists python3; then
    echo "Python 3 is installed."
    python3_version=$(python3 --version)
    echo "Python 3 version: $python3_version"
else
    echo "Python 3 is not installed. Installing Python 3.10..."
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install python3.10
    else
        echo "Unable to install Python 3.10. Please install it manually."
        exit 1
    fi
fi

# Check if pip is installed
if command_exists pip3; then
    echo "pip3 is installed."
    pip3_location=$(which pip3)
    echo "pip3 location: $pip3_location"
else
    echo "pip3 is not installed. Installing pip..."
    if command_exists apt-get; then
        sudo apt-get install python3-pip
    else
        echo "Unable to install pip. Please install it manually."
        exit 1
    fi
fi

# Check if /var/scripts/service-API exists, if not create it
if [ ! -d /var/scripts/service-API ]; then
    mkdir /var/scripts/service-API
    echo "Created /var/scripts/service-API directory."
fi

# move to the service-API directory
cd /var/scripts/service-API || exit

# Check if the service-API repository exists, if not clone it
if [ ! -d /var/scripts/service-API/ ]; then
    git clone https://github.com/newkle3r/nc_python_framework.git
    echo "Cloned the service-API repository."
fi

# Check if the required files exist, if not download them
if [ ! -f /var/scripts/service-API/nc_python_framework/main.py ]; then
    wget https://raw.githubusercontent.com/newkle3r/nc_python_framework/main/main.py -P /var/scripts/service-API/nc_python_framework/
fi
if [ ! -f /var/scripts/service-API/nc_python_framework/functions.py ]; then
    wget https://raw.githubusercontent.com/newkle3r/nc_python_framework/main/functions.py -P /var/scripts/service-API/nc_python_framework/
fi
if [ ! -f /var/scripts/service-API/nc_python_framework/Ledger.py ]; then
    wget https://raw.githubusercontent.com/newkle3r/nc_python_framework/main/Ledger.py -P /var/scripts/service-API/nc_python_framework/
fi
if [ ! -f /var/scripts/service-API/nc_python_framework/requirements.txt ]; then
    wget https://raw.githubusercontent.com/newkle3r/nc_python_framework/main/requirements.txt -P /var/scripts/service-API/nc_python_framework/
fi
if [ ! -f /var/scripts/service-API/nc_python_framework/paperless.py ]; then
    wget https://raw.githubusercontent.com/newkle3r/nc_python_framework/main/paperless.py -P /var/scripts/service-API/nc_python_framework/
fi


# install the requirements.txt
pip3 install -r /var/scripts/service-API/nc_python_framework/requirements.txt

# make empty env_variables.json
echo "{}" > /var/scripts/service-API/nc_python_framework/env_variables.json
# make empty filesystem.json
echo "{}" > /var/scripts/service-API/nc_python_framework/filesystem.json

# Upgrade PyYAML, MarkupSafe, and Jinja2 if they are already installed
pip3 install --upgrade PyYAML MarkupSafe Jinja2

python3 /var/scripts/service-API/nc_python_framework/main.py


