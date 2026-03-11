import numpy as np
from pymoo.core.algorithm import Algorithm
from pymoo.core.population import Population
from pymoo.operators.mutation.pm import PM


class HillClimbing(Algorithm):
    def __init__(self, sigma=0.01, **kwargs):
        super().__init__(**kwargs)
        self.mutation = PM(prob=1.0, eta=20)
        self.sigma = sigma

    def _initialize_infill(self):
        X = np.random.random(self.problem.n_var)
        xl, xu = self.problem.xl, self.problem.xu
        X = xl + X * (xu - xl)

        pop = Population.new("X", [X])
        self.evaluator.eval(self.problem, pop)
        return pop

    def _initialize_advance(self, infills=None, **kwargs):
        self.pop = infills

    def _infill(self):
        current = self.pop[0]

        off = Population.new("X", [current.X.copy()])
        self.mutation(self.problem, off)

        return off

    def _advance(self, infills=None, **kwargs):
        mutant = infills[0]
        current = self.pop[0]
        if mutant.F[0] < current.F[0]:
            self.pop[0] = mutant