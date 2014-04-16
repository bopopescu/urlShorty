###
# Runs Python Unit Test against db_functions.py
# 
#
##/

import unittest 
from db_functions import *

class dbUnitTests(unittest.TestCase):
	def testAddShortUrlQueryShouldReturnNotavailableWithFooddotcom(self):
		# print "Running Test: test_AddShortUrlQueryShouldReturnNotavailableWithFooddotcom"
		self.assertEqual('Not available', addShortURLQuery('food', 'http://food.com', 'fanman'))

    # def test_shouldPrintSimpleMessage(self):
        # # print "Running Test db_functions.py Unit Tests\n"
        # self.assertEqual(0, 0)
        
    # def test_AddUsershouldReturnUserAlreadyExistsUser007AndPasszebracake(self):    	
        # # print "Running Test: test_shouldPrintUserAlreadyExistsUser007AndPasszebracake\n"
        # self.assertEqual('User already exist', addUser('USER007', 'zebracake'))

	def test_UserValidateshouldReturnFalsewithUSER00w7(self):    	
        # print "Running Test: test_UserValidateshouldPrintFalsewithUSER00w7\n"
		self.assertFalse(userValidate('USER00w7'))
        
	def test_PasswordValidateshouldReturnIt_MatcheswithUSER007andZebraCake(self):
        # print "Running Test: test_PasswordValidateshouldReturnIt_MatcheswithUSER007andZebraCake\n"
		self.assertEqual('It matches', passwordValidate('USER007', 'zebracake'))

	def test_PasswordValidateshouldReturnUserdoesntExistwithUSER008andZebraCake(self):
        # print "Running Test: test_PasswordValidateshouldReturnIt_MatcheswithUSER007andZebraCake\n"
		self.assertEqual('User doesn\'t exist', passwordValidate('USER008', 'zebracake'))
		

		
if __name__ == '__main__':
	# unittest.main()
	suite = unittest.TestLoader().loadTestsFromTestCase(dbUnitTests)
	unittest.TextTestRunner(verbosity=2).run(suite)