import math
from DifferentialEquation import DifferentialEquation

class OdeSolver():
    def __init__(self):
        self.de = DifferentialEquation()
        
    def forward_euler_solver (self, x, step, iter_val, initial_value):
        y0 = initial_value
        y = y0 * 1.0
        t = 0
        counter = 0
        '''
        while not math.isinf(y) and counter <= iter_val:
            t += step
            y += step * self.de.evaluate_diff_equation (y, t, x)
            counter += 1
        '''
        while counter <= iter_val:
            t += step
            y += step * self.de.evaluate_diff_equation (y, t, x)
            counter += 1

        
        return y
   

o = OdeSolver()
print o.forward_euler_solver([2.51066,4.76718,6.80721], 2, 20, 10)
