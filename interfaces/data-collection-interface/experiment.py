import random
import pickle
import time

class CorrectionExperiment:
    def __init__(self, username, motor_pairs):
        self.username = username
        self.motor_pairs = motor_pairs
        self.curr_student_key = ""
        self.curr_expert_key = ""
        self.curr_student_val = [0,0]
        self.curr_expert_val = [0,0]
        self.corrections = []
        self.experiment_end = False
        
    def set_random_motor_pair(self):
        random_pair = random.choice(list(self.motor_pairs))
        student_key = random_pair[0]
        expert_key = random_pair[1]
        self.curr_student_key  = student_key
        self.curr_expert_key = expert_key
        
    def reset_experiment(self):
        print("Reset Experiment")
        self.set_random_motor_pair()
        self.curr_student_val = [0,0]
        self.curr_expert_val = [0,0]
    
    def add_correction(self, correction_num, correction_text, student_key, expert_key):
        self.corrections.append((correction_num, correction_text, student_key, expert_key))
        print((correction_num, correction_text, student_key, expert_key))
        print(len(self.corrections))
        
    def save(self):
        self.experiment_end = True
        save_fn = "logs/"+self.username+"_"+time.strftime("%Y%m%d-%H%M%S")+".log"
        with open(save_fn, 'w') as f:
            for c in self.corrections:
                f.write(f"{c}\n")
        
        
    
    