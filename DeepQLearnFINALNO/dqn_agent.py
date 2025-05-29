import numpy as np
from car_game_env import CarGameEnv

env = CarGameEnv()

# Fix: Get shape from MultiDiscrete using nvec
obs_space_shape = tuple(env.observation_space.nvec)
num_actions = env.action_space.n

Q = np.zeros(obs_space_shape + (num_actions,), dtype=np.float32)


alpha = 0.1
gamma = 0.99
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 1000

for ep in range(episodes):
    state, _ = env.reset()
    total_reward = 0
    done = False

    while not done:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[tuple(state)])

        next_state, reward, done, _, _ = env.step(action)

        best_next = np.max(Q[tuple(next_state)])
        Q[tuple(state)][action] += alpha * (reward + gamma * best_next - Q[tuple(state)][action])

        state = next_state
        total_reward += reward

    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if ep % 100 == 0:
        print(f"Episode {ep}, Total Reward: {total_reward}, Epsilon: {epsilon:.3f}")

np.save("car_dqn_project/car_q_table.npy", Q)