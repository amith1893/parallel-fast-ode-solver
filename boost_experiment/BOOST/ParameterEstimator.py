import scipy.stats as stats
import numpy as np

class ParameterEstimator():
    def __init__(self):
        self.normal = {'mu': 5, 'sigma': 1}
    
    def get_distribution(self, distribution_type, num_samples, lower_limit, upper_limit):
        if distribution_type == 'normal':
            return stats.truncnorm((lower_limit - self.normal['mu'])/self.normal['sigma'], (upper_limit - self.normal['mu'])/self.normal['sigma'], loc=self.normal['mu'], scale=self.normal['sigma']).rvs(num_samples)
        elif distribution_type == 'uniform':  
            return np.random.uniform(low=lower_limit, high=upper_limit, size=num_samples)


    
