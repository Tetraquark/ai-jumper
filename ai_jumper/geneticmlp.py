import random

import mlp


class GeneticMLP(mlp.MLP):

    def mutate(self):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                if random.choice([True, False]) == True:
                    self.weights[i][j] += 0.1
                else:
                    self.weights[i][j] -= 0.1

    def cross(self, otherWeights):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                self.weights[i][j] = (self.weights[i][j] + otherWeights[i][j]) / 2