#!/usr/bin/python3
import re
import sys
import argparse

parser = argparse.ArgumentParser(description="Inserts numbers after each -name: statement in Ansible playbooks.")
parser.add_argument("--filein", "-f", type=str, required=True, help="This is the Ansible Playbook you want steps numbered.")
parser.add_argument("--fileout", "-o", type=str, help="Output file name. Default is out-<filename>.")
parser.add_argument("--steps", "-s",  type=int, default=10, help="Value to increment the count with. default is 10.")
parser.add_argument("--report", "-r", default = False, action='store_true', help="Specify whether or not you want a report of steps.")
parser.add_argument("--verbose", "-v", default = False, action='store_true', help="Ouput is mirrored to stderr.")
parser.add_argument("--delete", "-d", default = False, action='store_true', help="Delete step numbering.")

args = parser.parse_args()
if (args.fileout == None): 
    fileout = "out-"
    fileout = fileout + args.filein
else: 
    fileout = args.fileout.strip()

filein = args.filein.strip()
report = args.report
steps = args.steps
verbose = args.verbose
delete = args.delete

print("Input file:", filein)

if (report != True):
    print("Output file", fileout, "\nShow Report:", report)

if (report != True):
    print("Verbose", verbose)

if (report != True):
    print("Increments:", steps, "\n")


def putNumber(filein, steps, verbose):
    numberz = 0
    with open(filein) as fr:
        fw = open(fileout, "w")
        while fr:
            line = fr.readline()
            if re.search("- name:", line):
                numberz += steps
            thisline = re.sub("- name: [0-9]*\.*[ ]*", "- name: " + str(numberz) + ". ", line)
            if (verbose):
                print(thisline.rstrip())
            fw.write(thisline)
            if line =="": 
                fr.close()
                fw.close()
                print("Done.")
                break


def deleNumber(filein, fileout, verbose):
    with open(filein) as fr:
        fw = open(fileout, "w")
        while fr:
            line = fr.readline()
            if re.search("- name:", line):
                thisline = re.sub("- name: [0-9]*\.*[ ]*", "- name: ", line)
            else:
                thisline = line
            
            if (verbose):
                    print(thisline.rstrip())
            fw.write(thisline)
            if line =="": 
                fr.close()
                fw.close()
                print("Done.")
                break

## Function to report 
def reportz(filein):
    print("\n")
    with open(filein) as fr:
        while fr:
            line = fr.readline()
            if line == "":
                fr.close()
                print("\nDone.")
                break
            if re.search("- name:", line):
                thisline = re.sub("- name:", "step:", line)
                print(thisline.rstrip())


if __name__ == '__main__':
    if (delete):
        deleNumber(filein, fileout, verbose)
        exit(0)
    elif (report):
        reportz(filein)
        exit(0)
    else:
        putNumber(filein, steps, verbose)
        exit(0)

# deleNumber(filein, fileout, verbose)

#####
#     TO DO
# 1. add stats to beginning of play for output to automation solution
## a. fileName = __file__ ( full path )
## b. repo / branch name if exists
# 2. Documentation
# 3. Output same name input with backup as .bak ( like reindent )
# 4. Take input file without the -f switch
