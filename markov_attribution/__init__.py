"""__init__.py

Main class that does markov chain attribution to your dataset.  

"""
from copy import deepcopy
from .markov_db import MarkovDB

class MarkovAttribution:
    def __init__(self, conversions, separator):
        self.conversions = conversions
        self.separator = separator
        self.db = MarkovDB(conversions,separator)
        self.full_probability = self.db.get_probability('START','CONVERSION')
        self.channels = self.db.get_channels()
        self.channel_probabilities = {}
        cumulative = 0
        total_conversions = 0
        total_value = 0
        for conversion in self.conversions:
            total_conversions += conversion['conversions']
            total_value += conversion['value']
        for channel in self.channels:
            self.channel_probabilities[channel] = self.__removal_effect(channel)
            cumulative += self.channel_probabilities[channel]['effect']
        for channel in self.channels:
            self.channel_probabilities[channel]['weighted'] = self.channel_probabilities[channel]['effect']/cumulative
            self.channel_probabilities[channel]['conversions'] = self.channel_probabilities[channel]['weighted']  * total_conversions
            self.channel_probabilities[channel]['value'] = self.channel_probabilities[channel]['weighted'] * total_value

    def __str__(self):
        return str(self.channel_probabilities)

    def __rm(self,channel):
        newconversions = deepcopy(self.conversions)
        for row in newconversions:
            try:
                orig = row['path']
                row['path'] = row['path'][:row['path'].index(channel)]
                if orig != row['path']:
                    row['conversions'] = 0
                    row['value'] = 0
            except:
                row['path'] = row['path']
        return newconversions

    def __removal_effect(self,channel):
        removal = {}
        removal['conversions'] = self.__rm(channel)
        removal['db'] = MarkovDB(removal['conversions'],self.separator)
        removal['probability'] = removal['db'].get_probability('START','CONVERSION')
        removal['effect'] = 1 - (removal['probability']/self.full_probability)
        return removal

    def get_removal(self,channel):
        return self.channel_probabilities[channel]
    def get_channel_probabilities(self):
        return self.channel_probabilities
