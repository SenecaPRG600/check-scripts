#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 4
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 4 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 4 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab4a or lab4b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab4-check-output.txt' file.
9. Submit this file along with your scripts: lab4a.py and lab4b.py.

PROBLEMS? BUGS? E-mail me!
'''

import unittest
import os
import hashlib
import logging
import datetime
import subprocess as sp
import sys
import re
from importlib import import_module

class lab4a(unittest.TestCase):
    "all tests for lab4a.py"
    '''
    Lab4a is 3d (guessing game) but with tests for numeric/non-numeric and out of bounds.
    '''
    filename = 'lab4a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_out(self):
        input = "".join([f"{i}\n" for i in range(0,11)])
        expect = r"Correct! You win"
        err_msg = (f"Error in {self.filename}: Your script should use "
                   "random.randint to select a secret number. "
                   "Use the variable name 'secret'.")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = (n.decode('utf-8') for n in p.communicate(input.encode()))
        if p.returncode != 0:
            logging.error(error)
            raise IOError("Error running the script.")
        self.assertRegex(output, expect, err_msg)
    
    def test_import(self):
        "check to see if randint is in the file"
        err = (f"Error in {self.filename}: not importing randint.")
        with open(self.filename) as f:
            contents = f.read()
        self.assertIn('randint', contents, err)
    
    def test_incorrect_non_num(self):
        input = "hamburger\n".join([f"{i}\n" for i in range(0,11)])
        expect = r"Error: not a number or out of bounds"
        err_msg = (f"Error in {self.filename}: Your script should "
                   "test to see if user input is numeric and"
                   f"print {expect} if not.")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = (n.decode('utf-8') for n in p.communicate(input.encode()))
        if p.returncode != 0:
            logging.error(error)
            raise IOError("Error running the script.")
        self.assertRegex(output, expect, err_msg)
        
    
    def test_incorrect_bound(self):
        inputs = ['0\n', '11\n']
        expect = r"Error: not a number or out of bounds"
        err_msg = (f"Error in {self.filename}: Your script should "
                   "test to see if user input is between 1 and 10"
                   f" and print {expect} if not.")
        cmd = [self.pypath, self.filename]
        for i in inputs:
            input = i.join([f"{f}\n" for f in range(0,11)])
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = (n.decode('utf-8') for n in p.communicate(input.encode()))
            if p.returncode != 0:
                logging.error(error)
                raise IOError("Error running the script.")
            self.assertRegex(output, expect, err_msg)

class lab4b(unittest.TestCase):
    "all tests for lab4b.py"
    '''
    this implements the functions that are given, students should enter comments. Also use this for __main__
    '''
    filename = 'lab4b.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_module_import(self):
        "make sure that the file can be imported"
        err_msg = (f"Error: your lab4 file could not be imported."
                    "Make sure that lab4b is named correctly and is"
                    "in the same folder as your check script.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)   

    def test_is_odd(self):
        std = import_module(self.filename.split('.')[0])
        err_msg = f"Error in {self.filename}: is_odd() should return True/False"
        self.assertTrue(std.is_odd(13), err_msg)

    def test_area(self):
        std = import_module(self.filename.split('.')[0])
        err_msg = f"Error in {self.filename}: rtrn_area() should take two arguments and return them multiplied"
        self.assertEqual(std.rtrn_area(12, 20), 240, err_msg)


class lab4c(unittest.TestCase):
    "all tests for lab4c.py"
    '''
    Radius calculator. Enter to exit.
    Needs a function.
    '''
    filename = 'lab4c.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_function(self):
        std = import_module(self.filename.split('.')[0])
        inputs = [2, 17, 5, 12]
        expects = [12.5663, 907.92027, 78.53975, 452.38896]
        for i,e in zip(inputs, expects):
            err_msg = (f"\nError in {self.filename}: circle_area() needs to exist"
            " and should return area as a float.\n"
            "I inputted: {i}\n"
            "I expected: {e}")
            self.assertAlmostEqual(std.circle_area(i), e, 3, err_msg)

    def test_correct_output(self):
        inputs = ['2\n4\n\n']
        expects = [r"12\.566.*\r?\n.*50\.265"]
        # expects = [r"Radius: 2\."]
        cmd = [self.pypath, self.filename]
        for i,e in zip(inputs, expects):
            err_msg = (f"\nError in {self.filename}: Your script "
                    f"should print the radius and the area for the user input.\n"
                    f"I inputted: {i}.\n"
                    f"I expected: {e}.\n")
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = (n.decode('utf-8') for n in p.communicate(i.encode()))
            if p.returncode != 0:
                logging.error(error)
                raise IOError("Error running the script.")
            self.assertRegex(output, e, err_msg)
    
    def test_incorrect_output(self):
        inputs = ['ten\n\n', '2001\n\n']
        expects = [r"Error: ten is not a number", r"Error: 2001 is out of "]
        cmd = [self.pypath, self.filename]
        for i,e in zip(inputs, expects):
            err_msg = (f"\nError in {self.filename}: Your script "
                    "should print the radius and the area for the user input.\n"
                    f"I inputted: {i}.\n"
                    f"I expected: {e}.")
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = (n.decode('utf-8') for n in p.communicate(i.encode()))
            if p.returncode != 0:
                logging.error(error)
                raise IOError("Error running the script.")
            self.assertRegex(output, e, err_msg)


class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge4.py'

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
    logging.basicConfig(filename="lab4-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab4a, lab4b, lab4c, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

