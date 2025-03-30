#!/usr/bin/env python3

'''
Submission Checker

1. From Blackboard, right-click a lab and choose 'Download assignment'.
2. Save zip file into a directory. Extract files.
3. Run this script, with either a target directory or target file.

This checker will:

1. [x] Create a list of all files.
2. [x] Find Usernames.
3. [x] Associate usernames with a score out of 5.
4. [x] Identify which lab this is (lab 1, 2, etc.) and associate that with deliverable list.
5. [x] Attempt to associate usernames with an output file
5a. (if no output file exists, deduct 2 marks and flag).
6. [x] Open the output file, and find all successes.
7. [x] Test the corresponding script to make sure md5sum matches.
8. [x] If a challenge file is missing, -1 mark.
9. [x] If one required file is missing, -2 mark. 
10. [x] If more than one required file is missing, 0/5.
11. [ ] Export findings into a CSV file.  

TODO: as usual, my schema left something to be desired!!
I added 'hashes' to dicts, So far nothing seems broken, but we'll see.
1. I'm doing a lot of parsing of 'deliverables' outside of the class.
2. change {'Lab 6': []} -> {'Name': 'Lab 6' 'files': []}
3. Just pass in the dictionary, take apart the info internally.
4. if 'hash' key is missing, ignore for now.
5. Otherwise do the check.
'''

import csv
import sys
from os import path, walk
import fnmatch
import hashlib
from colorama import Fore, Style
import re

deliverables = [
    {'Lab 1': ['lab1a.py', 'lab1b.py', 'lab1-check-output.txt']},
    {'Lab 2': ['lab2a.py', 'lab2b.py', 'datatypes.txt', 'challenge2.py', 'lab2-check-output.txt']},
    {'Lab 3': ['lab3a.py', 'lab3b.py', 'lab3c.py', 'lab3d.py', 'lab3e.py', 'flowchart.pdf', 'challenge3.py', 'lab3-check-output.txt']},
    {'Lab 4': ['lab4a.py', 'lab4b.py', 'lab4c.py', 'challenge4.py', 'lab4-check-output.txt']},
    {'Lab 5': ['lab5a.py', 'lab5b.py', 'lab5c.py', 'lab5d.py', 'lab5e.py', 'challenge5.py', 'lab5-check-output.txt']},
    {'Lab 6': ['lab6a.py', 'lab6b.py', 'lab6c.py', 'lab6d.py', 'challenge6.py', 'lab6-check-output.txt'], 'hash': '28a91ca5840d32645504b88395ff4a54'},
    {'Lab 7': ['lab7a.py', 'lab7b.py', 'lab7c.py', 'lab7d.py', 'challenge7.py', 'lab7-check-output.txt'], 'hash': '42055640e93721e17d158e40b137c684'},
    {'Lab 8': ['regex.txt', 'lab8a.py', 'lab8b.py', 'lab8c.py', 'lab8d.py', 'lab8e.py', 'lab8-check-output.txt'], 'hash': '65a559c8a4a6ecf5413609387ff74780'}
]

submissions = []

