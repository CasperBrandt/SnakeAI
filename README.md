# Snake AI using Proximal Policy Optimization (PPO)

A reinforcement learning implementation to play Snake using PPO algorithm from Stable Baselines3 with a custom Gymnasium environment.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Observation Space](#observation-space)
- [Reward Function](#reward-function)
- [Possible Improvements](#possible-improvements)
- [References](#references)

## Prerequisites
- Python 3.8+
- Pygame
- Stable Baselines3
- Gymnasium
- PyTorch
- TensorBoard

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## File Structure
```
├── snakeEnv.py           # Custom Snake environment implementation
├── rl_train.py          # Training script for PPO agent
├── rl_test.py           # Testing script for trained models
├── requirements.txt     # Python dependencies
└── models/              # Directory for saved models (auto-created)
└── logs/                # Directory for TensorBoard logs (auto-created)
```

## Usage

### Training
```bash
python rl_train.py
```
- Saves model checkpoints every 25,000 timesteps in `models/PPO/`
- TensorBoard logs available in `logs/`
```bash
tensorboard --logdir=logs
```

### Testing
```bash
python rl_test.py
```
- Modify `model_path` in rl_test.py to use different checkpoints
- Renders game window with 10 episodes

## Observation Space
8-dimensional vector containing:
- Snake head X/Y coordinates
- Current snake length
- Fruit X/Y coordinates
- Euclidean distance to fruit
- Current movement direction
- Time since last fruit eaten

## Reward Function
- `+10` for eating fruit
- Score multiplied by snake length for survival
- `-10` penalty for:
  - Hitting walls/body
  - Failing to eat fruit for >20+length steps

## References
- [Stable Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [PPO Paper](https://arxiv.org/abs/1707.06347)