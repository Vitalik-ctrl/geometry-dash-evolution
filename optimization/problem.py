# optimization/problem.py

import numpy as np

from pymoo.core.problem import ElementwiseProblem

from semestral_project.game_engine.core import run_simulation


class GeometryDashProblem(ElementwiseProblem):
    def __init__(self, max_jumps=40, max_time=40.0):
        self.max_jumps = max_jumps
        self.max_time = max_time

        n_var = max_jumps * 2

        xl = []
        xu = []
        for i in range(max_jumps):
            xl.extend([0.0, 0.0])
            xu.extend([max_time, 1.5])

        super().__init__(n_var=n_var, n_obj=1, n_constr=0, xl=np.array(xl), xu=np.array(xu))

    def _evaluate(self, x, out, *args, **kwargs):
        distance, jumps = run_simulation(x, render=False)
        out["F"] = [-distance]
