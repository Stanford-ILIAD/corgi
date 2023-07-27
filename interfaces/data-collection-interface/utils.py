import torch
import numpy as np
import random
random.seed(0)

def get_domain(input_string):
    domain_dict = {"walk":"humanoid",
                   "jump":"humanoid",
                   "throw":"humanoid",
                   "run":"humanoid",
                   "wave":"humanoid",
                   "jacks":"humanoid",
                   "bengali":"writing",
                   "burmese":"writing",
                   "arabic":"writing",
                   "japanese":"writing",
                   "futurama":"writing",
                   "car":"parking",
                   "bike":"parking",
                   "plane":"parking"}
    for key in domain_dict.keys():
        if (key in input_string):
            return domain_dict[key]
    else:
        print("Coulnd't find domain for: "+input_string)
        return None
    
def format_trajectory_filename(input_fn):
    domain = get_domain(input_fn)
    if(domain == "humanoid" or domain == "parking"):
        return input_fn + ".gif"
    elif(domain == "writing"):
        return input_fn + ".txt"
    else:
        return None
    
    
def stitch_embeddings(embeddings_list, dimension):
    concat = torch.cat(embeddings_list, dim=1)
    return concat

def get_num_dim(embeddings_list, dimension):
    num_dim = 0
    for emb in embeddings_list:
        num_dim += emb.shape[dimension]
    return num_dim


def load_omniglot_traj(fn):
    motor = []
    with open(fn,'r') as fid:
        lines = fid.readlines()
    lines = [l.strip() for l in lines]
    for myline in lines:
        if myline =='START': # beginning of character
            stk = []
        elif myline =='BREAK': # break between strokes
            stk = np.array(stk)
            infill_stk = infill_action_trajectory(stk,dim=2)
            motor.append(infill_stk) # add to list of strokes
            stk = [] 
        else:
            arr = np.fromstring(myline,dtype=float,sep=',')
            stk.append(arr[:2])
    #return sum of all motors
    return np.concatenate(motor)

def get_omniglot_actions(trajectory):
    """only return first 300 actions"""
    actions = []
    curr_state = [trajectory[0][0], trajectory[0][1]]
    for i in range(0, len(trajectory), 2):
        actions.append([trajectory[i][0]-curr_state[0], trajectory[i][1]-curr_state[1]])
        curr_state = [trajectory[i][0], trajectory[i][1]]
    while(len(actions) < 150):
        actions.append([0,0])
    return actions

def infill_action_trajectory(trajectory, dim=2):
    """actually for strokes"""
    infilled_trajectory = []
    if(len(trajectory) == 1):
        return trajectory
    for i in range(len(trajectory)-1):
        action_1 = trajectory[i]
        action_2 = trajectory[i+1]
        dist = np.abs(np.linalg.norm(np.array(action_1) - np.array(action_2), np.inf))
        infilled_trajectory.append(action_1)
        for scale_term in range(1,int(dist),1):
            scaling = scale_term*(1/int(dist))
            new_action = action_1.copy()
            for d in range(dim):
                new_action[d] += (action_2[d]-action_1[d])*scaling
            infilled_trajectory.append(new_action)
        infilled_trajectory.append(action_2)
    return infilled_trajectory