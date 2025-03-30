#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 2
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 2 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 2 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab2a or lab2b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab1-check-output.txt' file.
9. Submit this file along with your scripts: lab2a.py and lab2b.py.

PROBLEMS? BUGS? E-mail me!
'''

import unittest
import os
import hashlib
import logging
import datetime
import subprocess as sp
import sys

class lab2a(unittest.TestCase):
    "all tests for lab2a.py"

    filename = 'lab2a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_2a(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "adds two numbers and re-creates the output "
                  "specified in the lab exactly.")
        inp = '6\n7\n'
        expect = r"The \w+ of 6 \w+ 7 is: 13"
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = (n.decode('utf-8') for n in p.communicate(inp.encode()))  
        if p.returncode != 0:
            logging.error(error)
            raise IOError("Error running the script.")
        self.assertRegex(output, expect, err_msg)

class lab2b(unittest.TestCase):
    "all tests for lab2b.py"

    filename = 'lab2b.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_2b(self):
        inputs = ['46000\n2\n', '28000\n3\n', '67500\n4\n', '8000\n1\n']
        expects = [r"\$4800", r"\$1200", r"\$12375", r"\$0"]
        err_msg = (f"Error in lab2b.py: Your script should ask the user "
                   "for gross income and then dependents and should "
                   "return the result with a $ symbol in front.\n"
                   f"I entered: {inputs[0]}"
                   f"I expected: {expects[0]}.")
        cmd = [self.pypath, self.filename]
        for i,e in zip(inputs, expects):
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = (n.decode('utf-8') for n in p.communicate(i.encode()))
            if p.returncode != 0:
                logging.error(error)
                raise IOError("Error running the script.")
            self.assertRegex(output, e, err_msg)

class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge2.py'

    def test_exists(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

def ChecksumLocal(filename=None):
    fil = open(filename, 'r', encoding='utf-8')
    dat = fil.readlines()
    textdata = ''
    for line in dat:
        textdata = textdata + line
    checksum = hashlib.md5(textdata.encode('utf-8')).hexdigest()  # hexdigest for a string
    return checksum

if __name__ == '__main__':
    logging.basicConfig(filename="lab2-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab2a, lab2b, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

