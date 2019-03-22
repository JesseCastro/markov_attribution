"""markov_db.py

Bespoke object for storing conversions and probabilities for the markov chain procedures.  

"""
from itertools import islice
from .markov_matrix import MarkovMatrix
class MarkovDB:
    def __init__(self, conversions, separator):
        self.conversions = conversions
        self.separator = separator
        self.keys = self.__get_keys()
        self.channels = self.__get_channels()
        self.db = self.__get_db()
        self.matrix = self.__get_prob_matrix()

    def __str__(self):
        return """
conversions: {0}
separator: {1}
keys: {2}
channels: {3}
db: {4}
matrix: {5}
""".format(self.conversions,self.separator, self.keys, self.channels, self.db, self.matrix)

    def __get_keys(self):
        keys = set()
        for row in self.conversions:
            rstates = row['path'].split(self.separator)
            for state in rstates:
                if state != "":
                    keys.add(state)
        return ['START'] + sorted(list(keys)) + ['NULL', 'CONVERSION']

    def __get_channels(self):
        keys = set()
        for row in self.conversions:
            rstates = row['path'].split(self.separator)
            for state in rstates:
                if state != "":
                    keys.add(state)
        return sorted(list(keys))

    def __get_db(self):
        states = {}
        db = {}
        for row in self.conversions:
            rstates = row['path'].split(self.separator)
            rstates = ['START'] + rstates
            if row['conversions'] > 0:
                rstates = rstates + ['CONVERSION']
            else:
                rstates = rstates + ['NULL']
            for i in range(len(rstates) - 1):
                key = rstates[i] + self.separator + rstates[i + 1]
                try:
                    states[key] += 1
                except:
                    states[key] = 1
        transitions = 0
        for key in states:
            sstate = key.split(self.separator)[0]
            estate = key.split(self.separator)[1]
            transitions += states[key]
            try:
                db[sstate][estate] += states[key]
            except:
                try:
                    db[sstate][estate] = states[key]
                except:
                    db[sstate] = {}
                    db[sstate][estate] = states[key]
        for key in db:
            for rkey in db[key]:
                db[key][rkey] = db[key][rkey]/transitions
        #don't forget the absorption states!
        db['NULL'] = {}
        db['NULL']['NULL'] = 1
        db['CONVERSION'] = {}
        db['CONVERSION']['CONVERSION'] = 1

        return db

    def __get_prob_matrix(self):
        states = self.keys
        data = []
        for rkey in states:
            row = []
            for ckey in states:
                try:
                    row.append(round(self.db[rkey][ckey],2))
                except:
                    row.append(0)
            data.append(row)
        return MarkovMatrix(data)

    def get_probability(self,start,end):
        start_idx = self.keys.index(start)
        end_idx = self.keys.index(end) - len(self.channels) - 1
        return self.matrix.get_probability(start_idx, end_idx)

    def get_channels(self):
        return self.channels

    def get_keys(self):
        return self.keys
