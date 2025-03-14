import time  
import gymnasium as gym 
import numpy as np 
from gym_robotics_custom import RoboGymObservationWrapper
from buffer import ReplayBuffer 
from model import * 
from agent import Agent
if __name__ == '__main__':
    env_name = "FrankaKitchen-v1"
    max_episode_steps = 500
    task = 'microwave'
    replay_buffer_size = 1000000
    task_no_spaces = task.replace(" ", "_")
    gamma = 0.99 
    alpha = 0.1 
    tau = 0.05
    target_update_interval = 1 
    hidden_size = 512
    learning_rate = 0.0001
    batch_size = 64 
    updates_per_steps = 4 
    
    
    env = gym.make(env_name, max_episode_steps, max_episode_steps, tasks_to_complete = [task])
    env = RoboGymObservationWrapper(env, goal =task)
    
    observation, info = env.reset() 
    observation_size = observation.shape[0]
    
    agent = Agent(observation_size, env.action_space, gamma = gamma, tau = tau,
                  alpha = alpha , target_update_interval = target_update_interval,
                  hidden_size = hidden_size, learning_rate = learning_rate, goal = task_no_spaces)

    memory = ReplayBuffer(replay_buffer_size, input_size = observation_size,
                          n_actions = env.action_space.shape[0], augment_rewards = True, augment_data = True)
    
    memory.load_from_csv(filename=f"checkpoint/human_memory_{task_no_spaces}.npz")
    time.sleep(2)
    
    #Phase 1
    memory.expert_data_ratio = 0.5 
    agent.train(env = env, memory = memory, episodes =150,
                batch_size = batch_size , updates_per_steps = updates_per_steps,
                summaery_writer_name = f"live_train_phase1_{task_no_spaces}",
                max_episodes_steps = max_episodes_steps)
    
    #Phase 2
    memory.expert_data_ratio = 0.25 
    agent.train(env = env, memory = memory, episodes =250,
                batch_size = batch_size , updates_per_steps = updates_per_steps,
                summaery_writer_name = f"live_train_phase1_{task_no_spaces}",
                max_episodes_steps = max_episodes_steps)
    
    #Phase 1
    memory.expert_data_ratio = 0.
    agent.train(env = env, memory = memory, episodes =1000,
                batch_size = batch_size , updates_per_steps = updates_per_steps,
                summaery_writer_name = f"live_train_phase1_{task_no_spaces}",
                max_episodes_steps = max_episodes_steps)