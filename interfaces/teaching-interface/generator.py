"""
    Dummy generator.py skeleton for experiment set-up. 
    Can replace score / correction in get_feedback() with model outputs. 
"""

import torch
import random
import numpy as np


random.seed(0)
np.random.seed(0)
torch.manual_seed(0)



def adjust_trajectory(user_trajectory):
    first_tuple = user_trajectory[0]
    z = [[ui[0]-first_tuple[0], first_tuple[1]-ui[1]] for ui in user_trajectory]
    return z
    
    
def get_feedback(user_trajectory, temperature=0.5, random_val=0, score_only=False):
    user_trajectory = adjust_trajectory(user_trajectory)
    score = -1
    if (score_only):
        return "", score
    if(random_val == 1):
        return "RANDOM", score
    elif(random_val == 2):
        return "RANDOM", score
    else:
        return "MODEL OUTPUT", score