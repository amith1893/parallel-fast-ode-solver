import matplotlib.pyplot as plt
from math import exp, expm1
from mpl_toolkits.mplot3d import Axes3D

class GraphPlot():
    def __init__(self):
        self.input = []
        self.y = []
        self.h = []
        self.a = []
        self.b = []
        self.c = []

    def plot(self, input_list, num_par):
        self.input = input_list
        for each in self.input:
            if each[num_par+4-1] == 1:
                self.y.append(each[num_par+3-1])
                #print each[num_par+3-1]
                #print abs(each[num_par+1-1])
                self.h.append(abs(each[num_par+1-1]))
                self.a.append(each[0])
                self.b.append(each[1])
                self.c.append(each[2])
        
        plt.hist(self.y)       
        plt.savefig("HistogramOfY")
        plt.clf()

        plt.hist(self.h)
        plt.savefig("HistogramOfH")
        plt.clf()
        
        plt.hist(self.a)
        plt.savefig("HistogramOfA")
        plt.clf()

        plt.hist(self.b)
        plt.savefig("HistogramOfB")
        plt.clf()
        
        plt.hist(self.c)
        plt.savefig("HistogramOfC")
        plt.clf()

        fig = plt.figure()
        ax = Axes3D(fig)

        ax.plot_wireframe(self.a, self.b, self.y)
        plt.show()
