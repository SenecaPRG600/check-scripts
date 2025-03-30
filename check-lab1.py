#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 1
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 1 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 1 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab1a or lab1b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab1-check-output.txt' file.
9. Submit this file along with your scripts: lab1a.py and lab1b.py.

PROBLEMS? BUGS? E-mail me!
'''

import unittest
import os
import hashlib
import logging
import datetime
import subprocess as sp
import sys

class lab1a(unittest.TestCase):
    "all tests for lab1a.py"

    filename = 'lab1a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_1a(self):
        err = False
        err_msg = ("Error in lab1a.py: Make sure that your text matches what's "
                  "specified in the lab exactly.")
        expect = r".*[Hh]ello Melissa!\r?\n"
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = (n.decode('utf-8') for n in p.communicate(b"Melissa"))  
        if p.returncode != 0:
            logging.error(stderr)
            raise IOError("Error running the script.")
        self.assertRegex(stdout, expect, err_msg)

class lab1b(unittest.TestCase):
    "all tests for lab1b.py"

    filename = 'lab1b.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_1b(self):
        input = "Melissa\n123\n69\ntuna\n"
        expect = r"Melissa is 69 years old and loves to eat tuna!"
        err_msg = (f"Error in lab1b.py: Your script should ask the user "
                   "four questions and use the text of three of those "
                   "questions in the second-to-last line.\n"
                   f"I entered: {input}"
                   f"I expected: {expect}.")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = (n.decode('utf-8') for n in p.communicate(input.encode()))  
        if p.returncode != 0:
            logging.error(stderr)
            raise IOError("Error running the script.")
        self.assertRegex(stdout, expect, err_msg)

def ChecksumLocal(filename=None):
    fil = open(filename, 'r', encoding='utf-8')
    dat = fil.readlines()
    textdata = ''
    for line in dat:
        textdata = textdata + line
    checksum = hashlib.md5(textdata.encode('utf-8')).hexdigest()  # hexdigest for a string
    return checksum

if __name__ == '__main__':
    logging.basicConfig(filename="lab1-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)

    for case in lab1a, lab1b:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

