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

class SnakeEnv(gym.Env):
    """Snake Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super(SnakeEnv, self).__init__()
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

        # If two keys pressed simultaneously
        # we don't want snake to move into two 
        # directions simultaneously
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
        # if fruits and snakes collide then scores
        # will be incremented by 10
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
            
        self.game_window.fill(black)
        
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, green,
                            pygame.Rect(pos[0], pos[1], 100, 100))
        pygame.draw.rect(self.game_window, white, pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 100, 100))

        # Game Over conditions
        if self.snake_position[0] < 0 or self.snake_position[0] > window_x-100:
            self.done = True
        if self.snake_position[1] < 0 or self.snake_position[1] > window_y-100:
            self.done = True
            
        

        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.done = True

        # Refresh game screen
        pygame.display.update()
        # Frame Per Second /Refresh Rate
        self.fps.tick(3)
        
        # Vart ormens huvud är
        headx = self.snake_position[0]
        heady = self.snake_position[1]
        
        # Vart ormens kropp är
        snakeLength = len(self.snake_body) #todo:kom på hur man kan säga vart kroppen är, Längden på ormen tills dess 
        
        # Vart frukten finns
        fruitx = self.fruit_position[0]
        fruity = self.fruit_position[1]
        
        # Hur långt ifrån frukten huvudet är
        fruitdist = math.sqrt( ((headx-fruitx)**2) + ((heady-fruity)**2) )
        
        # Vilken riktning ormen rör sig åt
        snakeDirection = self.direction
        
        self.observation = [headx, heady, snakeLength, fruitx, fruity, fruitdist, snakeDirection, self.timeSinceFruit]
        self.observation = np.array(self.observation)
        self.timeSinceFruit += 1
        
        if self.timeSinceFruit > 20+snakeLength:
            self.truncated = True
        
        if self.done or self.truncated:
            self.reward = -10
        else:
            self.reward = self.score*snakeLength
            
        self.terminated = self.done
        
        
        info = {}
        return self.observation, self.reward, self.terminated, self.truncated, info

    def reset(self, seed=None, options=None):
        # Initialising pygame
        pygame.init()
        # Initialise game window
        pygame.display.set_caption('GeeksforGeeks Snakes')
        self.game_window = pygame.display.set_mode((window_x, window_y))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()
        self.done=False
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
        
        # Vart ormens huvud är
        headx = self.snake_position[0]
        heady = self.snake_position[1]
        
        # Vart ormens kropp är
        snakeLength = len(self.snake_body) #todo:kom på hur man kan säga vart kroppen är, Längden på ormen tills dess 
        
        # Vart frukten finns
        fruitx = self.fruit_position[0]
        fruity = self.fruit_position[1]
        
        # Hur långt ifrån frukten huvudet är
        fruitdist = math.sqrt( ((headx-fruitx)**2) + ((heady-fruity)**2) )
        
        # Vilken riktning ormen rör sig åt
        snakeDirection = self.direction
        
        self.observation = [headx, heady, snakeLength, fruitx, fruity, fruitdist, snakeDirection, self.timeSinceFruit]
        self.observation = np.array(self.observation)
        
        self.info = {}

        return self.observation, self.info
    
    def close(self):
        pygame.quit()