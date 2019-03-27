"""__init__.py

Main class that does markov chain attribution to your dataset.

"""
from numpy import matrix, identity, subtract, matmul
from numpy.linalg import inv
from itertools import islice
from copy import deepcopy
from pprint import pprint

class MarkovMatrix:
    def __init__(self, matrix_arr):
        self.matrix_obj = matrix(matrix_arr)
        self.rows = self.matrix_obj.shape[0]
        self.cols = self.matrix_obj.shape[1]
        self.size = self.rows
        self.status = self.__is_stochastic()
        self.absorption_states = self.__get_absorption_states()
        self.q = self.__get_q()
        self.r = self.__get_r()
        self.i = self.__get_i()
        self.zero = self.__get_0()
        self.n = self.__get_n()
        self.m = self.__get_m()

    def __str__(self):
        return """\nmatrix: {0}\nrows: {1}\ncols: {2}\n
        size: {3}\nstatus: {4}\nabsorption_states: {5}\nm: {6}""".format(
            self.matrix_obj, self.rows, self.cols, self.size, self.status,
            self.absorption_states, self.m
        )

    def __is_stochastic(self):
        result = (
            True
            and self.rows == self.cols
        )
        if not result:
            raise Exception(
                'This is not a stochastic matrix.  Rows should == Columns.'
            )
        else:
            return result

    def __get_absorption_states(self):
        if self.status:
            num_absorption_states = 0
            ridx = 0
            for row in self.matrix_obj:
                absorption = True
                cidx = 0
                for col in self.matrix_obj:
                    value = self.matrix_obj.item(ridx, cidx)
                    if value not in [1, 0]:
                        absorption = False
                    elif ridx == cidx and value != 1:
                        absorption = False
                    elif ridx != cidx and value == 1:
                        absorption = False
                    cidx += 1
                if absorption:
                    num_absorption_states += 1
                ridx += 1
            return num_absorption_states

    def __get_q(self):
        if self.status:
            max = self.rows - self.absorption_states
            values = []
            for i in range(0, max):
                row = []
                for j in range(0, max):
                    row.append(self.matrix_obj.item(i, j))
                    j += 1
                values.append(row)
                i += 1
            return matrix(values)

    def __get_r(self):
        if self.status:
            rows = self.rows
            cols = self.cols
            astates = self.absorption_states
            rcols = astates
            rrows = rows - astates
            start = cols - astates
            values = []
            for i in range(0, rrows):
                row = []
                for j in range(start, cols):
                    row.append(self.matrix_obj.item(i, j))
                    j += 1
                values.append(row)
                i += 1

            return matrix(values)

    def __get_i(self):
        if self.status:
            rows = self.rows
            cols = self.cols
            astates = self.absorption_states
            start = cols - astates
            values = []
            for i in range(start, rows):
                row = []
                for j in range(start, cols):
                    item = self.matrix_obj.item(i, j)
                    if item != 1 and item != 0:
                        raise Exception("""This is not a stochastic matrix.  I
                        sub matrix should contain only 1s and 0s""")
                    else:
                        row.append(self.matrix_obj.item(i, j))
                    j += 1
                values.append(row)
                i += 1
            return matrix(values)

    def __get_0(self):
        if self.status:
            rows = self.rows
            cols = self.cols
            astates = self.absorption_states
            zrows = astates
            zcols = rows - astates
            start = rows - astates
            values = []
            for i in range(start, rows):
                row = []
                for j in range(0, zcols):
                    item = self.matrix_obj.item(i, j)
                    if item != 0:
                        raise Exception("""This is not a stochastic matrix.
                        Zero sub matrix should contain only 0s""")
                    else:
                        row.append(self.matrix_obj.item(i, j))
                    j += 1
                values.append(row)
                i += 1
            return matrix(values)

    def __get_n(self):
        if self.status:
            it = identity(self.q.shape[0])
            pre_n = subtract(it, self.q)
            return inv(pre_n)

    def __get_m(self):
        if self.status:
            return matmul(self.n, self.r)

    def get_absorption_states(self):
        if self.status:
            return self.absorption_states

    def get_probability(self, start_state_index, end_state_index):
        if self.status:
            return self.m.item(start_state_index, end_state_index)


