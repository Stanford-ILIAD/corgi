# Generating Language Corrections for Teaching Physical Control Tasks

Authors: Megha Srivastava (@meghabyte), Noah Goodman, and Dorsa Sadigh

This repository contains the code for the ICML 2023 paper "Generating Language Corrections for Teaching Physical Control Tasks". 
In this work we design and build CORGI, a model trained to generate language corrections for three diverse physical control tasks (drawing, steering, and joint movement). CORGI takes in as input a pair of student and expert trajectories, and then generates natural language corrections to help the student improve. To train CORGI, we collect over 2k  crowdsourced corrections for pair-wise (student, expert) trajectories, and further augment the data with large language-model (LLM) assistance. 

If you find this respository useful, please cite:

```
@InProceedings{corgi2023srivastava,
  title = 	 {Generating Language Corrections for Teaching Physical Control Tasks},
  author = 	 {Srivastava, Megha and Goodman, Noah and Sadigh, Dorsa},
  booktitle	=   {International Conference on Machine Learning (ICML)},
  year = 	 {2023},
}
```

## Interface
We provide code for user study interfaces to aid reproducibility of our experiment. Specifically:
* ```interfaces/teaching-interface/``` contains source code for the learning gain experiment for the Drawing task
* Other interfaces: Coming soon! 


## Data
We provide data used to train CORGI. Specifically:
* ```data/data.json``` contains the raw crowdsourced data without any data augmentation
* ```data/resources/``` contains gif files corresponding to movements shown during crowdsourcing for entries in ```data.json```

## Environments
Coming soon!

## Model 
Coming soon!
