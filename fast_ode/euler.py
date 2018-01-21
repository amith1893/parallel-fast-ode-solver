

class EulerEstimation():
    
    def __init__(self, step_size, target, initial_value, lambda_value):
        self.step_size = step_size
        self.target = target
        self.init_val = initial_value
        self.lambda_val = lambda_value 
        
        #the below two lists are instantiated
        #to allow us to plot the values
        self.y = list()
        self.t = list()

    def __get_next_forward_euler_val(self, y):
        return y + (self.step_size) * self.lambda_val * y * 1.0 

    def __get_next_backward_euler_val(self, y):
        return (y*1.0)/(1 - (self.step_size * self.lambda_val))
    
    def __estimate (self, curr_iter, prev_y, callback_func):
        #boundary condition
        if curr_iter > self.target:
            return prev_y

        
        #pres_y = prev_y + (self.step_size) * self.lambda_val * prev_y 
        return self.__estimate (curr_iter+1, callback_func(prev_y), callback_func)

    def estimate_using_forward_euler(self):
        #print self.__estimate (1, self.init_val, self.__get_next_forward_euler_val)
        return self.__estimate (1, self.init_val, self.__get_next_forward_euler_val)

    def estimate_using_backward_euler(self):
        #print self.__estimate (1, self.init_val, self.__get_next_backward_euler_val)
        return self.__estimate (1, self.init_val, self.__get_next_backward_euler_val)
