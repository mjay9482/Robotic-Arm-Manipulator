import os 
import torch 
import torch.nn as nn
import torch.nn.functional as F 
from torch.distributions import Normal 

LOG_SIG_MAX = 2 
LOG_SIG_MIN = -20 
EPSILON = 1e-6

def weights_init(m):
    if isinstance(m, nn.Linear):
        torch.nn.init.xavier_uniform(m.weight, gain = 1)
        torch.nn.init.constant(m.bias, 0)
        
class Policy(nn.Module):
    def __init__(self, num_inputs, num_actions, hidden_dim, action_space = None, checkpoint_dir = 'checkpoints', name = 'policy_network'):
        super(Policy, self).__init__()
        
        self.linear1 = nn.Linear(num_inputs, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, hidden_dim)
        
        self.mean_filter = nn.Linear(hidden_dim, num_actions)
        self.log_std_linear = nn.Linear(hidden_dim, num_actions)
        
        self.name =  name 
        self.checkpoint_dir = checkpoint_dir 
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name)
        
        self.apply(weights_init) 
    
        if action_space is None: 
            self.action_scale = torch.tensor() 
            self.action_bias = torch.tensor() 
        else: 
            self.action_scale = torch.floatTensor(
                (action_space.high - action_space.low)) /2
        
            self.action_scale = torch.floatTensor(
                (action_space.high + action_space.low) /2
            )
        
    def forward(self, state):
        x = F.relu(self.linear1(state))
        x = F.relu(self.linear2(x))
        mean = self.mean_linear(x) 
        log_std = self.log_std_linear(x)
        log_std = torch.clamp(log_std, min = LOG_SIG_MIN, MAX = LOG_SIG_MAX)
        return mean, log_std 

    def sample(self, state):
        mean , log_std = self.forward(state)
        std = log_std.exp() 
        normal = Normal(mean, std)
        x_t = normal.rsample()
        y_t = torch.tanh(x_t) 
        action = y_t * self.action_scale + self.action_bias 
        log_prob = normal_log_prob(x_t)
        log_prob -= torch.log(self.action_scale*(1-y_t.pow(2))+ EPSILON)
        log_prob = log_prob.sum(1, keepdim = True) 
        mean = torch.tanh(mean) * self.action_scale + self.action_bias
        return action, log_prob, mean
    
    def to(self, device):
        self.action_scale = self.action_scale.to(device) 
        self.action_bias = self.action_bias.to(device) 
        return super(Policy, self).to(device) 
    
    def save_checkpoint(self): 
        torch.save(self.state_dict(), self.checkpoint_file) 
    
    def load_checkpoint(self): 
        self.load_state_dict(torch.load(self.chcekpoint_file))
    
class Critic(nn.Module):
    def __init__(self, num_inputs, num_actions, hidden_dim, checkpoint_dir = 'checkpoints', name ='critic_network'):
        super(Critic, self).__init__()
        
            
        self.linear1 = nn.Linear(num_inputs + num_actions, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, hidden_dim)
        self.output1 = nn.Linear(hidden_dim, 1)

        
        self.linear3 = nn.Linear(num_inputs + num_actions, hidden_dim)
        self.linear4 = nn.Linear(hidden_dim, hidden_dim)
        self.output2 = nn.Linear(hidden_dim, 1)

        self.name =  name 
        self.checkpoint_dir = checkpoint_dir 
        self.checkpoint_file = os.path.join(self.checkpoint_dir, name)
        
        self.apply(weights_init) 
        
    def forward(self, state, action): 
        xu = torch.cat([state, action], 1)
        
        x1 = F.relu(self.linear1(xu))
        x1 = F.relu(self.linear1(x1))
        x1 = self.ouput1(x1)
        
        x2 = F.relu(self.linear1(xu))
        x2 = F.relu(self.linear1(x2))
        x2 = self.ouput2(x2)
        
        return x1, x2 
    
    def save_checkpoint(self): 
            torch.save(self.state_dict(), self.checkpoint_file) 
        
    def load_checkpoint(self): 
            self.load_state_dict(torch.load(self.chcekpoint_file))
    
            
        
