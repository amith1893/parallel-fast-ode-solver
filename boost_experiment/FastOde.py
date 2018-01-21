from ParameterEstimator import ParameterEstimator
import configparser
import sys
import itertools
import numpy

class FastOde():
    def __init__(self, param_list, num_iter, init_val, accuracy, dist, num_samples, max_step_size):
        self.param_list = param_list
        self.num_iter = num_iter
        self.init_val = init_val
        self.accuracy = accuracy
        self.param_list = param_list
        self.dist = dist
        self.num_samples = num_samples
        self.max_step_size = max_step_size
        self.parameter_matrix = []
        self.parameter_combinations = []
        self.pe = ParameterEstimator()

    def setup_parameters(self):
        for param in self.param_list:
            self.parameter_matrix.append(self.pe.get_distribution(self.dist, self.num_samples, param[0], param[1]))
        self.parameter_combinations = [list(x) for x in list(itertools.product(*self.parameter_matrix))]
        #print len(self.parameter_matrix)
         
    def setup_list_for_solving(self):
        #need to instantiate the previous value, infinity value and iteration time
        for each_comb in self.parameter_combinations:
            each_comb.append(self.max_step_size)
            each_comb.append("inf")
            each_comb.append(1)
        
        print self.parameter_combinations
       
    def solve(self):
        #this is where the boost library comes into the picture
        pass
    
if __name__ == "__main__":
   
    if len(sys.argv) == 1:
        print "Please specify the config filename"
        exit()

    config_filename = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_filename)
    
    num_par  = int(config['BASIC']['NumParameters'])
    num_iter = int(config['BASIC']['NumIterations'])
    init_val = int(config['BASIC']['InitialValue'])
    accuracy = float(config['BASIC']['Accuracy'])
    dist     = config['BASIC']['DistType']
    num_samples = int(config['BASIC']['NumSamples'])
    max_step_size = int(config['BASIC']['MaxStepSize'])
    param_input_val = [int(x) for x in config['BASIC']['ParamRanges'].split()]
    param_list = []
    
    for i in range(0, len(param_input_val), 2):
        param_list.append((param_input_val[i], param_input_val[i+1]))

    
    fastOde = FastOde(param_list, num_iter, init_val, accuracy, dist, num_samples, max_step_size)
    fastOde.setup_parameters() 
    fastOde.setup_list_for_solving()
    fastOde.solve()
