"""Markov.py

Does Markov Chain multi-channel attribution on your dataset.

"""
from markov_attribution import MarkovAttribution

test_data = [
  {'conversions': 1, 'value': 1000.00, 'path': 'C1 > C2 > C3'},
  {'conversions': 0, 'value': 0, 'path': 'C1'},
  {'conversions': 0, 'value': 0, 'path': 'C2 > C3'},
]

sep = ' > '
marka = MarkovAttribution(test_data, sep)
print(marka.get_removal('C1'))
print(marka.get_channel_probabilities())
