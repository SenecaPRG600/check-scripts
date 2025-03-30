#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 3
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 3 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 3 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab3a or lab3b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab1-check-output.txt' file.
9. Submit this file along with your scripts: lab3a.py and lab3b.py.

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

class lab3a(unittest.TestCase):
    "all tests for lab3a.py"
    '''
    Lab3a is a math quiz. Get numbers, enter solution, test mistakes. Use s to skip.
    '''
    filename = 'lab3a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_correct_output(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "accepts a correct answer by the user.")
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        try:
            wrong = '0'
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            q = p.stdout.readline().decode('utf-8')
            num_reg = re.compile(r"\d{1,2}")
            nums = [ int(num) for num in num_reg.findall(q) ]
            result = str(sum(nums))
            p.stdin.write(result.encode() + b'\n')
            p.stdin.flush()
            try:
                out = p.stdout.readline().decode('utf-8')
            except AttributeError:
                print("Your script has encountered an exception. Fix and try again.")
                logging.error(p.stderr.readline().decode('utf-8'))
            self.assertRegex(out, r'\s[Cc]orrect', err_msg)
        except (BrokenPipeError):
            pass

        p.stdin.close()
        p.terminate()
        p.wait(timeout=0.2)
    
    def test_incorrect_output(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "tells the user that an incorrect answer is incorrect.")
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        try:
            wrong = '0'
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            try:
                out = p.stdout.readline().decode('utf-8')
            except AttributeError:
                print("Your script has encountered an exception. Fix and try again.")
                logging.error(p.stderr.readline().decode('utf-8'))
            self.assertRegex(out, r'[Ii]ncorrect', err_msg)
        except (BrokenPipeError):
            pass

        p.stdin.close()
        p.terminate()
        p.wait(timeout=0.2)

    def test_skips(self):
        err_msg = (f"Error in {self.filename}: Make sure that "
        "entering 's' will skip tests, and that 0.0% is returned "
        "if all tests are skipped.")
        i = 's\ns\ns\ns\n'
        e = r'\s0.0%'
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        output, error = p.communicate(i.encode())
        if p.returncode != 0:
            logging.error(output.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), e, err_msg)
        
    def test_incorrect_repeat(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "loops until a correct answer is given by the user.")
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        try:
            wrong = '0'
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            q = p.stdout.readline().decode('utf-8')
            num_reg = re.compile(r"\d{1,2}")
            nums = [ int(num) for num in num_reg.findall(q) ]
            inc_reg = r"Incorrect"
            nums_reg = f"{nums[0]}.*{nums[1]}"
            # nums_reg = nums_reg.encode('string-escape')
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            try:
                out = p.stdout.readline().decode('utf-8')
                p.stdin.write(wrong.encode() + b'\n')
                p.stdin.flush()
                out2 = p.stdout.readline().decode('utf-8')
            except AttributeError:
                print("Your script has encountered an exception. Fix and try again.")
                logging.error(p.stderr.readline().decode('utf-8'))
            self.assertEqual(out, out2, err_msg)
        except (BrokenPipeError):
            pass

        p.stdin.close()
        p.terminate()
        p.wait(timeout=0.2)

class lab3b(unittest.TestCase):
    "all tests for lab3b.py"
    '''
    Converting a flow chart to code. Count to 10. In lab, specify PRINT.'''
    filename = 'lab3b.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_out(self):
        expect = r"0\s+1\s+2\s+3\s+4\s+5\s+6\s+7\s+8\s+9\s+10\s+[Ff]inish"
        err_msg = (f"Error in {self.filename}: Your script should "
                   "count from 0 to 10, and then print finished ")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = (n.decode('utf-8') for n in p.communicate())
        if p.returncode != 0:
            logging.error(error)
            raise IOError("Error running the script.")
        self.assertRegex(output, expect, err_msg)

class lab3c(unittest.TestCase):
    "all tests for lab3b.py"
    '''
    Hardcoded. Used to teach debugging.
    '''
    filename = 'lab3c.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_output(self):
        inputs = ['4\n6\n10\n16\n\n', '13\n7\n6\n1\n\n', '6\n7\n5\n\n']
        expects = [r"The final sum was 36", r"The final sum was 27", r"The final sum was 18"]
        err_msg = (f"Error in {self.filename}: Your script "
                   "should add numbers from the user until the "
                   "user enters a blank input.")
        cmd = [self.pypath, self.filename]
        for i,e in zip(inputs, expects):
            p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            output, error = (n.decode('utf-8') for n in p.communicate(i.encode()))
            if p.returncode != 0:
                logging.error(error)
                raise IOError("Error running the script.")
            self.assertRegex(output, e, err_msg)

class lab3d(unittest.TestCase):
    "all tests for lab3b.py"
    '''
    This is guess a number. Override randint, have students use main().
    '''
    filename = 'lab3d.py'

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


class lab3e(unittest.TestCase):
    "all tests for lab3e.py"
    '''
    Lab3e is a math quiz 2.0. Get numbers, enter solution, test mistakes. Use s to skip.
    '''
    filename = 'lab3e.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_correct_output(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "accepts a correct answer by the user.")
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        try:
            wrong = '0'
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            q = p.stdout.readline().decode('utf-8')
            num_reg = re.compile(r"\d{1,2}")
            nums = [ int(num) for num in num_reg.findall(q) ]
            result = str(sum(nums))
            p.stdin.write(result.encode() + b'\n')
            p.stdin.flush()
            out = p.stdout.readline().decode('utf-8')
            self.assertRegex(out, r'[Cc]orrect', err_msg)
        except (BrokenPipeError):
            pass

        p.stdin.close()
        p.terminate()
        p.wait(timeout=0.2)
    
    def test_incorrect_output(self):
        err_msg = (f"Error in {self.filename}: Make sure that your script "
        "tells the user that an incorrect answer is incorrect.")
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        try:
            wrong = '0'
            p.stdin.write(wrong.encode() + b'\n')
            p.stdin.flush()
            q = p.stdout.readline().decode('utf-8')
            self.assertRegex(q, r'[Ii]ncorrect', err_msg)
        except (BrokenPipeError):
            pass

        p.stdin.close()
        p.terminate()
        p.wait(timeout=0.2)

    def test_skips(self):
        err_msg = (f"Error in {self.filename}: Make sure that "
        "entering 's' will skip tests, and that 0.0% is returned "
        "if all tests are skipped.")
        i = 's\ns\ns\nq\n'
        e = r'\s0.0%'
        p = sp.Popen([sys.executable, self.filename], 
                     stdin=sp.PIPE,
                     stdout=sp.PIPE,
                     stderr=sp.STDOUT)
        output, error = (n for n in p.communicate(i.encode()))
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), e, err_msg)


class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge3.py'

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
    logging.basicConfig(filename="lab3-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab3a, lab3b, lab3c, lab3d, lab3e, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

