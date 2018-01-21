class AdaptiveSolver():
    def __init__(self):
        self.last_stable_step_size = -1


    def set_last_stable_step_size(self, ss):
        self.last_stable_step_size = ss

    def get_step_size(self, ss):
        return [ss*1.0/pow(2,s)  for s in range(0,11)]
