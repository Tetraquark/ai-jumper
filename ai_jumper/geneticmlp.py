import random
import copy

import mlp

class GeneticMLP(mlp.MLP):

    def mutate(self):
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                if random.choice([True, False]) == True:
                    self.weights[i][j] += 0.2
                else:
                    self.weights[i][j] -= 0.2

    def cross(self, otherWeights):
        child1 = copy.deepcopy(self.weights)
        child2 = copy.deepcopy(self.weights)
        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                if j > len(self.weights[i]) / 2:
                    child1[i][j] = otherWeights[i][j]
                    child2[i][j] = self.weights[i][j]
                else:
                    child1[i][j] = self.weights[i][j]
                    child2[i][j] = otherWeights[i][j]
        return child1, child2