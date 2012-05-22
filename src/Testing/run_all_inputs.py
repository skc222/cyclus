#!/usr/bin/python

import sys
import subprocess
import os
import re
 
def main():
    check_inputs()
    path = get_path()
    files = get_files(path)
    for file in files :
        file_to_test = TestFile(file) 
        file_to_test.run_tests()

def check_inputs():
    if len(sys.argv) != 2: 
        print 'Usage: run_all_inputs.py <path_to_Input_folder>' 
        sys.exit(1) 
 
def get_path():
    path = sys.argv[1]
    return path

def get_files(path):
    for root, dirs, files in os.walk(path, followlinks=True):
        if '.git' in dirs:
            dirs.remove('.git')
        for name in files: 
            if re.search("null\.xml",name):
                files.append(os.path.join(root, name))
            else :
                files.remove(name)
    return files

class TestFile():
    """An object representing the inputxml file to test"""
    def __init__(self, file_path):
        self.name = file_path # strip off front bit
  
    def run_tests(self):
        """Runs all of the input file tests"""
        if self.test_no_crash() : 
            output = self.get_output()
            self.test_no_errors(output)
            self.test_expected(output)

    def get_output(self):
        """Returns the output from running the FileTest"""
        flags = " -v9 " + self.name
        try :
            subprocess.check_call(["./cyclus", flags])
        except subprocess.CalledProcessError, e:
            print "native CalledProcessError.output = " + e.output
        output = subprocess.check_output("./cyclus"+flags, stderr=subprocess.STDOUT, shell=True)
        return output
        
    def test_no_errors(self, output):
        """returns true if there were no errors or segfaults running this TestFile"""
        to_ret = True
        if re.search("ERROR",output) or re.search("Segmentation fault",output):
            to_ret = False
            print "Test " + self.name + " resulted in errors: "
            print output
       return to_ret 

   def test_expected(self, output):
       """This function is currently a placeholder. It is intended to print the 
       difference between the current output and the output gathered the last 
       time the test was run"""
       return True

if __name__ == '__main__' : main()
