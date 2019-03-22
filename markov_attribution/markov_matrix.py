"""markov_matrix.py

Additional stochastic functions not included in numpy that are required for Markov math.  

"""
from numpy import matrix, identity, subtract, matmul
from numpy.linalg import inv

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
        return """
matrix: {0}
rows: {1}
cols: {2}
size: {3}
status: {4}
absorption_states: {5}
m: {6}
        """.format(self.matrix_obj, self.rows, self.cols, self.size, self.status, self.absorption_states, self.m)

    def __is_stochastic(self):
        result = (
            True
            and self.rows == self.cols
        )
        if not result:
            raise Exception('This is not a stochastic matrix.  Rows should == Columns.')
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
                    value = self.matrix_obj.item(ridx,cidx)
                    if value not in [1,0]:
                        absorption = False
                    elif ridx == cidx and value != 1:
                        absorption = False
                    elif ridx != cidx and value == 1:
                        absorption = False
                    cidx += 1
                if absorption:
                    num_absorption_states+= 1
                ridx += 1
            return num_absorption_states

    def __get_q(self):
        if self.status:
            max = self.rows - self.absorption_states
            values = []
            for i in range(0,max):
                row = []
                for j in range(0,max):
                    row.append(self.matrix_obj.item(i,j))
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
            for i in range(0,rrows):
                row = []
                for j in range(start,cols):
                    row.append(self.matrix_obj.item(i,j))
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
            for i in range(start,rows):
                row = []
                for j in range(start,cols):
                    item = self.matrix_obj.item(i,j)
                    if item != 1 and item != 0:
                        raise Exception('This is not a stochastic matrix.  I sub matrix should contain only 1s and 0s')
                    else:
                        row.append(self.matrix_obj.item(i,j))
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
            for i in range(start,rows):
                row = []
                for j in range(0,zcols):
                    item = self.matrix_obj.item(i,j)
                    if item != 0:
                        raise Exception('This is not a stochastic matrix.  Zero sub matrix should contain only 0s')
                    else:
                        row.append(self.matrix_obj.item(i,j))
                    j += 1
                values.append(row)
                i += 1
            return matrix(values)

    def __get_n(self):
        if self.status:
            it = identity(self.q.shape[0])
            pre_n = subtract(it,self.q)
            return inv(pre_n)

    def __get_m(self):
        if self.status:
            return matmul(self.n,self.r)

    def get_absorption_states(self):
        if self.status:
            return self.absorption_states
    def get_probability(self,start_state_index, end_state_index):
        if self.status:
            return self.m.item(start_state_index,end_state_index)
