import numpy as np
import random

class Mutate(object):
    """Operation of mutating a NN."""

    def __init__(self,net,mutationRate=.05):

        self.oldnet = net
        self.newnet = net.copy()
        self.mutationRate = mutationRate

        for l in self.newnet.layers:
            for i in range(l.np['b'].shape[0]):
                if random.random()>(1-self.mutationRate):
                    l.np['b'][i] = 1-2*random.random()

            for i in range(l.np['w'].shape[0]):
                for j in range(l.np['w'].shape[1]):
                if random.random()>(1-self.mutationRate):
                    l.np['w'][i,j] = 1-2*random.random()

    def mutant(self):
        return self.newnet