class MarkovDB:
    def __init__(self, conversions, separator):
        self.conversions = conversions
        self.separator = separator
        self.keys = self.__get_keys()
        self.channels = self.__get_channels()
        self.db = self.__get_db()
        self.matrix = self.__get_prob_matrix()

    def __str__(self):
        return """conversions: {0}\nseparator: {1}\nkeys: {2}\nchannels: {3}
            db: {4}\nmatrix: {5}""".format(
                self.conversions, self.separator, self.keys,
                self.channels, self.db, self.matrix
            )

    def __get_keys(self):
        return ['START'] + sorted(list(self.__get_channels())) + ['NULL', 'CONVERSION']

    def __get_channels(self):
        keys = set()
        for row in self.conversions:
            rstates = row['path'].split(self.separator)
            for state in rstates:
                if state != "" and state not in keys:
                    keys.add(state)
        try:
            keys.remove('NULL')
            return sorted(list(keys))
        except:
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
                except Exception:
                    states[key] = 1
        transitions = 0
        totals = {}
        for key in states:
            sstate = key.split(self.separator)[0]
            estate = key.split(self.separator)[1]
            transitions += states[key]
            try:
                db[sstate][estate] += states[key]
            except Exception:
                try:
                    db[sstate][estate] = states[key]
                    totals[sstate] += states[key]
                except Exception:
                    db[sstate] = {}
                    db[sstate][estate] = states[key]
                    totals[sstate] = states[key]
        for key in db:
            for rkey in db[key]:
                db[key][rkey] = db[key][rkey]/totals[key]
        db['NULL'] = {}
        db['NULL']['NULL'] = 1
        db['CONVERSION'] = {}
        db['CONVERSION']['CONVERSION'] = 1
        db['DELME'] = {}
        del db['DELME']
        #pprint(db)
        return db

    def __get_prob_matrix(self):
        states = self.keys
        #print('KEYSS',self.keys)
        data = []
        for rkey in states:
            row = []
            for ckey in states:
                try:
                    row.append(self.db[rkey][ckey])
                except Exception:
                    row.append(0)
            data.append(row)
        #pprint(data)
        return MarkovMatrix(data)

    def get_probability(self, start, end):
        start_idx = self.keys.index(start)
        end_idx = self.keys.index(end) - len(self.channels) - 1
        return self.matrix.get_probability(start_idx, end_idx)

    def get_channels(self):
        return self.channels

    def get_keys(self):
        return self.keys


class MarkovAttribution:
    def __init__(self, conversions, separator):
        self.conversions = conversions
        self.separator = separator
        self.db = MarkovDB(conversions, separator)
        self.full_probability = self.db.get_probability('START', 'CONVERSION')
        self.channels = self.db.get_channels()
        self.cprobs = {}
        cumulative = 0
        total_conversions = 0
        total_value = 0
        for conversion in self.conversions:
            total_conversions += conversion['conversions']
            total_value += conversion['value']
        for channel in self.channels:
            self.cprobs[channel] = self.__removal_effect(channel)
            cumulative += self.cprobs[channel]['effect']
        for channel in self.channels:
            self.cprobs[channel]['weighted'] = (
                self.cprobs[channel]['effect'] / cumulative
            )
            self.cprobs[channel]['conversions'] = (
                self.cprobs[channel]['weighted'] * total_conversions
            )
            self.cprobs[channel]['value'] = (
                self.cprobs[channel]['weighted'] * total_value
            )

    def __str__(self):
        return str(self.cprobs)

    def __rm(self, channel):
        newconversions = deepcopy(self.conversions)
        for row in newconversions:
            try:
                orig = row['path']
                row['path'] = row['path'].replace(channel, 'NULL')
            except Exception:
                row['path'] = row['path']
        return newconversions

    def __removal_effect(self, channel):
        removal = {}
        removal['conversions'] = self.__rm(channel)
        removal['db'] = MarkovDB(removal['conversions'], self.separator)
        removal['probability'] = (
            removal['db'].get_probability('START', 'CONVERSION')
        )
        #pprint(removal)
        if self.full_probability == 0:
            removal['effect'] = 0
        else:
            removal['effect'] = 1 - (removal['probability']/self.full_probability)
        return removal

    def get_removal(self, channel):
        return self.cprobs[channel]

    def get_channel_probabilities(self):
        return self.cprobs
