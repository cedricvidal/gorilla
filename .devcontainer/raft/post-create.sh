#!/bin/bash

cd raft

echo "Allowing raft direnv"
direnv allow

echo "Creating virtual environment"
python3 -m venv .venv
. ./.venv/bin/activate

echo "Upgrading pip"
pip install --upgrade pip

echo "Installing requirements"
pip install -r requirements.txt

echo "Utilities to display PDFs in notebooks"
sudo apt-update && \
    sudo apt install -y libmagickwand-dev && \
    sudo sed -i /PDF/d /etc/ImageMagick-6/policy.xml
