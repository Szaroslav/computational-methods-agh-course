import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import math
from enum import Enum
from itertools import permutations

n = 64
deltas = [.1, .3, .4]

image = np.random.randint(100, size=(n, n))
for i in range(n):
    for j in range(n):
        image[i][j] = 0 if image[i][j] < 30 else 1


class SimulatedAnnealingImage:
    def __init__(self, initial_solution, gamma, initial_T, max_iterations):
        self.initial_solution = initial_solution
        self.gamma = gamma
        self.T = initial_T
        self.max_iterations = max_iterations

    def run(self):
        fig, ax = plt.subplots()
        ims = []

        state, state_energy = copy.copy(self.initial_solution), self.__E(self.initial_solution)
        solution, solution_energy = copy.copy(state), state_energy

        swaps = 0
        for c in range(self.max_iterations):
            # if self.T <= 10**-6:
            #     break

            # Progress bar
            # if c % 20000 == 0:
            #     p = c / self.max_iterations
            #     if p > 0:
            #         print(f"\r[{'=' * math.ceil((25 * c / p))}{' ' * math.floor((25 * (1 - p)))}]", end='')
            #     else:
            #         print(f"\r[{' ' * 25}]", end='')

            i, j = np.random.randint(n, size=2)
            neighbour = self.neighbour(state, (i, j))
            local_state_energy = np.abs(self.E(state, (i, j)) - self.E(state, neighbour))
            state[i][j], state[neighbour[0]][neighbour[1]] = state[neighbour[0]][neighbour[1]], state[i][j]
            local_new_state_energy = np.abs(self.E(state, (i, j)) - self.E(state, neighbour))
            # print(local_state_energy, local_new_state_energy)
            if self.P(local_new_state_energy, local_state_energy) >= np.random.uniform(0, 1):
                swaps += 1
                # print(i, j, neighbour[0], neighbour[1], local_new_state_energy - local_state_energy)
                # if state_energy < solution_energy:
                #     solution, solution_energy = copy.copy(state), state_energy
            else:
                state[i][j], state[neighbour[0]][neighbour[1]] = state[neighbour[0]][neighbour[1]], state[i][j]

            self.T *= self.gamma

            if c % 10000 == 0:
                if c == 0:
                    ax.imshow(state, cmap="gray", vmin=0, vmax=1, interpolation="none")
                im = ax.imshow(state, cmap="gray", vmin=0, vmax=1, interpolation="none", animated=True)
                ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, interval=100)
        plt.show()

        print(f"\r{' ' * 50}")
        return state, self.__E(state)

    def E(self, state, pos):
        if state[pos[0]][pos[1]] != 0:
            return 0
        return self.distance(pos)

    def __E(self, state):
        n, acc = len(state), 0
        for i in range(n):
            for j in range(n):
                acc += self.E(state, (i, j))

        return acc

    def distance(self, p):
        n = len(self.initial_solution)

        # Upper left
        if 0 <= p[0] < n // 2 and 0 <= p[1] < n // 2:
            p0 = (0, 0)
        # Upper right
        elif n // 2 <= p[0] < n and 0 <= p[1] < n // 2:
            p0 = (n - 1, 0)
        # Bottom right
        elif n // 2 <= p[0] < n and n // 2 <= p[1] < n:
            p0 = (n - 1, n - 1)
        # Bottom left
        else:
            p0 = (0, n - 1)

        return math.ceil(((p0[0] - p[0]) ** 2 + (p0[1] - p[1]) ** 2) * .5)

    def neighbour(self, state, pos):
        neighbours = []
        deltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        n = len(state)

        i, j = np.random.randint(n, size=2)
        for di, dj in deltas:
            if 0 <= pos[0] + di < n and 0 <= pos[1] + dj < n and state[pos[0] + di][pos[1] + dj] != state[pos[0]][pos[1]]:
                neighbours.append((pos[0] + di, pos[1] + dj))

        return neighbours[np.random.randint(len(neighbours))] if len(neighbours) > 0 else pos

    def P(self, new_state_cost, state_cost):
        if new_state_cost < state_cost:
            return 1
        return np.exp((state_cost - new_state_cost) / self.T)


plt.imshow(image, cmap="gray", vmin=0, vmax=1, interpolation="none")
plt.show()

solution, energy = SimulatedAnnealingImage(image, .99, 1000, 100000).run()
plt.imshow(solution, cmap="gray", vmin=0, vmax=1, interpolation="none")
plt.show()
