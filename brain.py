import random
import numpy as np

class Brain:
    DECISION_WAIT = 0
    DECISION_JUMP = 1
    OUTPUT_THRESHOLD = 0.5
    HIDDEN_LAYERS = 1
    NEURONS_PER_LAYER = 5

    def __init__(self):
        np.random.seed(99)
        self.layers = []
        self.layers.append(self.create_layer(2, Brain.NEURONS_PER_LAYER))
        
        for i in range(Brain.HIDDEN_LAYERS):
            self.layers.append(self.create_layer(Brain.NEURONS_PER_LAYER, Brain.NEURONS_PER_LAYER))
        
        self.layers.append(self.create_layer(Brain.NEURONS_PER_LAYER, 1))

    def create_layer(self, x, y):
        layer = np.random.uniform(-1., 1., size=(x, y))
        return layer.astype(np.float32)
    
    def activation(self, x):
        return 1/(1 + np.exp(-x))

    def normalize(self, x):
        d = x[0]
        hd = x[1]
        return np.array([d, hd])

    def feed_forward(self, x):
        x = self.normalize(x)
        x_a = x

        for i in range(len(self.layers)):
            x_l = x_a.dot(self.layers[i])
            x_a = self.activation(x_l)

        return x_l

    def decision(self, d, hd):
        inp = self.normalize([d, hd])
        out = self.feed_forward(inp)

        if out[0] < Brain.OUTPUT_THRESHOLD:
            return Brain.DECISION_JUMP
        else:
            return Brain.DECISION_WAIT
