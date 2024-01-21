from typing import Optional
from dtos import Flow, Graph
from common import Core
from .solution import Solution
from .randomized import RandomizedSolution
from .targets import Target
from visualization import Listener, BlankListener
import pygad
import numpy as np


class GeneticSolution(Solution):
    def __init__(self, graph: Graph, *, num_generations: int = 100, sol_per_pop: int = 100, mutation_intensity: int = 1):
        self.graph = graph
        self.num_generations = num_generations
        self.sol_per_pop = sol_per_pop
        self.mutation_intensity = mutation_intensity
    
    def solve(self, core: Core, target: Target, attach: Listener = BlankListener(), seed: Optional[int] = None) -> Flow:
        random = np.random.default_rng(seed)
        paths = self.graph.possible_paths()

        randomized = RandomizedSolution(self.graph)
        initial_population = [randomized.solve(core, seed=random.integers(2e6)).to_numpy() for _ in range(self.sol_per_pop)]

        def fitness_func(ga_instance, solution, solution_idx):
            return -target.calc(Flow(self.graph, {path: solution[idx] for idx, path in enumerate(paths)}), path=None)
        
        def crossover_func(parents, offspring_size, ga_instance):
            return np.array([
                core.correct_values(np.average(parents, axis=0, weights=random.uniform(0, 1, size=parents.shape[0]))) 
                for _ in range(offspring_size[0])
            ])
        
        def mutation_func(offspring, ga_instance):
            for idx in range(len(offspring)):
                for _ in range(self.mutation_intensity):
                    idx_from = random.integers(0, offspring.shape[1])
                    idx_to = random.integers(0, offspring.shape[1])
                    if idx_from != idx_to:
                        value = core.correct_value(offspring[idx][idx_from]*min(1, random.uniform(0, 1.15)))
                        offspring[idx][idx_from] -= value
                        offspring[idx][idx_to] += value
            return offspring

        def on_generation(ga_instance):
            solution = ga_instance.best_solution()[0]
            attach.on_iteration(Flow(self.graph, {path: solution[idx] for idx, path in enumerate(paths)}), None)
        
        
        attach.on_start(self.graph, core)
        ga_instance = pygad.GA(
            num_generations=self.num_generations,
            sol_per_pop=self.sol_per_pop,
            num_parents_mating=2,
            num_genes=len(paths),
            initial_population=initial_population,
            fitness_func=fitness_func,
            crossover_type=crossover_func,
            mutation_type=mutation_func if self.mutation_intensity > 0 else None,
            mutation_percent_genes=100,
            random_seed=seed,
            on_generation=on_generation
        )
        ga_instance.run()
        solution = core.correct_values(ga_instance.best_solution()[0])
        attach.on_end()
        return Flow(self.graph, {path: solution[idx] for idx, path in enumerate(paths)})