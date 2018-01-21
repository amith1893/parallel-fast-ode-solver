import sys
import random
import math
from ParameterEstimator import ParameterEstimator
from AdaptiveSolver import AdaptiveSolver
from OdeSolver import OdeSolver

class FastOde():
    def __init__(self, num_var, num_iter, init_val, expected_ratio):
        self.num_var  = num_var
        self.num_iter = num_iter
        self.init_val = init_val
        self.pe = ParameterEstimator()
        self.ads = AdaptiveSolver()
        self.os = OdeSolver()
        self.parameter_matrix = []
        self.parameter_dict = {}
        self.probability_distributions = ["normal", "lognormal", "exponential"]
        self.lower_expected_ratio = expected_ratio - 0.2
        self.higher_expected_ratio = expected_ratio + 0.2
    def __get_parameters(self):
        max_rand_range = len(self.probability_distributions) - 1
        min_rand_range = 0

        for num in range(0, self.num_var):
            rand_dist = random.randint(min_rand_range, max_rand_range)
            self.parameter_matrix.append(self.pe.get_distribution(self.probability_distributions[rand_dist], 10))

    def solve(self):
        
        self.__get_parameters()
        step_sizes = self.ads.get_step_size(2)
        
        #Prepare the parameter-list to send to ODE-Solver
        #Get the step size from Adaptive Solver
        '''
            for each parameter combination in the parameter list
                Try different step sizes until the ratio between the outputs for the 2 consecutive different step sizes (ie. alpha)
        '''
        
        result_dict = {}
        result_flag = {}
        for i in range(0, 10):
            print "\n"
            curr_parameter_set = []
            for j in range(0, self.num_var):
                curr_parameter_set.append(self.parameter_matrix[j][i])
            
            self.parameter_dict[i] = curr_parameter_set
            result_dict[i] = []
            result_flag[i] = 0
            for step in step_sizes:
                res = self.os.forward_euler_solver(curr_parameter_set, step, self.num_iter, self.init_val)
                result_dict[i].append(res)

            last_res = result_dict[i][0]
            for j in range(1, len(result_dict[i])):
                res = result_dict[i][j]
                if math.isinf(last_res) and math.isinf(res):
                    ratio = float("inf")
                elif math.isinf(last_res) and not math.isinf(res):
                    ratio = 0
                elif not math.isinf(last_res) and math.isinf(res):
                    ratio = float("inf")
                elif not math.isinf(last_res) and not math.isinf(res) and (last_res == 0):
                    ratio = float("inf")
                else:
                    ratio = ((res-last_res)*1.0)/last_res
               
                #print ratio
                if not math.isinf(ratio):
                    if abs(ratio) >= self.lower_expected_ratio and abs(ratio) <= self.higher_expected_ratio:
                        result_flag[i] = step_sizes[j]
                last_res = res
                        
        print result_flag


if __name__ == "__main__":
    num_var = int(sys.argv[1])  #Number of parameters in the differential equation
    num_iter = int(sys.argv[2]) #Number of maximum iterations
    init_val = int(sys.argv[3]) #The initial value to start with
    expected_ratio = float(sys.argv[4])
    fastOde = FastOde(num_var, num_iter, init_val, expected_ratio)
    fastOde.solve()
