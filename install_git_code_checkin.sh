#!/bin/bash

sudo apt-get install xclip
sudo mkdir -p /usr/local/bin/python_scripts/
sudo cp git_code_checkin.py /usr/local/bin/python_scripts/
sudo ln -s /usr/local/bin/python_scripts/git_code_checkin.py /usr/local/bin/git-code-checkin
