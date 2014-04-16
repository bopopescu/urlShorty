###
# Runs Python Unit Test against db_functions.py
# 
#
##/

import unittest 
from db_functions import *

class dbUnitTests(unittest.TestCase):

    def test_shoudPrintSimpleMessage(self):
        print "Running db_functions.py Unit Tests"
        self.assertEqual(0, 0)
        
    def test_shouldPrintUserAlreadyExistsUser007AndPasszebracake(self):    	
        print "Running Test: test_shouldPrintUserAlreadyExistsUser007AndPasszebracake"
        self.assertEqual('User already exist', addUser('USER007', 'zebracake'))
        
if __name__ == '__main__':
  unittest.main()