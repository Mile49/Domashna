import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

class CarGameEnv(gym.Env):
    def __init__(self):
        super(CarGameEnv, self).__init__()

        self.action_space = spaces.Discrete(3)  # left, stay, right

        self.observation_space = spaces.MultiDiscrete([3, 3, 10, 3, 10])

        self.reset()

    def reset(self, seed=None, options=None):
        self.main_lane = 1
        self.enemy1_lane = random.randint(0, 2)
        self.enemy2_lane = random.randint(0, 2)
        self.enemy1_y = -10
        self.enemy2_y = -20
        self.done = False
        self.score = 0
        return self._get_obs(), {}

    def _get_obs(self):
        enemy1_y_bin = min(9, max(0, int((self.enemy1_y + 100) / 70)))
        enemy2_y_bin = min(9, max(0, int((self.enemy2_y + 200) / 70)))
        return np.array([
            self.main_lane,
            self.enemy1_lane,
            enemy1_y_bin,
            self.enemy2_lane,
            enemy2_y_bin
        ])

    def step(self, action):
        if action == 0:
            self.main_lane = max(0, self.main_lane - 1)
        elif action == 2:
            self.main_lane = min(2, self.main_lane + 1)

        self.enemy1_y += 7
        self.enemy2_y += 9
        reward = 1

        if self.enemy1_y > 600:
            self.enemy1_lane = random.randint(0, 2)
            self.enemy1_y = -100
            self.score += 1

        if self.enemy2_y > 600:
            self.enemy2_lane = random.randint(0, 2)
            self.enemy2_y = -200
            self.score += 1

        if (self.enemy1_lane == self.main_lane and 470 <= self.enemy1_y <= 540) or            (self.enemy2_lane == self.main_lane and 470 <= self.enemy2_y <= 540):
            reward = -100
            self.done = True

        return self._get_obs(), reward, self.done, False, {}

    def render(self):
        print(f"Lane: {self.main_lane}, E1: ({self.enemy1_lane}, {self.enemy1_y}), "
              f"E2: ({self.enemy2_lane}, {self.enemy2_y})")

    def close(self):
        pass