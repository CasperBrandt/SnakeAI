from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
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

eval_env = SnakeEnv()
eval_callback = EvalCallback(eval_env, best_model_save_path=models_dir, eval_freq=10000, deterministic=True, render=False)

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir, device='cpu')
#model = PPO.load(model_path, env=env, device='cpu') # Swap to this line if you wanna start training a pre-existing modell

TIMESTEPS = 50000
while True:
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, callback=eval_callback, tb_log_name="PPO")