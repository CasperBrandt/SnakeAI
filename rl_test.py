from stable_baselines3 import PPO
from snakeEnv import SnakeEnv

models_dir = "models/PPO"
model_path = f"{models_dir}/50000.zip"

env = SnakeEnv(render_mode='human')

model = PPO.load(model_path, env=env, device='cpu')

for ep in range(10):
    obs, _ = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        
env.close()