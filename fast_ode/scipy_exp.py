from scipy.integrate import odeint
import numpy as np

#t = [2, 4, 6, 8, 10]

t = np.linspace(2, 20, 10)

def fun(y, t, a, b, c):
    #dydt = (a * t * y * y) - (b/t) + (c/t*t)
    #dydt = y 
    dydt = 1
    return dydt

a=1
b=2
c=1

sol = odeint(fun, 10, t, args=(a, b, c))
print sol
