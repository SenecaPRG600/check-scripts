#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 6
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 6 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 6 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab6a or lab6b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab6-check-output.txt' file.
9. Submit this file along with your scripts: lab6a.py and lab6b.py.

PROBLEMS? BUGS? E-mail me!
'''

import unittest
import os
import hashlib
import logging
import datetime
import subprocess as sp
import sys
from importlib import import_module
from random import shuffle

class lab6a(unittest.TestCase):
    "all tests for lab6a.py"
    '''
    Writes to testing.txt and writes to separate lines.
    output: 
    First Line!
    Second Line!!
    Third Line!!!
    ...and so on!
    '''
    filename = 'lab6a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            os.remove('testing.txt')
        except FileNotFoundError:
            pass
    
    def test_module_import(self):
        "lab6a must include the correct list"
        "make sure that the script contains the correct list of lines"
        expected = ['First Line!', 'Second Line!!', 'Third Line!!!', '...and so on!']
        err_msg = (f"Error: your lab6a does not contain a proper list"
                    "Make sure to copy 'data_to_write' into lab6a"
                    "EXACTLY as how it appears in the lab.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        self.assertEqual(std.data_to_write, expected, err_msg)

    def test_correct_output(self):
        "lab6a must write the list, each item on a new line"
        expect = r"First Line!\r?\nSecond Line!!\r?\nThird Line!!!\r?\n...and so on!\r?\n"
        cmd = [self.pypath, self.filename]
        err_msg = (f"\nError in {self.filename}: Your script "
                f"should write each item on the list onto a new line\n"
                "Hint: append a newline character after each item."
                f"I'm expecting: {expect}")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        with open('testing.txt') as f:
            self.assertRegex(f.read(), expect, err_msg)


class lab6b(unittest.TestCase):
    "all tests for lab6b.py"
    '''
    given cmd arg, print data in reverse order
    default is readme.txt
    '''
    filename = 'lab6b.py'
    testfile = '6bdebug'
    expect = r""

    def shuffle(self):
        lst = ['abc', 'def', 'ghi', 'jkl', 'mno']
        shuffle(lst)  # new order each time
        with open(self.testfile, 'w') as f:
            for item in lst:
                f.write(item + '\n')
        for item in reversed(lst):
            self.expect += item + '\r?\n'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        self.assertTrue(os.path.exists('readme.txt'), msg='make sure that you have created readme.txt as per instructions.')
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass
        self.shuffle()

    def test_with_arg(self):
        "Print reversed lines for a testfile I specify"
        cmd = [self.pypath, self.filename, self.testfile]
        err_msg = (f"\n\nError in {self.filename}:"
                f"When a command line argument is given,\n"
                "use it instead of readme.txt.\n"
                "make sure that there is a single newline after each line, \n"
                "and that the lines are reversed.\n")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), self.expect, err_msg)

    def test_no_args(self):
        "Print reversed lines, use readme.txt as default"
        expect = r"and goodbye.\r?\nI would just like to say hello again!\r?\nthis is the third line.\r?\nthis is the second line.\r?\nhello world\r?\n"
        cmd = [self.pypath, self.filename]
        err_msg = (f"\n\nError in {self.filename}:"
                f"When no command line argument is given,\n"
                "default to opening readme.txt."
                f"I'm expecting: \n{expect}")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def tearDown(self):
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass


class lab6c(unittest.TestCase):
    "all tests for lab6c.py"
    '''
    Grep task with line numbers
    - usage msg
    Usage: lab6c.py keyword filename
    - filenotfound
    ERROR: missing.txt not found.
    '''
    filename = 'lab6c.py'
    testfile = '6cdebug'
    exp = r""  # expected output: line # and results
    
    def shuffle(self):
        lst = ['abc', 'def', 'abcdef', 'xyz', 'acab', 'acac']
        shuffle(lst)  # new order each time
        with open(self.testfile, 'w') as f:
            for ln, item in enumerate(lst, start=1):
                f.write(item + '\n')
                if 'ab' in item:
                    self.exp += str(ln)+ ': ' + item + '\r?\n'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass
        self.shuffle()

    def test_output(self):
        "use testfile we create, output should contain line numbers"
        cmd = [self.pypath, self.filename, 'ab', self.testfile]
        err_msg = (f"\nError in {self.filename}:\n"
                f"Results printed did not match what's expected for the \n"
                "file given. Make sure your output includes line numbers!\n"
                "For example: \n"
                "1: hello world")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), self.exp, err_msg)

    def test_usage_msg(self):
        "Usage: printed when no args"
        cmd = [self.pypath, self.filename]
        expect = r"(?i)usage: "
        err_msg = (f"\nError in {self.filename}:\n"
                f"If no argument provided, print a\n"
                "helpful usage message. For example:\n"
                f"Usage: {self.filename} keyword filename")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_error_msg(self):
        "ERROR: printed when bad filename"
        cmd = [self.pypath, self.filename, 'ab', 'bloop']
        expect = r"(?i)error:.*bloop"
        err_msg = (f"\nError in {self.filename}:\n"
                f"If an invalid filename is passed, catch\n"
                "the exception and print an error message.\n"
                f"For example:\n"
                f"ERROR: bloop not found.")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        self.assertRegex(output.decode('utf-8'), expect, err_msg)
    
    def tearDown(self):
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass


class lab6d(unittest.TestCase):
    "all tests for lab6d.py"
    '''
    letters and numbers, print sums and output only letters.
    '''
    filename = 'lab6d.py'
    testfile = '6ddebug'
    exp_sum = r""  # the expected printed sums of each line
    exp_out = r""  # expected contents of the file
    
    def shuffle(self):
        lst = [
            {'in': 'a o 4 y 5', 'sum': '9.0', 'exp': 'a o y'},
            {'in': 'gh 11 i 5.2', 'sum': '16.2', 'exp': 'gh i'},
            {'in': '2.9 x 2 y', 'sum': '4.9', 'exp': 'x y'},
            {'in': '2 3 o 1 op', 'sum': '6.0', 'exp': 'o op'},
            {'in': '12 ay 0.2 i', 'sum': '12.2', 'exp': 'ay i'}
        ]
            
        shuffle(lst)  # new order each time
        with open(self.testfile, 'w') as f:
            for item in lst:
                f.write(item['in'] + '\n')
                self.exp_sum += item['sum'] + '\r?\n'
                self.exp_out += item['exp'] + '\r?\n'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass
        self.shuffle()
    
    def test_sums(self):
        "Prints sums using my testfile"
        cmd = [self.pypath, self.filename, self.testfile]
        err_msg = (f"\nError in {self.filename}:\n"
                f"Sums printed did not match for the \n"
                "file given. HINT: convert to float.\n")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), self.exp_sum, err_msg)
    
    def test_file_out(self):
        "testfile is updated with no numbers"
        cmd = [self.pypath, self.filename, self.testfile]
        err_msg = (f"\nError in {self.filename}:\n"
                f"File contents did not match for the \n"
                "file given. HINT: Make sure the contents\n"
                "of the file don't have any trailing spaces.")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        with open(self.testfile) as f:
            self.assertRegex(f.read(), self.exp_out, err_msg)

    def test_usage_msg(self):
        "Usage: printed when no args"
        cmd = [self.pypath, self.filename]
        expect = r"(?i)usage: "
        err_msg = (f"\nError in {self.filename}:\n"
                f"If no argument provided, print a\n"
                "helpful usage message. For example:\n"
                f"Usage: {self.filename} target")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_error_msg(self):
        "ERROR: printed when bad filename"
        cmd = [self.pypath, self.filename, 'bloop']
        expect = r"(?i)error:.*bloop"
        err_msg = (f"\nError in {self.filename}:\n"
                f"If an invalid filename is passed, catch\n"
                "the exception and print an error message.\n"
                f"For example:\n"
                f"ERROR: bloop not found.")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        self.assertRegex(output.decode('utf-8'), expect, err_msg)
    
    def tearDown(self):
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass

class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge6.py'

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
    logging.basicConfig(filename="lab6-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info(f"{sys.argv[0]} {ChecksumLocal(sys.argv[0])}")
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab6a, lab6b, lab6c, lab6d, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

