import random
import pickle
import time
import generator

class DrawingExperiment:
    def __init__(self, username, mode):
        self.username = username
        self.mode = mode #should be red(score_only), blue(random_feedback), green(model_feedback)
        self.trajectories = []
        self.scores = []
        self.feedbacks = []
        self.experiment_end = False
        
    def add_drawing(self, drawing):
        self.trajectories.append(drawing)
        feedback, score = self.feedback(drawing)
        self.scores.append(score)
        print(self.scores)
        self.feedbacks.append(feedback)
        print(self.feedbacks)
        return score, feedback
        
    def feedback(self, drawing):
        if (self.mode == "blue"):
            model_feedback, score = generator.get_feedback(drawing,  temperature=0.7, random_val=random.choice([1, 2]))
            return model_feedback, score
        elif (self.mode == "red"):
            model_feedback, score = generator.get_feedback(drawing,  temperature=0.7, score_only=True)
            return model_feedback, score
        else:
            print("Model feedback!")
            model_feedback, score = generator.get_feedback(drawing,  temperature=0.7, random_val=0)
            return model_feedback, score
         
    def save(self):
        self.experiment_end = True
        save_fn = "logs/drawing_data_"+self.mode+"_"+self.username+"_"+time.strftime("%Y%m%d-%H%M%S")+".pkl"
        with open(save_fn, 'wb') as f:
            pickle.dump((self.trajectories, self.scores, self.feedbacks), f)
        
        
    
    