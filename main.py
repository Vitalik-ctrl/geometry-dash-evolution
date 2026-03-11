# main.py

import numpy as np
import matplotlib.pyplot as plt
import time

from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.callback import Callback

from optimization.hill_climbing import HillClimbing
from optimization.memetic import MemeticGA
from optimization.problem import GeometryDashProblem
from game_engine.core import run_simulation


class ProgressCallback(Callback):
    """Callback to track optimization progress"""

    def __init__(self):
        super().__init__()
        self.best_distances = []
        self.avg_distances = []
        self.generation_times = []
        self.diversity_scores = []
        self.gen_start_time = None

    def notify(self, algorithm):
        if hasattr(algorithm, 'pop') and algorithm.pop is not None and len(algorithm.pop) > 0:
            F = algorithm.pop.get("F")
            if F is None: return

            F = F.flatten()
            distances = -F

            self.best_distances.append(np.max(distances))
            self.avg_distances.append(np.mean(distances))

            self.diversity_scores.append(np.std(distances))
        else:
            pass

        if self.gen_start_time is not None:
            gen_time = time.time() - self.gen_start_time
            self.generation_times.append(gen_time)

        self.gen_start_time = time.time()


def plot_optimization_progress(callback):
    """Plot 1: Optimization Progress (Best vs Average Distance)"""
    if not callback.best_distances: return None

    generations = range(1, len(callback.best_distances) + 1)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(generations, callback.best_distances, 'b-', linewidth=2.5,
            label='Best Distance', marker='o', markersize=4)
    ax.plot(generations, callback.avg_distances, 'r--', linewidth=2,
            label='Average Distance', marker='s', markersize=3, alpha=0.7)

    ax.fill_between(generations, callback.avg_distances, callback.best_distances,
                    alpha=0.2, color='green')

    ax.set_xlabel('Generation', fontsize=12, fontweight='bold')
    ax.set_ylabel('Distance (pixels)', fontsize=12, fontweight='bold')
    ax.set_title('Optimization Progress: Distance Over Generations',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='lower right')
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig


def plot_generation_timing(callback):
    """Plot 2: Generation Time Analysis"""
    if not callback.generation_times: return None

    generations = range(1, len(callback.generation_times) + 1)
    times = callback.generation_times

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.bar(generations, times, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.axhline(np.mean(times), color='red', linestyle='--', linewidth=2,
                label=f'Average: {np.mean(times):.2f}s')

    ax1.set_xlabel('Generation', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Time per Generation', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')

    cumulative_time = np.cumsum(times)
    ax2.plot(generations, cumulative_time, 'g-', linewidth=2.5, marker='o', markersize=4)
    ax2.fill_between(generations, 0, cumulative_time, alpha=0.3, color='green')

    ax2.set_xlabel('Generation', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cumulative Time (seconds)', fontsize=12, fontweight='bold')
    ax2.set_title('Cumulative Optimization Time', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_population_diversity(callback):
    """Plot 3: Population Diversity Over Time"""
    if not callback.diversity_scores: return None

    generations = range(1, len(callback.diversity_scores) + 1)
    diversity = callback.diversity_scores

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(generations, diversity, 'purple', linewidth=2.5, marker='D', markersize=4)
    ax1.fill_between(generations, 0, diversity, alpha=0.3, color='purple')

    ax1.set_xlabel('Generation', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Diversity (Std Dev of Distance)', fontsize=12, fontweight='bold')
    ax1.set_title('Population Diversity Over Generations', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def main():
    # MODE HERE: "GA", "MA", or "HC"
    ALGORITHM_MODE = "MA"
    MAX_TIME = 40.0

    if ALGORITHM_MODE == "HC":
        POPULATION_SIZE = 1
        GENERATIONS = 20_000
        MAX_JUMPS = 80
    else:
        POPULATION_SIZE = 450
        GENERATIONS = 150
        MAX_JUMPS = 80

    print("=" * 70)
    print(f"GEOMETRY DASH - ALGORITHM: {ALGORITHM_MODE}")
    print("=" * 70)
    print(f"Population Size: {POPULATION_SIZE}")
    print(f"Generations: {GENERATIONS}")
    print(f"Max Jumps: {MAX_JUMPS}")
    print("=" * 70 + "\n")

    callback = ProgressCallback()

    algorithm = ALGORITHM_MODE

    if ALGORITHM_MODE == "GA":
        algorithm = GA(
            pop_size=POPULATION_SIZE,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(prob=2.0 / (MAX_JUMPS * 2), eta=10),
            eliminate_duplicates=True
        )
    elif ALGORITHM_MODE == "MA":
        algorithm = MemeticGA(
            ls_freq=1,
            ls_depth=5,
            ls_ratio=0.05,
            pop_size=POPULATION_SIZE,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(prob=2.0 / (MAX_JUMPS * 2), eta=10),
            eliminate_duplicates=True
        )
    elif ALGORITHM_MODE == "HC":
        algorithm = HillClimbing()

    problem = GeometryDashProblem(max_jumps=MAX_JUMPS, max_time=MAX_TIME)

    print("Starting optimization...\n")
    start_time = time.time()

    res = minimize(problem,
                   algorithm,
                   ('n_gen', GENERATIONS),
                   callback=callback,
                   seed=1,
                   verbose=True)

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("OPTIMIZATION COMPLETE")
    print("=" * 70)
    print(f"Total Time: {int(total_time // 60)}m {int(total_time % 60)}s")
    print("=" * 70 + "\n")


    X_pop = []
    F_pop = []

    if ALGORITHM_MODE == "HC":
        X_pop = [res.X]
        F_pop = [res.F]
    else:
        X_pop = res.pop.get("X")
        F_pop = res.pop.get("F")

    F_pop = np.asarray(F_pop).reshape(-1)

    distances = -F_pop

    jumps = np.array([run_simulation(ind, render=False)[1] for ind in X_pop], dtype=float)
    efficiency = distances / (jumps + 1)

    furthest_idx = int(np.argmax(distances))

    print("=" * 70)
    print("FINAL STATISTICS")
    print("=" * 70)
    print(f"Best Distance: {distances[furthest_idx]:.0f} pixels")
    print(f"Best Jumps: {jumps[furthest_idx]:.1f}")
    print(f"Best Efficiency: {efficiency[furthest_idx]:.1f} px/jump")

    if len(callback.best_distances) > 0:
        print(f"\nImprovement: {callback.best_distances[-1] - callback.best_distances[0]:.0f} pixels")
        if len(callback.diversity_scores) > 0 and callback.diversity_scores[0] > 0:
            print(f"Convergence: {((1 - callback.diversity_scores[-1] / callback.diversity_scores[0]) * 100):.1f}%")
    print("=" * 70 + "\n")

    print("Generating graphs...\n")

    if len(callback.best_distances) > 0:
        fig1 = plot_optimization_progress(callback)
        fig2 = plot_generation_timing(callback)
        fig3 = plot_population_diversity(callback)
        plt.show()

    best_solution = X_pop[furthest_idx]
    print("Best Genome: ", best_solution)

    cmd = input("\nRun simulation? (y/n): ")
    if cmd.lower() == "y":
        run_simulation(best_solution, render=True)


if __name__ == "__main__":
    main()