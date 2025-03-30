#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 8
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 8 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 8 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab8a or lab8b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab8-check-output.txt' file.
9. Submit this file along with your scripts: lab8a.py and lab8b.py.

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
import re
from random import randint, choice
import urllib.request as request
import shutil

class lab8a(unittest.TestCase):
    "all tests for lab8a.py"
    '''
    provided to students. regex example for phone numbers.
    import re

    tel_num = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
    mo = tel_num.search('My telephone number is 555-877-5678. Or you can reach me on my cell: 555-212-0771. Call me!')
    print('Found phone number: ' + mo.group())
    '''
    filename = 'lab8a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_module_regex_import(self):
        "lab8a must include the correct regex"
        expected = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
        err_msg = (f"Error: your lab8a does not contain an object called "
                    "tel_num. Make sure to copy code into lab8a"
                    "EXACTLY as how it appears in the lab.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        self.assertEqual(std.tel_num, expected, err_msg)

class lab8b(unittest.TestCase):
    "all tests for lab8b.py"
    '''
    given regex-test.txt, arg specifies file, print number of results, ask if they'd to see. y/n
    '''
    filename = 'lab8b.py'
    testfile = '8bdebug'
    url = "https://ict.senecacollege.ca/~eric.brauer/prg600/labs/regex-test.txt"
    length = 4  # number of results already in file
    expect = []  # used for last test


    def is_downloadable(self, url):
        req = request.urlopen(url)
        header = dict(req.info())
        content_type = header.get("Content-Type")
        if 'text/plain' in content_type.lower():  # we do want text/csv
            return True
        if 'html' in content_type.lower():
            return False
        return False

    def download_test_file(self, url, filepath):
        err_msg = f"{url} is not reachable. Check your network connection and try again. You may also need to connect to the VPN."
        chunk_size = 8192
        self.assertTrue(self.is_downloadable(url), msg=err_msg)
        r = request.urlopen(url)
        with open(filepath, 'wb') as out:
            while True:
                data = r.read(chunk_size)
                if not data:
                    break
                out.write(data)

    def phone_num_gen(self):
        output = ''
        for i in 'ddd-ddd-dddd':
            if i == 'd':
                output += str(randint(0,9))
            else:
                output += i
        return output

    def append_rand_nums(self, filepath):
        with open(filepath, 'a') as f:
            for i in range(randint(0, 4)):
                x = self.phone_num_gen()
                self.expect.append(fr"{x}")
                f.write(x + ' ')
                self.length += 1


    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        self.length = 4  # reset value
        self.expect = []  # reset value
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass
    
    def test_num_results(self):
        "running script on test file should return number of results"
        err_msg = (f"{self.filename}: the file should accept a filename as \n"
                    "arg. Find all matches and print the number of results."
                    "If the user enters 'n', quit the program.\n")
        self.download_test_file(self.url, self.testfile)  # before
        self.append_rand_nums(self.testfile)  # add extra
        cmd = [self.pypath, self.filename, self.testfile]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate('n\n'.encode())  # n to not show results
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), str(self.length), err_msg) 
    
    def test_def_output(self):
        "xx should be one of the results printed when user selects 'y'."
        expect = r"416-922-0621"
        err_msg = (f"{self.filename}: the file should accept a filename as \n"
                    "arg. Find all matches and print the number of results."
                    "If the user enters 'y', show each result on a new line.\n")
        self.download_test_file(self.url, self.testfile)  # before
        self.append_rand_nums(self.testfile)
        cmd = [self.pypath, self.filename, self.testfile]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate('y\n'.encode())  # n to not show results
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), expect, err_msg) 
    
    def test_rand_output(self):
        "xx should be one of the results printed when user selects 'y'."
        err_msg = (f"{self.filename}: the file should accept a filename as \n"
                    "arg. Find all matches and print the number of results."
                    "If the user enters 'y', show each result on a new line.\n")
        self.download_test_file(self.url, self.testfile)  # before
        self.append_rand_nums(self.testfile)
        cmd = [self.pypath, self.filename, self.testfile]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate('y\n'.encode())  # n to not show results
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        for item in self.expect:
            self.assertRegex(output.decode('utf-8'), item, err_msg) 

    def tearDown(self):
        try:
            os.remove(self.testfile)
        except FileNotFoundError:
            pass


class lab8c(unittest.TestCase):
    "all tests for lab8c.py"
    '''
    3 checks: ping, whoami, uptime/systeminfo
    '''

    filename = 'lab8c.py'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_system_ping(self):
        "use os.system to run ping"
        expect = r"= ?os.system\([\'\"]ping"
        err = (f"Error in {self.filename}: Use os.system() to call the ping command. Save the exit code and use it to test.\n")
        with open(self.filename) as f:
            contents = f.read()
        self.assertRegex(contents, expect, err)
    
    def test_popen_whoami(self):
        "use os.popen to run whoami"
        expect = r"= ?os.popen\([\'\"]whoami"
        err = (f"Error in {self.filename}: Use os.popen() to call the whoami command. Save the exit code and use it to test.\n")
        with open(self.filename) as f:
            contents = f.read()
        self.assertRegex(contents, expect, err)


