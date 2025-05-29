import pygame
import numpy as np
from car_game_env import CarGameEnv

Q = np.load("car_dqn_project/car_q_table.npy")
env = CarGameEnv()

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("DQN Car Game")

LANE_X = [80, 170, 260]
CAR_WIDTH = 50
CAR_HEIGHT = 80

def draw_game(main_lane, enemy1_lane, enemy1_y, enemy2_lane, enemy2_y):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (LANE_X[main_lane], 500, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.rect(screen, (255, 0, 0), (LANE_X[enemy1_lane], enemy1_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 255), (LANE_X[enemy2_lane], enemy2_y, CAR_WIDTH, CAR_HEIGHT))
    pygame.display.flip()

clock = pygame.time.Clock()

for _ in range(3):
    state, _ = env.reset()
    done = False

    while not done:
        pygame.event.pump()
        action = np.argmax(Q[tuple(state)])
        next_state, reward, done, _, _ = env.step(action)
        draw_game(env.main_lane, env.enemy1_lane, env.enemy1_y, env.enemy2_lane, env.enemy2_y)
        state = next_state
        clock.tick(30)

pygame.quit()