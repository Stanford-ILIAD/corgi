# Generating Language Corrections for Teaching Physical Control Tasks

Authors: Megha Srivastava (@meghabyte), Noah Goodman, and Dorsa Sadigh

This repository contains the code for the ICML 2023 paper *"Generating Language Corrections for Teaching Physical Control Tasks"*. 
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
* ```interfaces/teaching-interface/``` contains source code for the learning gain experiment for the Drawing task.
* ```interfaces/data-collection-interface/``` contains source code for the our data collection process. It is currently set-up for the Drawing task, but easily adaptable to any task where the data type consists of trajectories (sequence of states/actions).

To run each interface, simple run ```python server.py```, and direct your browser to ```http://localhost:8080/?username=username```.


## Data
We provide data used to train CORGI. Specifically:
* ```data/resources/``` contains gif files corresponding to movements shown during crowdsourcing for entries in ```data.json```
* ```data/data.json``` contains the raw crowdsourced data without any data augmentation. These include fun and metaphorical examples across the different physical control tasks, such as:
  - Drawing: _"make picture narrower and the end curl like a musical note"_, _"make the loop more like a sidewards sharks fin"_
  - Steering: _"be brave dont be afraid dont stop"_
  - Movement: _"softer landing needed"_, _"be more fluent in your movements"_


## Model 
Please contact  ```megha@cs.stanford.edu```, as the file is too large! 
