#!/usr/bin/env python3

'''
Check script for Winter 2022

Lab 7
Author: Eric Brauer
Date: January 2022

Usage: 
1. Place this file in the same directory as your Lab 7 files.
2. Open VSCode. From 'File', select "Open Folder". Find your Lab 7 folder.
3. If VSCode opens the folder in "Restricted Mode", make sure to enable execution of scripts by selecting "Trust" for this workspace.
3a. For more information, refer to this video: https://youtu.be/1nePPW6Xx7A
4. Open the check script inside VSCode by double-clicking it from the file explorer on the left.
5. Click inside this script, but do not change the code. Press Ctrl+Shift+D to enter "Run and Debug" mode.
6. Click the "Run and Debug" button. Select "Python" from the drop-down menu.
7. In the bottom terminal, you will see output from the check script. Use the messages to solve any problems inside lab7a or lab7b.
8. Once all errors have been resolved, you will notice that the check script has created a 'lab7-check-output.txt' file.
9. Submit this file along with your scripts: lab7a.py and lab7b.py.

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
from random import shuffle, choice
from unittest.mock import patch
import io
# import requests
import urllib.request as request
from difflib import SequenceMatcher as sm

class lab7a(unittest.TestCase):
    "all tests for lab7a.py"
    '''
    student1 + shipping_label
    '''
    filename = 'lab7a.py'  # necessary for main loop to print
    
    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
    
    def test_module_dict_import(self):
        "lab7a must include the correct dictionary"
        expected = {'first_name': 'eric', 'last_name':'smith', 'addr1': '217 Au Large Blvd', 'city': 'Toronto', 'prov': 'Ontario', 'pcode': 'M4A 1P3'}
        err_msg = (f"Error: your lab7a does not contain a student1 dictionary"
                    "Make sure to copy it into lab7a"
                    "EXACTLY as how it appears in the lab.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        self.assertEqual(std.student1, expected, err_msg)
    
    def test_module_func_import(self):
        "lab7a must include the correct function"
        test_in = {'first_name': 'pam', 'last_name':'anders', 'addr1': '99 Maple St.', 'city': 'Kitchener', 'prov': 'Ontario', 'pcode': 'N1P 7J4'}
        expected = ("Pam Anders\n99 Maple St.\nKitchener, Ontario\nN1P 7J4")
        err_msg = (f"Error: your lab7a does not contain a shipping_label function\n"
                    "or it isn't returning the correct string."
                    "Reproduce the output EXACTLY as it appears in the lab.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        self.assertEqual(std.shipping_label(test_in), expected, err_msg)


class lab7b(unittest.TestCase):
    "all tests for lab7b.py"
    '''
    Print a menu using f-strings, 50 width
    '''
    filename = 'lab7b.py'
    inputd = dict()

    def shuffle(self):
        lst = ['pizza', 'tofu', 'biryani', 'bibimbap', 'soup']
        self.inputd['breakfast'] = choice(lst)  # new order each time
        self.inputd['lunch'] = choice(lst)
        self.inputd['dinner'] = choice(lst)

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        self.shuffle()

    def test_header_line(self):
        "use == to divide Title from Menu"
        expected = r"(?m)^\={50}\r?$"  # needs to be multiline for anchors to work! TIL
        err_msg = (f"Error in {self.filename}: no function named\n"
            "'print_meal_plan' was found, or it did not print a \n"
            "header bar composed of 50 equal signs.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            std.print_meal_plan(std.meal_plan)
        self.assertRegex(fake_stdout.getvalue(), expected, err_msg)

    def test_menu_breakfast(self):
        "Print the meals passed in as arg with correct spacing"
        expect = r"(?m)"
        bsl = 50 - len("Breakfast") - len(self.inputd['breakfast'])
        expect += r"^Breakfast {" + str(bsl) + "}" + self.inputd['breakfast'] + "\r?$"
        err_msg = (f"Error in {self.filename}: no function named\n"
            "'print_meal_plan' was found, or it did not print the\n"
            "meals specified in the dictionary passed in.\n"
            "Make sure that you are printing from the parameter dictionary.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            std.print_meal_plan(self.inputd)
        self.assertRegex(fake_stdout.getvalue(), expect, err_msg)
    
    def test_menu_lunch(self):
        "Print the meals passed in as arg with correct spacing"
        expect = r"(?m)"
        bsl = 50 - len("Lunch") - len(self.inputd['lunch'])
        expect += r"^Lunch {" + str(bsl) + "}" + self.inputd['lunch'] + "\r?$"
        err_msg = (f"Error in {self.filename}: no function named\n"
            "'print_meal_plan' was found, or it did not print the\n"
            "meals specified in the dictionary passed in.\n"
            "Make sure that you are printing from the parameter dictionary.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            std.print_meal_plan(self.inputd)
        self.assertRegex(fake_stdout.getvalue(), expect, err_msg)
    
    def test_menu_dinner(self):
        "Print the meals passed in as arg with correct spacing"
        expect = r"(?m)"
        bsl = 50 - len("Dinner") - len(self.inputd['dinner'])
        expect += r"^Dinner {" + str(bsl) + "}" + self.inputd['dinner'] + "\r?$"
        err_msg = (f"Error in {self.filename}: no function named\n"
            "'print_meal_plan' was found, or it did not print the\n"
            "meals specified in the dictionary passed in.\n"
            "Make sure that you are printing from the parameter dictionary.")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            std.print_meal_plan(self.inputd)
        self.assertRegex(fake_stdout.getvalue(), expect, err_msg)


class lab7c(unittest.TestCase):
    "all tests for lab7c.py"
    '''
    Use input() to add meal plans to a list.
    '''

    filename = 'lab7c.py'
    inp = ""  # for user prompt
    exp = r"(?m)Breakfast {39}"  # 50 - len(breakfast) - 2 = 39
    num_d_reg = r"\(1-"
    
    def shuffle(self):
        letters = 'abcdefg'
        lst = [x+y for x in letters for y in letters]
        num_of_days = choice(range(2, 6))  # at least 2, up to 5
        self.num_d_reg += str(num_of_days) + '\)'  # used to check (1-4)
        day_to_choose = choice(range(1, num_of_days))  # should not be last ever
        for i in range(1, num_of_days+1):
            self.inp += 'y\n'
            br = choice(lst)
            ln = choice(lst)
            dn = choice(lst)
            self.inp += br + '\n'
            self.inp += ln + '\n'
            self.inp += dn + '\n'
            if i == day_to_choose:
                self.exp += br + '\r?\nLunch {43}'
                self.exp += ln + '\r?\nDinner {42}'
                self.exp += dn + '\r?\n'
        self.inp += 'n\n' + str(day_to_choose) + '\n'

    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        self.shuffle()
    
    def test_module_dict_template(self):
        "lab7a must include an empty template dictionary"
        expected = {'breakfast': None, 'lunch': None, 'dinner': None}
        err_msg = (f"Error: your {self.filename} does not contain a dictionary"
                    "called template. Make sure that you created template outside the main block.\n"
                    "I expected: {expected}")
        try:
            std = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print(err_msg)
        self.assertEqual(std.template, expected, err_msg)

    def test_7b_import(self):
        "import function from lab7b"
        expect = 'from lab7b import print_meal_plan'
        err = (f"Error in {self.filename}: not importing from lab7b.\n"
               f"I expected: {expect}.")
        with open(self.filename) as f:
            contents = f.read()
        self.assertIn(expect, contents, err)
    
    def test_dict_copy(self):
        "use copy on template"
        expect = 'template.copy()'
        err = (f"Error in {self.filename}: not creating a copy of template.\n"
               f"I expected: {expect}.")
        with open(self.filename) as f:
            contents = f.read()
        self.assertIn(expect, contents, err)

    def test_list_range(self):
        "print the correct range of days (1-x)"
        input = self.inp
        err_msg = (f"Error in {self.filename}: Your script should use "
                   "len() to get the length of the days list and \n"
                   "present the user with an option. For example: \n"
                   "if the list has three items, present a range of (1-3)")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate(input.encode())
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), self.num_d_reg, err_msg)

    def test_meal_output(self):
        "print the menu for the correct list item"
        input = self.inp
        err_msg = (f"Error in {self.filename}: Your script should use "
                   "print_meal_plan for the item selected by the user \n")
        cmd = [self.pypath, self.filename]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        output, error = p.communicate(input.encode())
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        self.assertRegex(output.decode('utf-8'), self.exp, err_msg)

class lab7d(unittest.TestCase):
    "all tests for lab7d.py"
    '''
    CSV file: change test1.csv name and addresses
    Steps:
    1. Download the test input
    2. Download the test output
    3. Compare the two files, if within spec, it's a pass.
    
    '''
    filename = 'lab7d.py'
    testfile = '7ddebug.csv'
    testfile_out = '7ddebugo.csv'
    exp_sum = r""  # the expected printed sums of each line
    exp_out = r""  # expected contents of the file
    url1 = "https://ict.senecacollege.ca/~eric.brauer/prg600/labs/test1.csv"
    url1o = "https://ict.senecacollege.ca/~eric.brauer/prg600/labs/test1-output.csv"
    url2 = "https://ict.senecacollege.ca/~eric.brauer/prg600/labs/test2.csv"
    url2o = "https://ict.senecacollege.ca/~eric.brauer/prg600/labs/test2-output.csv"
    
    def is_downloadable(self, url):
        req = request.urlopen(url)
        header = dict(req.info())
        content_type = header.get("Content-Type")
        if 'text/csv' in content_type.lower():  # we do want text/csv
            return True
        if 'html' in content_type.lower():
            return False
        return False

    # def is_downloadable(self, url):
    #     h = requests.head(url, allow_redirects=True)
    #     header = h.headers
    #     content_type = header.get('content-type')
    #     if 'text/csv' in content_type.lower():  # we do want text/csv
    #         return True
    #     if 'html' in content_type.lower():
    #         return False
    #     return False

    def download_test_csv(self, url, filepath):
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

    # def download_test_csv(self, url, filepath):
    #     err_msg = f"{url} is not reachable. Check your network connection and try again. You may also need to connect to the VPN."
    #     self.assertTrue(self.is_downloadable(url), msg=err_msg)
    #     r = requests.get(url, allow_redirects=True)
    #     open(filepath, 'wb').write(r.content)

    def compare_two_files(self, f1, f2):
        "new for nov 2021: file comparison using difflib approach"
        if f1 != f2:
            with open(f1) as file1:
                c1 = file1.read()
            with open(f2) as file2:
                c2 = file2.read()
            m = sm(None, c1, c2)
            return m.ratio()
        return 0


    def setUp(self):
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        self.pypath = sys.executable
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        for file in self.testfile, self.testfile_out:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    def test_test1(self):
        "running script on test1 should result in the appropriate changes"
        err_msg = (f"{self.filename}: the CSV file you are modifying doesn't\n"
                    "match what's expected. Make sure you are making all necessary changes,\n"
                    "and that you are using a single command line argument to specify \n"
                    "the file being read and written to.")
        self.download_test_csv(self.url1, self.testfile)  # before
        self.download_test_csv(self.url1o, self.testfile_out)  # what a success should look like
        cmd = [self.pypath, self.filename, self.testfile]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        _, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        ratio = self.compare_two_files(self.testfile, self.testfile_out)
        self.assertGreaterEqual(ratio, 0.99, err_msg)  # files should match at least 99% 

    def test_test2(self):
        "running script on test1 should result in the appropriate changes"
        err_msg = (f"{self.filename}: the CSV file you are modifying doesn't\n"
                    "match what's expected. Make sure you are making all necessary changes,\n"
                    "and that you are using a single command line argument to specify \n"
                    "the file being read and written to.")
        self.download_test_csv(self.url2, self.testfile)  # before
        self.download_test_csv(self.url2o, self.testfile_out)  # what a success should look like
        cmd = [self.pypath, self.filename, self.testfile]
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        _, error = p.communicate()
        if p.returncode != 0:
            logging.error(error.decode('utf-8'))
            raise IOError("Error running the script.")
        ratio = self.compare_two_files(self.testfile, self.testfile_out)
        self.assertGreaterEqual(ratio, 0.99, err_msg)  # files should match at least 99.%
 
    def tearDown(self):
        for file in self.testfile, self.testfile_out:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass


class challenge(unittest.TestCase):
    "test if challenge file exists"

    filename = 'challenge7.py'

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
    logging.basicConfig(filename="lab7-check-output.txt", level=logging.DEBUG, filemode='w')
    logging.info(f"{sys.argv[0]} {ChecksumLocal(sys.argv[0])}")
    logging.info('logging test')
    logging.info(f"Test Run: {datetime.datetime.now()}")
    runner = unittest.TextTestRunner(failfast=True)
    for case in lab7a, lab7b, lab7c, lab7d, challenge:
        print(f"Testing {case.filename}...")
        loader = unittest.TestLoader().loadTestsFromTestCase(case)
        result = runner.run(loader)
        if result.wasSuccessful():
            logging.info(f"{case.filename}: test successful.")
            logging.info(f"{case.filename} {ChecksumLocal(case.filename)}")
        else:
            logging.warning(f"{case.filename}: Failures encountered.")
        logging.info('done.')

