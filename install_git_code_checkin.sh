#!/bin/bash

sudo apt-get install xclip
sudo mkdir -p /usr/local/bin/python_scripts/
echo "Directory 'python_scripts' created in '/usr/local/bin'."
sudo cp git_code_checkin.py /usr/local/bin/python_scripts/
echo "Copied 'git_code_checkin.py' to '/usr/local/bin/python_scripts/'."
sudo ln -s /usr/local/bin/python_scripts/git_code_checkin.py /usr/local/bin/git-code-checkin
echo "Created a symbolic link 'git-code-checkin'."
