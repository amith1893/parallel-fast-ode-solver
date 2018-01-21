import numpy as np

class ParameterEstimator():
    def __init__(self):
        self.normal = {'mu': 5, 'sigma': 1}
        self.lognormal = {'mu': 5, 'sigma': 1}
        self.exponential = {'range': 2}
    
    def get_distribution(self, distribution_type, num_samples):
        if distribution_type == 'normal':
            return np.random.normal(self.normal['mu'], self.normal['sigma'], num_samples)
        elif distribution_type == 'lognormal':
            return np.random.lognormal(self.lognormal['mu'], self.lognormal['sigma'], num_samples)
        elif distribution_type == 'exponential':
            return np.random.exponential(self.exponential['range'], num_samples)



    
