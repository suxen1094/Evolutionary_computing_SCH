import numpy as np
import random
import matplotlib.pyplot as plt
import time
import os

# Global variable setting
pop_size = 100                  # Population size
termination = 500               # Number of generation to stop
N = 10                          # N-dimensional Schwefel function problem
K = 10                          # Each element in vector is in [-512, 511] => 10 bits
s = 3                           # Used in tournament selection of survivor selection
current_round = 1               # Used when testing pc = [0, 0.2, 0.5, 0.8, 1]
tl = [0, 0.2, 0.5, 0.8, 1]       # Test possibility for pc and pm
nl = [2, 3, 4, 6, 8]            # Test number for n in tournament
take_aver = 30                  # Numbers of averages taken

# Used to calculate the average over 'take_aver' times
# 1: binary_GA_uniform_CO
# 2: binary_GA_2point_CO
# 3: real_GA_uniform_CO
# 4: real_GA_whole_arithmetic_CO
anytime_GA1 = [np.inf for k in range(termination)]
anytime_GA2 = [np.inf for k in range(termination)]
anytime_GA3 = [np.inf for k in range(termination)]
anytime_GA4 = [np.inf for k in range(termination)]
GA1_min = GA2_min = GA3_min = GA4_min = np.inf

# The Schwefel function
def schwefel(x):
    right_sum = 0
    for i in range(N):
        right_sum += x[i] * np.sin(np.sqrt(abs(x[i])))
    return (418.98291 * N - right_sum)