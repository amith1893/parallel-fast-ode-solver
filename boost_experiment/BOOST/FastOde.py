from ParameterEstimator import ParameterEstimator
import configparser
import sys
import itertools
import numpy
#import ode_solver
import ode_solver_modf
from GraphPlot import GraphPlot

class FastOde():
    def __init__(self, num_par, param_list, num_iter, init_val, accuracy, dist, num_samples, max_step_size, max_steps):
        self.param_list = param_list
        self.num_iter = num_iter
        self.init_val = init_val
        self.accuracy = accuracy
        self.param_list = param_list
        self.dist = dist
        self.max_steps = max_steps
        self.num_par = num_par
        self.num_samples = num_samples
        self.max_step_size = max_step_size
        self.parameter_matrix = []
        self.parameter_combinations = []
        self.pe = ParameterEstimator()
        self.gp = GraphPlot() 

    def setup_parameters(self):
        for param in self.param_list:
            self.parameter_matrix.append(self.pe.get_distribution(self.dist, self.num_samples, param[0], param[1]))
        self.parameter_combinations = [list(x) for x in list(itertools.product(*self.parameter_matrix))]
        #print len(self.parameter_matrix)
         
    def setup_list_for_solving(self):
        #need to instantiate the previous value, infinity value and iteration time
        for each_comb in self.parameter_combinations:
            each_comb.append(self.max_step_size)
            each_comb.append(float('inf'))
            each_comb.append(1)
        
        #print self.parameter_combinations
       
    def solve(self):
        #this is where the boost library comes into the picture
        res = ode_solver_modf.OdeSolve(self.parameter_combinations, self.num_par, self.accuracy, self.num_iter, self.init_val, self.max_steps)
       
        self.gp.plot(res, self.num_par)

if __name__ == "__main__":
   
    if len(sys.argv) == 1:
        print "Please specify the config filename"
        exit()

    config_filename = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_filename)
    
    num_par  = int(config['BASIC']['NumParameters'])
    num_iter = int(config['BASIC']['NumIterations'])
    max_steps = int(config['BASIC']['MaxSteps'])
    init_val = int(config['BASIC']['InitialValue'])
    accuracy = float(config['BASIC']['Accuracy'])
    dist     = config['BASIC']['DistType']
    num_samples = int(config['BASIC']['NumSamples'])
    max_step_size = int(config['BASIC']['MaxStepSize'])
    param_input_val = [int(x) for x in config['BASIC']['ParamRanges'].split()]
    param_list = []
    
    for i in range(0, len(param_input_val), 2):
        param_list.append((param_input_val[i], param_input_val[i+1]))

    
    fastOde = FastOde(num_par, param_list, num_iter, init_val, accuracy, dist, num_samples, max_step_size, max_steps)
    fastOde.setup_parameters() 
    fastOde.setup_list_for_solving()
    fastOde.solve()
