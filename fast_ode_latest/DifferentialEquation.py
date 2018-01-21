class DifferentialEquation():
    def __init__(self):
        pass

    def evaluate_diff_equation(self, y, t, x):
        new_y = (x[0] * t * y * y) - (x[1]/t) + (x[2]/t*t)
        return new_y
