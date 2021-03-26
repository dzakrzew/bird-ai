import random
import numpy as np

class Brain:
    DECISION_WAIT = 0
    DECISION_JUMP = 1

    def __init__(self):
        np.random.seed(99)
        self.l1 = self.create_layer(2, 5)
        self.l2 = self.create_layer(5, 5)
        self.l3 = self.create_layer(5, 1)

    def create_layer(self, x, y):
        layer = np.random.uniform(-1., 1., size=(x, y)) / np.sqrt(x * y)
        return layer.astype(np.float32)
    
    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    def d_sigmoid(self, x):
        return (np.exp(-x))/((np.exp(-x)+1)**2)

    def softmax(self, x):
        exponents = np.exp(x)
        return exponents/np.sum(exponents)

    def normalize(self, x):
        d = x[0]
        hd = x[1]
        return np.array([d, hd])

    def propagation(self, x):
        x = self.normalize(x)
        #print(x)
        x_l1 = x.dot(self.l1)
        x1_sigmoid = self.sigmoid(x_l1)

        x_l2 = x1_sigmoid.dot(self.l2)
        x2_sigmoid = self.sigmoid(x_l2)

        x_l3 = x2_sigmoid.dot(self.l3)
        out = x_l3

        return out

    def decision(self, d, hd):
        input = self.normalize([d, hd])
        out = self.propagation(input)
        print(out)
        jump = out[0] < 0.045
        
        if jump:
            return Brain.DECISION_JUMP
        else:
            return Brain.DECISION_WAIT
