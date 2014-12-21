#!/usr/bin/python3
__author__ = 'Ashish Kayastha'
# Python script for automating Git code check-in emails.
# Usage: git-code-checkin -c <commit-hash>

import argparse
import subprocess
import collections
import sys
import os

changed_files_dict = collections.OrderedDict()

changed_files_dict["New"] = list()
changed_files_dict["Modified"] = list()
changed_files_dict["Renamed"] = list()
changed_files_dict["Deleted"] = list()

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Code Checkin Script")
    parser.add_argument("-c", "--commit", required=True, dest="Hash", help="Commit Hash")
    args = parser.parse_args()

    hash = args.Hash

    list_changed_files_cmd = "git diff-tree --no-commit-id --name-status -r -M {}".format(hash)
    commit_in_branch_cmd = "git branch -r --contains {}".format(hash)
    commit_hash_and_message_cmd = "git log --pretty=oneline | grep {}".format(hash)

    pipe = subprocess.Popen(list_changed_files_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pipe.communicate()

    files_list = str(out, encoding="utf_8").splitlines()

    for file in files_list:
        if file.startswith('A'):
            changed_files_dict["New"].append(file)
        elif file.startswith('M'):
            changed_files_dict["Modified"].append(file)
        elif file.startswith('R'):
            changed_files_dict["Renamed"].append(file)
        elif file.startswith('D'):
            changed_files_dict["Deleted"].append(file)
        else:
            pass

    try:
        project = input("Project: ") or "N/A"
        reviewed_by = input("Code/Unit Test Reviewed By: ") or "N/A"
        qat_by = input("QAT By: ") or "N/A"
        summary = input("Summary: ") or "N/A"
        impacts = input("Impacts: ") or "N/A"
        notes = input("Notes: ") or "N/A"
    except KeyboardInterrupt:
        sys.exit()

    pipe = subprocess.Popen(commit_in_branch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pipe.communicate()

    branch_list = str(out, encoding="utf_8").splitlines()
    branch_list = [branch.strip() for branch in branch_list]
    branches = ', '.join(branch_list)

    with open("{}/Desktop/checkin.html".format(os.getenv("HOME")), 'w') as out_file:
        pipe = subprocess.Popen(commit_hash_and_message_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pipe.communicate()

        commit = str(out, encoding="utf_8").split(' ', 1)
        commit_hash, commit_message = tuple(commit)

        out_file.write("<div><b>Project:</b>&nbsp;{}</div>".format(project))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Task:</b>&nbsp;{}</div>".format(commit_message.split(':')[0].strip('\n')))
        out_file.write("<div><br></div>")

        out_file.write("<div><div style=\"color: rgb(34, 34, 34);\"><h2 style=\"font-family: 'Lucida Grande', verdana, arial, helvetica, sans-serif; padding: 12px 20px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: rgb(174, 204, 215); color: rgb(68, 68, 68); border-top-width: 1px; border-top-style: solid; border-top-color: white; border-top-left-radius: 8px; border-top-right-radius: 8px; letter-spacing: -1px; background-image: url(https://ci5.googleusercontent.com/proxy/uePTVeN_JgVYsynEuyhDhbtB0mD6pTiFux95naGYnCiLzO_SBt6a9vE8hEb0LMrlNECS1JSVZeGt9mZ5ERQSUV8Br9Z9sOisA5P1AQ0hHkT3ze3ZPNEfnyjoZKFuRuEy-21EDuAPoa8=s0-d-e1-ft#https://deermine.deerwalk.com/themes/deerwalk-blue/images/smooth-gradient-blue.jpg); background-color: rgb(234, 242, 245);\">{}</h2></div></div>".format(commit_message.strip('\n')))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Code/Unit Test Reviewed By:</b>&nbsp;{}</div>".format(reviewed_by))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>QAT By:</b>&nbsp;{}</div>".format(qat_by))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Summary:</b>&nbsp;{}</div>".format(summary))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Impacts:</b>&nbsp;{}</div>".format(impacts))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Notes:</b>&nbsp;{}</div>".format(notes))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Git Branch:</b>&nbsp;{}</div>".format(branches))
        out_file.write("<div><br></div>")
        out_file.write("<div><b>Commit Hash:</b>&nbsp;{}</div>".format(commit_hash))
        out_file.write("<div><br></div>")

        for header, file_list in changed_files_dict.items():
            if len(file_list) != 0:
                out_file.write("<div><b>{} Files:</b><div>".format(header))

                for file in file_list:
                    i = 0
                    out_file.write("<div>")
                    for token in file.split('\t'):
                        if i == 0:
                            out_file.write("#&nbsp;&nbsp;")
                        elif i == 2:
                            out_file.write(" -> " + token)
                        else:
                            out_file.write(token)

                        i += 1
                    out_file.write("</div>")

                out_file.write("<div><br></div>")

        out_file.write("Regards,")
        out_file.close()
        os.system("xclip -selection clipboard -t text/html {}/Desktop/checkin.html".format(os.getenv("HOME")))

if __name__ == "__main__": main()