class Submission():
    "contains name, pass/fail for each lab"

    total = 5

    def __init__(self, name, requirements):
        self.name = name  # student id
        self.filepaths = {}  # each requirement mapped to filepath
        self.ftests = {}  # F/T for fail/pass of each requirement
        self.requirements = requirements
        for file in requirements:
            self.ftests[file] = False
            self.filepaths[file] = None
        self.checkoutput = None
        self.notes = ""  # summary of what went wrong

    def ChecksumLocal(self, filename=None):
        fil = open(filename, 'r', encoding='utf-8')
        dat = fil.readlines()
        textdata = ''
        for line in dat:
            textdata = textdata + line
        checksum = hashlib.md5(textdata.encode('utf-8')).hexdigest()  # hexdigest for a string
        return checksum

    def get_score(self):
        "calculate p/f"
        hashes = self.get_hashes()
        lab_fails = 0  # more than 1 means 0/5
        lab_reg = r'lab\d[a-z]\.py'  # this makes it a required scriptfile
        chal_reg = r'challenge\d\.py'  # a challege must be attempted
        output_reg = r'check-output'
        score = 5  # ultimately out of 5
        if self.checkoutput is None:
            self.notes = "Output file not found. Recommend manual testing\n"
            score = 0
        else:
            for file in self.ftests:
                if re.match(lab_reg, file):  # if the file is a lab file,
                    try:
                        hash = ""  # placeholder in case file not found
                        assert self.filepaths[file] is not None, f'{file} not found'
                        suc = hashes.get(file, False)  # file has a valid hash in output, indicating pass
                        assert suc is not False, f'{file} failed check'
                        hash = self.ChecksumLocal(self.filepaths[file])  # get hash if it is.
                        assert hash in hashes.values(), f'hash for {file} not valid'
                        self.ftests[file] = True
                    except AssertionError as msg:
                        self.notes += str(msg)+'\n' 
                        self.notes += str(hash)+'\n'  # print hash for comparison
                        lab_fails += 1
                        score -= 2
                elif re.match(chal_reg, file):
                    try:
                        assert self.filepaths[file] is not None, f'{file} not found'
                        hash = self.ChecksumLocal(self.filepaths[file])
                        assert hash in hashes.values(), f'hash for {file} not valid'
                        self.ftests[file] = True
                    except AssertionError as msg:
                        self.notes += str(msg)+'\n'
                        score -= 1
                elif re.match(output_reg, file): # if is an output file,
                    try:
                        assert self.filepaths[file] is not None, f'{file} not found'
                        self.ftests[file] = True
                    except AssertionError as msg:
                        print('should not be reaching this. check.')
                        self.notes += str(msg)+'\n'
                else:
                    try:
                        assert self.filepaths[file] is not None, f'{file} not found'
                        self.ftests[file] = True
                    except AssertionError as msg:
                        lab_fails += 1
                        self.notes += str(msg)+'\n'
            if lab_fails > 1:
                score = 0
            elif lab_fails > 0:
                score = 3
        self.score = score


    def get_hashes(self):
        "open output, compare each hash"
        if self.checkoutput is not None:
            reg = re.compile(r'\w+\.\w{2,3} [0-9a-f]{32}')
            matches = re.findall(reg, self.checkoutput)
            rtn = dict()
            for m in matches:
                f, h = m.split(' ')
                rtn[f] = h
            return rtn


    def add_file(self, filepath):
        "flip switch, do md5sum"
        if fnmatch.fnmatch(filepath, '*-check-output.txt'):
            with open(filepath) as f:  # save contents of output for later use
                self.checkoutput = f.read()
        for rq in self.requirements:  # if file matches a requirement, add it
            if fnmatch.fnmatch(filepath, '*' + rq):
                self.filepaths[rq] = filepath
                return True  # indicates file added successfully
        raise AssertionError("Not added.")
            

    def print_sum(self):
        "show summary for student"
        self.get_score()
        print("=================================")
        print(Fore.BLUE + self.name)
        print(Style.RESET_ALL)
        for k,v in self.ftests.items():
            if v == False:
                print(f"{Fore.RED}{k:<28}{'[❌]':>5}{Style.RESET_ALL}")
            else:
                print(f"{k:<28}{'[✅]':>5}")
        print(f"Score: {self.score}/{self.total}")
        print(f"{self.notes}")
        print("=================================")
        print()

        
    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Submission):
            return self.name == other.name
        else: 
            return self.name == other

    def __gt__(self, other):
        if isinstance(other, Submission):
            return self.name > other.name
        else: 
            return self.name > other
    
    def __lt__(self, other):
        if isinstance(other, Submission):
            return self.name < other.name
        else: 
            return self.name < other


def get_all_files_in_dir(dir, file_list):
    for root,dirs,files in walk(dir):
        for file in files:
            # pth = path.abspath(file) omits base dir apparently
            pth = path.join(root, file)
            file_list.append(pth)

def extract_f_name_data(filepath):
    "try to get username from filename"
    file = path.basename(filepath)
    filename, ext = path.splitext(file)
    try:
        lst = filename.split('_')
        task = lst[0]
        stname = lst[1]
        labfile = lst[-1]
    except (ValueError, IndexError):
        print('file split failed')
        task = None
        stname = None
        labfile = filename
    return (task, stname, labfile)



if __name__ == "__main__":
    file_list = []
    dir_list = []
    flagged_list = []  # something wrong with these
    if len(sys.argv) == 1:
        dir_list.append('.')
    else:
        for arg in sys.argv[1:]:
            if path.isfile(arg):
                file_list.append(path.abspath(arg))
            elif path.isdir(arg):
                dir_list.append(arg)
    for dir in dir_list:
        get_all_files_in_dir(dir, file_list)
    if len(file_list) == 0:
        print(f"Error: no files found.")
        sys.exit()
    task = extract_f_name_data(file_list[0])[0]
    requirements = next((item[task] for item in deliverables if task in item), False)
    if not requirements:
        print("What assignment is this?")
        sys.exit(1)
    reg = re.compile(r'.*attempt_\d{4}(-\d{2}){5}\.txt')  # remove attempt summary files
    file_list = [x for x in file_list if not re.match(reg, x)]
    while len(file_list) != 0:
        file = file_list.pop()
        t, st, f = extract_f_name_data(file)
        if t != task:
            flagged_list.append(file)
        else:
            if st not in submissions:  
                submissions.append(Submission(st, requirements))
            for studentid in submissions:
                if st == studentid:
                    try:
                        studentid.add_file(file)
                        break
                    except AssertionError:  # if not added, save for later
                        flagged_list.append(file)
    for i in sorted(submissions):
        i.print_sum()
    print('Files remaining: ' + str(len(file_list)))
    print(file_list)
    print(flagged_list)
        
