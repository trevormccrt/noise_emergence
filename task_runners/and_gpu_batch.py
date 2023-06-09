import datetime
import os

import evolution_runners, tasks, ragged_task_evolution

N = 8
population_size = 70
keep_best = int(0.4 * population_size)
n_children = population_size - keep_best
n_populations = 200
n_trajectories = 200
noise_prob = 0.00
mutation_rate = 0.005

init_avg_k = 2
max_k = 3

n_generations = 50000
n_memory_timesteps = 10

out_dir = os.path.join(os.getenv("DATA_DIR"), "boolean_network_data/and_evolution_results/{}".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
os.makedirs(out_dir, exist_ok=False)
checkpointint_dir = os.path.join(out_dir, "checkpoint_data/")
os.makedirs(checkpointint_dir, exist_ok=False)


file_name = "batch_1.npz"


def f_no_breed(f, c, uc):
    return f[0], c[0], uc[0]


f_breed = ragged_task_evolution.pair_breed_swap_all
f_mutate = lambda f, c, uc: ragged_task_evolution.mutate_equal_prob(f, c, uc, mutation_rate)

evolution_runners.evolve_random_batch(N, max_k, population_size, keep_best, n_populations, n_trajectories, noise_prob,
                                      init_avg_k, n_generations, n_memory_timesteps,
                                      tasks.make_2_bit_input_state, tasks.evaluate_and_task,
                                      f_breed, f_mutate,
                                      out_dir, file_name, using_cuda=True,
                                      checkpointing_freq=100, checkpointing_dir=checkpointint_dir)
