import numpy as np
import random
import numpy as np
import random

def objective(v):
    x, y, z = v

    # Prevent division by zero or very small values
    if x == 0 or z == 0:
        return 1e12                # large positive penalty

    ratio = y / (x * z)
    temp_c = 700 + 19050 * ratio - 273.15
    inner = temp_c * 0.01917 + 726.59

    # Small regularization to avoid log(0) and pow(0, negative)
    arg_log = np.abs(0.0010822109 * inner) + 1e-8
    log_val = np.log(arg_log)
    abs_log = np.abs(log_val)

    # Avoid division by zero or extremely large exponents
    if abs_log < 1e-10:
        return 1e12                # penalty for getting too close to singularity

    power_term = abs_log ** (-2.6401255)
    product = 0.000677729241918855 * (inner ** 2) * power_term
    outer_arg = np.abs(product) + 1e-8

    return -np.log(outer_arg)

def simple_ga_optimize_pyr(
    objective_func,          # your func like liquid_opt_pyr or h2_vol_opt
    bounds,                  # list of (low, high) tuples, e.g. [(3.3,9)] or [(low1,up1), ...]
    pop_size=200,
    max_gen=200,
    cx_prob=0.5,
    mut_prob=0.2,
    tournament_size=3,
    progress_callback=None   # optional func(gen) to update progress
):
    n_vars = len(bounds)
    # Population: shape (pop_size, n_vars)
    pop = np.array([
        [random.uniform(low, high) for low, high in bounds]
        for _ in range(pop_size)
    ])

    best_sol = None
    best_fit = np.inf  # assume minimization; flip sign if maximizing

    for gen in range(max_gen):
        print(gen)
        # Evaluate
        fits = np.array([objective_func(ind) for ind in pop])
        if np.any(np.isinf(fits)):
            fits[np.isinf(fits)] = 0.0  # or large penalty

        # Assuming minimization (your code negates at end → treat as min -f1)
        min_idx = np.argmin(fits)
        if fits[min_idx] < best_fit:
            best_fit = fits[min_idx]
            best_sol = pop[min_idx].copy()

        # Tournament selection
        selected = []
        for _ in range(pop_size):
            candidates_idx = random.sample(range(pop_size), tournament_size)
            winner_idx = candidates_idx[np.argmin(fits[candidates_idx])]
            selected.append(pop[winner_idx].copy())
        selected = np.array(selected)

        # Crossover (blend for reals)
        offspring = selected.copy()
        for i in range(0, pop_size, 2):
            if i+1 < pop_size and random.random() < cx_prob:
                alpha = random.random()
                offspring[i]   = alpha * selected[i] + (1-alpha) * selected[i+1]
                offspring[i+1] = alpha * selected[i+1] + (1-alpha) * selected[i]

        # Mutation
        for ind in offspring:
            if random.random() < mut_prob:
                for j in range(n_vars):
                    if random.random() < 0.2:  # per-gene prob
                        sigma = (bounds[j][1] - bounds[j][0]) * 0.1
                        ind[j] += random.gauss(0, sigma)
                        ind[j] = np.clip(ind[j], bounds[j][0], bounds[j][1])

        pop = offspring

        if progress_callback:
            progress_callback(gen + 1)

    return best_sol, best_fit