class lab8d(unittest.TestCase):
    "all tests for lab8d.py"
    '''
    os.walk example, but only printing files.
    this literally is all provided to the students, just do basic check
    '''
    filename = 'lab8d.py'
    

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)

    def test_walk_exists(self):
        "use os.walk to find files"
        expect = r"os\.walk"
        err = (f"Error in {self.filename}: Use os.walk() to find files. Re-create the code provided in the lab.\n")
        with open(self.filename) as f:
            contents = f.read()
        self.assertRegex(contents, expect, err)
    
    def test_join_exists(self):
        "use os.path.join to create paths"
        expect = r"os\.path\.join\(root, file"
        err = (f"Error in {self.filename}: Use os.path.join() to join subdirectories with files. Re-create the code provided in the lab.\n")
        with open(self.filename) as f:
            contents = f.read()
        self.assertRegex(contents, expect, err)


class lab8e(unittest.TestCase):
    "all tests for lab8e.py"
    '''
    os.walk example, backing files up.
    '''
    filename = 'lab8e.py'
    target = '8etree'
    expect = set() 
    
    def randofile(self):
        names = ('file', 'program', 'banana')
        suffixes = ('.py', '.py', '.txt', '.py.txt', '')
        out = f"{choice(names)}{randint(0,9)}{choice(suffixes)}"
        if out.endswith('.py'):
            self.expect.add(out)
        return out

    def randotouch(self, filename):
        with open(filename, 'w') as f:
            f.write('')

    def randotree(self):
        dirnames = ['test', 'example', 'raw', 'resource', 'assets', 'local']
        target = os.path.join(os.getcwd(), self.target)
        if os.path.isdir(target):
            shutil.rmtree(target)
        os.mkdir(target)
        for _ in range(1, 3):
            subd = choice(dirnames)
            try:
                os.mkdir(os.path.join(target, subd))
            except FileExistsError:
                pass
            for _ in range(1,3):
                self.randotouch(os.path.join(target, subd, self.randofile()))
        for _ in range(2,5):
            self.randotouch(os.path.join(target, self.randofile()))



    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        self.expect = set()  # set to ignore dupes
        self.randotree()
        

    def test_not_a_dir(self):
        "ERROR: printed when directory doesn't exist"
        cmd = [self.pypath, self.filename, 'bloop']
        expect = r"(?i)error:"
        err_msg = (f"\nError in {self.filename}:\n"
                f"If an invalid directory is passed, catch\n"
                "the exception and print an error message.\n"
                f"For example:\n"
                f"ERROR: Not a valid directory.")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        self.assertRegex(output.decode('utf-8'), expect, err_msg)

    def test_create_backup(self):
        "backups directory exists after execution"
        cmd = [self.pypath, self.filename, self.target]
        err_msg = (f"\nError in {self.filename}:\n"
                f"If a valid directory is passed, create\n"
                "'backups' as a subdirectory of that directory.\n")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        if error:
            err_msg += error.decode('utf-8')
        exp = os.path.join(self.target, 'backups')
        self.assertTrue(os.path.isdir(exp), msg=err_msg)

    def test_files_copied(self):
        "backups directory contains only python files"
        cmd = [self.pypath, self.filename, self.target]
        err_msg = (f"\nError in {self.filename}:\n"
                f"If a valid directory is passed, create\n"
                "'backups' as a subdirectory of that directory.\n"
                "Then, copy each valid Python file into that directory. You must recursively search each subdirectory.")
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate()
        self.assertFalse(error, "Your code must run without errors.")
        exp = os.path.join(self.target, 'backups')
        for root, dirs, fs in os.walk(exp):
            for f in fs:
                self.assertIn(f, self.expect, err_msg)
                self.expect.remove(f)
            self.assertFalse(self.expect, err_msg)
            for d in dirs:
                self.assertIsNone(d, err_msg)



    def tearDown(self):
        try:
            shutil.rmtree(self.target)
        except FileNotFoundError:
            pass


def ChecksumLocal(filename=None):
    fil = open(filename, 'r', encoding='utf-8')
    dat = fil.readlines()
    textdata = ''
    for line in dat:
        textdata = textdata + line
    checksum = hashlib.md5(textdata.encode('utf-8')).hexdigest()  # hexdigest for a string
    return checksum

if __name__ == '__main__':
    logging.basicConfig(filename="lab8-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info(f"{sys.argv[0]} {ChecksumLocal(sys.argv[0])}")
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab8a, lab8b, lab8c, lab8d, lab8e:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

