from unittest import TestCase
from numpy import matrix, array_equal, allclose
from markov_attribution import MarkovDB

test_data = [
  {'conversions': 1, 'value': 1000.00, 'path': 'C1 > C2 > C3'},
  {'conversions': 0, 'value': 0, 'path': 'C1'},
  {'conversions': 0, 'value': 0, 'path': 'C2 > C3'},
]

sep = ' > '


class TestMarkovDB(TestCase):

    def test_keys(self):
        comp = ['START', 'C1', 'C2', 'C3', 'NULL', 'CONVERSION']
        test_db = MarkovDB(test_data, sep)
        test = test_db.keys
        self.assertTrue(array_equal(comp, test))

    def test_channels(self):
        comp = ['C1', 'C2', 'C3']
        test_db = MarkovDB(test_data, sep)
        test = test_db.channels
        self.assertTrue(array_equal(comp, test))

    def test_db(self):
        comp = {
            'C1': {
                'C2': 1/2,
                'NULL': 1/2
            },
            'C2': {
                'C3': 1
            },
            'C3': {
                'CONVERSION': 1/2,
                'NULL': 1/2
            },
            'CONVERSION': {
                'CONVERSION': 1
            },
            'NULL': {
                'NULL': 1
            },
            'START': {
                'C1': 2/3,
                'C2': 1/3
            }
        }
        test_db = MarkovDB(test_data, sep)
        test = test_db.db
        self.assertTrue(comp == test)

    def test_probability(self):
        test_db = MarkovDB(test_data, sep)
        test = test_db.get_probability('START', 'CONVERSION')
        comp = 33
        self.assertTrue(comp == round(test*100))
