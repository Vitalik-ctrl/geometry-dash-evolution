# algorithms/memetic.py

import copy
import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.population import Population
from pymoo.operators.mutation.pm import PM


class MemeticGA(GA):
    def __init__(self, ls_freq=1, ls_depth=10, ls_ratio=0.1, **kwargs):
        """
        ls_freq: Run local search every N generations
        ls_depth: How many hill climbing steps to perform per individual
        ls_ratio: Top % of population to apply Local Search to (0.1 = top 10%)
        """
        super().__init__(**kwargs)
        self.ls_freq = ls_freq
        self.ls_depth = ls_depth
        self.ls_ratio = ls_ratio
        self.ls_mutation = PM(prob=1.0, eta=30)

    def _advance(self, infills=None):
        super()._advance(infills)

        if self.n_gen % self.ls_freq == 0:
            self.apply_local_search()

    def apply_local_search(self):
        sorted_indices = np.argsort(self.pop.get("F").flatten())
        n_elites = int(len(self.pop) * self.ls_ratio)
        if n_elites < 1: n_elites = 1

        elite_indices = sorted_indices[:n_elites]

        for idx in elite_indices:
            individual = self.pop[idx]
            for _ in range(self.ls_depth):
                mutant = copy.deepcopy(individual)

                noise = np.random.normal(0, 0.05, size=mutant.X.shape)
                mutant.X = np.clip(mutant.X + noise, 0, 1)

                out = {}
                self.problem._evaluate(mutant.X, out)
                mutant.F = out["F"]

                if mutant.F[0] < individual.F[0]:
                    individual.X = mutant.X
                    individual.F = mutant.F