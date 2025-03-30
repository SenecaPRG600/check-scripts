#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 5
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 5 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 5 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab5a or lab5b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab5-check-output.txt' file.
9. Submit this file along with your scripts: lab5a.py and lab5b.py.

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
from random import randint
from unittest.mock import patch

class lab5a(unittest.TestCase):
    "all tests for lab5a.py"
    '''
    Create a my_sum function that works with a list
    '''
    filename = 'lab5a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_module_import(self):
        "make sure that the file can be imported"
        err_msg = (f"Error: your lab5a file could not be imported."
                    "Make sure that lab5a is named correctly and is"
                    "in the same folder as your check script.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)  
    
    def test_my_sum(self):
        inputs=[[1,2,3], [22, 48, 60, 37], [3, 3, 5, 3, 7, 10], [4, 6, 8, 1]]
        expects=[6, 167, 31, 19]
        std = import_module(self.filename.split('.')[0])
        for i, e in zip(inputs, expects):
            err_msg = (f"Error in {self.filename}: my_sum() isn't found or isn't working."
                       f"the list {i} was passed in as argument\n"
                       f"and I expected {e} to be returned")
            self.assertEqual(std.my_sum(i), e, err_msg)
    

class lab5b(unittest.TestCase):
    "all tests for lab5b.py"
    '''
    this implements the functions that are given, students should enter comments. Also use this for __main__
    '''
    filename = 'lab5b.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_module_import(self):
        "make sure that the file can be imported"
        expected = ['snake', 'hamster', 'scorpion', 'beaver', 'mosquito', 'camel', 'vulture', 'horse', 'python', 'capybara'] 
        err_msg = (f"Error in {self.filename}: a list called 'animals'"
                    "Could not be found, or contains the wrong values")
        try:
            sts = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)  
        self.assertEqual(sts.animals, expected, err_msg)

    def test_correct_output(self):
        expect = r"hamster\r?\nbeaver\r?\ncamel\r?\nhorse\r?\ncapybara\r?\n"
        cmd = [self.pypath, self.filename]
        err_msg = (f"\nError in {self.filename}: Your script "
                f"should print even-numbered animals from the list provided.\n"
                "Hint: each animal is printed on a new line."
                f"I'm expecting: {expect}")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)


class lab5c(unittest.TestCase):
    "all tests for lab5c.py"
    '''
    New: guessing game
    '''
    filename = 'lab5c.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_list_exists(self):
        "make sure that the file can be imported"
        expected = ['snake', 'hamster', 'scorpion', 'beaver', 'mosquito', 'camel', 'vulture', 'horse', 'python', 'capybara'] 
        err_msg = (f"Error in {self.filename}: a list called 'animals'"
                    "Could not be found, or contains the wrong values")
        try:
            sts = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)  
        self.assertEqual(sts.animals, expected, err_msg)

    def test_secret_exists(self):
        expected = ['snake', 'hamster', 'scorpion', 'beaver', 'mosquito', 'camel', 'vulture', 'horse', 'python', 'capybara'] 
        err_msg = (f"Error in {self.filename}: a list called 'animals'"
                    "Could not be found, or contains the wrong values")
        try:
            sts = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)  
        self.assertIn(sts.secret, expected, err_msg)

    def test_bad_guess(self):
        input = 'kangaroo\n\n'
        expect = r"Sorry, that's not it"
        err_msg = (f"\nError in {self.filename}: Incorrect output for wrong guesses.\n"
                   f"I entered: {input}\n"
                   f"I expected: {expect}")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate(input.encode())
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_bad_letter(self):
        input = 'x\n\n'
        expect = r"Sorry, my word doesn't contain that letter."
        err_msg = (f"\nError in {self.filename}: Incorrect output for wrong letters.\n"
                   f"I entered: {input}\n"
                   f"I expected: {expect}")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate(input.encode())
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_good_letter(self):
        input = 'a\ne\ni\no\nu\n\n'
        expect = r"my word contains that letter."
        err_msg = (f"\nError in {self.filename}: Incorrect output for correct letters.\n"
                   f"I entered: {input}\n"
                   f"I expected: {expect}")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate(input.encode())
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)
        ...

class lab5d(unittest.TestCase):
    "all tests for lab5d.py"
    '''
    Testing command line arguments
    '''
    filename = 'lab5d.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_no_args(self):
        expect = r"No arguments found."
        err_msg = (f"\nError in {self.filename}: Change output if no arguments provided.")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_args(self):
        inputs = [randint(0,4) for i in range(4)]
        expect = "The name of the file you are running is: .*\\r?\\n"
        expect += "".join([f"Argument found: {i}.\\r?\\n" for i in inputs])
        err_msg = (f"\nError in {self.filename}: print ONLY the "
                   "additional command line arguments.\n"
                   f"I entered: {inputs}")
        cmd = [self.pypath, self.filename]
        for i in inputs:
            cmd.append(str(i))
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)


class lab5e(unittest.TestCase):
    "all tests for lab5e.py"
    '''
    Average calculator, but CLI.
    '''
    filename = 'lab5e.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_bad_args(self):
        expect = r"Error: ten is not a number."
        err_msg = (f"\nError in {self.filename}: Use validation to test args.")
        cmd = [self.pypath, self.filename, '2', 'ten']
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_args(self):
        range_limit = randint(1, 6)
        inputs = [randint(0,4) for i in range(range_limit)]
        exp_len = len(inputs)
        exp_avg = sum(inputs) / exp_len
        expect = f"Average for {exp_len} numbers: {exp_avg}"
        err_msg = (f"\nError in {self.filename}: print the average"
                   "of all the given command line arguments.\n"
                   f"I entered: {inputs}\n"
                   f"I expected: {expect}")
        cmd = [self.pypath, self.filename]
        for i in inputs:
            cmd.append(str(i))
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)


class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge5.py'

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
    logging.basicConfig(filename="lab5-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab5a, lab5b, lab5c, lab5d, lab5e, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

