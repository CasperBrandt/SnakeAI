import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame
import random
import math

# Window size
window_x = 1000
window_y = 1000

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

RENDER_FPS = 3

class SnakeEnv(gym.Env):
    """Snake Environment that follows gym interface."""

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode=render_mode
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-1000, high=1000,
                                            shape=(8,), dtype=np.float64)

    def step(self, action):
        # handling key events
        self.change_to = action

        # Makes sure AI cant do illegal turns
        if self.change_to == 0 and self.direction != 1:
            self.direction = 0
        if self.change_to == 1 and self.direction != 0:
            self.direction = 1
        if self.change_to == 2 and self.direction != 3:
            self.direction = 2
        if self.change_to == 3 and self.direction != 2:
            self.direction = 3

        # Moving the snake
        if self.direction == 0:
            self.snake_position[1] -= 100
        if self.direction == 1:
            self.snake_position[1] += 100
        if self.direction == 2:
            self.snake_position[0] -= 100
        if self.direction == 3:
            self.snake_position[0] += 100

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 10
            self.timeSinceFruit = 0
            self.fruit_spawn = False
        else:
            self.snake_body.pop()
            
        while not self.fruit_spawn:
            self.fruit_position = [random.randrange(1, (window_x//100)) * 100, 
                            random.randrange(1, (window_y//100)) * 100]
            if self.fruit_position not in self.snake_body:
                self.fruit_spawn = True
                    
        # Game Over conditions
        if self.snake_position[0] < 0 or self.snake_position[0] > window_x-100:
            self.terminated = True
        if self.snake_position[1] < 0 or self.snake_position[1] > window_y-100:
            self.terminated = True
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.terminated = True
        
        # Coordinates to the head of the snake
        headx = self.snake_position[0]
        heady = self.snake_position[1]
        
        # Length of the snake
        snakeLength = len(self.snake_body) 
        
        # Todo: Come up with a clever way to let the agent know where the snakes body is,
        
        
        # Coordinates to the fruit
        fruitx = self.fruit_position[0]
        fruity = self.fruit_position[1]
        
        # Euclidean distance between head and fruit
        fruitdist = math.sqrt( ((headx-fruitx)**2) + ((heady-fruity)**2) )
        
        # Direction that the snake is traveling in
        snakeDirection = self.direction
        
        # Knowledge that the agent will have access to
        self.observation = [headx, heady, snakeLength, fruitx, fruity, fruitdist, snakeDirection, self.timeSinceFruit]
        self.observation = np.array(self.observation)
        
        # Step time since fruit has been eaten
        self.timeSinceFruit += 1
        
        # Makes sure that the agent doesnt end up in a loop
        if self.timeSinceFruit > 20+snakeLength:
            self.truncated = True
        
        # If the agent dies or ends up in a loop it gets a negative reward, else its the normal reward
        if self.terminated or self.truncated:
            self.reward = -10
        else:
            self.reward = self.score*snakeLength
        
        info = {}
        return self.observation, self.reward, self.terminated, self.truncated, info

    def reset(self, seed=None, options=None):
        if self.render_mode == 'human':
            # Initialising pygame
            pygame.init()
            # Initialise game window
            pygame.display.set_caption('GeeksforGeeks Snakes')
            self.game_window = pygame.display.set_mode((window_x, window_y))
            # FPS (frames per second) controller
            self.fps = pygame.time.Clock()
        
        self.terminated=False
        self.truncated = False
        # defining snake default position
        self.snake_position = [500, 500]
        # defining first 3 blocks of snake body
        self.snake_body = [[500, 500],
                    [400, 500],
                    [300, 500]
                    ]
        # fruit position
        self.fruit_spawn = False
        while not self.fruit_spawn:
                self.fruit_position = [random.randrange(1, (window_x//100)) * 100, 
                                random.randrange(1, (window_y//100)) * 100]
                if self.fruit_position not in self.snake_body:
                    self.fruit_spawn = True
        # setting default snake direction towards
        # right
        self.direction = 3
        self.change_to = self.direction
        # initial score
        self.score = 0
        self.reward = 0
        self.timeSinceFruit = 0
        
        # Coordinates to the head of the snake
        headx = self.snake_position[0]
        heady = self.snake_position[1]
        
        # Length of the snake
        snakeLength = len(self.snake_body) 
        
        # Todo: Come up with a clever way to let the agent know where the snakes body is,
        
        
        # Coordinates to the fruit
        fruitx = self.fruit_position[0]
        fruity = self.fruit_position[1]
        
        # Euclidean distance between head and fruit
        fruitdist = math.sqrt( ((headx-fruitx)**2) + ((heady-fruity)**2) )
        
        # Direction that the snake is traveling in
        snakeDirection = self.direction
        
        # Knowledge that the agent will have access to
        self.observation = [headx, heady, snakeLength, fruitx, fruity, fruitdist, snakeDirection, self.timeSinceFruit]
        self.observation = np.array(self.observation)
        
        self.info = {}

        return self.observation, self.info
    
    def render(self):
        self.game_window.fill(black)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, green,
                            pygame.Rect(pos[0], pos[1], 100, 100))
        pygame.draw.rect(self.game_window, white, pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 100, 100))
        # Refresh game screen
        pygame.display.update()
        self.fps.tick(RENDER_FPS)
    
    def close(self):
        pygame.quit()