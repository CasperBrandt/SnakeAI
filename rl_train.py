from stable_baselines3 import PPO
import os
from snakeEnv import SnakeEnv

models_dir = "models/PPO"
logdir = "logs"

#model_path = f"{models_dir}/450000.zip" # Swap to this line if you wanna start training a pre-existing modell, remember to change to the correct .zip

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    
if not os.path.exists(logdir):
    os.makedirs(logdir)
    
env = SnakeEnv()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device='cpu')
#model = PPO.load(model_path, env=env, device='cpu') # Swap to this line if you wanna start training a pre-existing modell

TIMESTEPS = 25000
i = 1
while True:
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")
    i += 1