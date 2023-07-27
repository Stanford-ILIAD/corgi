import numpy as np
import io
import socketio
from aiohttp import web
from src import utils
import random
from collections import defaultdict
from experiment import CorrectionExperiment
from urllib.parse import parse_qs

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


SCALE = 2
NUM_CORRECTIONS = 10
MOTOR_PAIRS = []
# Alphabet specifies the (student, expert) pairs to collect data over. 
# This interface currently covers the futuram dataset. 
ALPHABET = [('drawing/futurama/0341_05.txt', 'drawing/futurama/0341_expert.txt'), ('drawing/futurama/0330_05.txt', 'drawing/futurama/0330_expert.txt'), ('drawing/futurama/0341_12.txt', 'drawing/futurama/0341_expert.txt'), ('drawing/futurama/0341_13.txt', 'drawing/futurama/0341_expert.txt'), ('drawing/futurama/0330_03.txt', 'drawing/futurama/0330_expert.txt'), ('drawing/futurama/0330_16.txt', 'drawing/futurama/0330_expert.txt'), ('drawing/futurama/0341_02.txt', 'drawing/futurama/0341_expert.txt'), ('drawing/futurama/0327_19.txt', 'drawing/futurama/0327_expert.txt'), ('drawing/futurama/0334_02.txt', 'drawing/futurama/0334_expert.txt'), ('drawing/futurama/0334_03.txt', 'drawing/futurama/0334_expert.txt'), ('drawing/futurama/0336_12.txt', 'drawing/futurama/0336_expert.txt'), ('drawing/futurama/0326_01.txt', 'drawing/futurama/0326_expert.txt'), ('drawing/futurama/0338_15.txt', 'drawing/futurama/0338_expert.txt'), ('drawing/futurama/0338_01.txt', 'drawing/futurama/0338_expert.txt'), ('drawing/futurama/0331_19.txt', 'drawing/futurama/0331_expert.txt'), ('drawing/futurama/0333_08.txt', 'drawing/futurama/0333_expert.txt'), ('drawing/futurama/0349_01.txt', 'drawing/futurama/0349_expert.txt'), ('drawing/futurama/0326_14.txt', 'drawing/futurama/0326_expert.txt'), ('drawing/futurama/0331_08.txt', 'drawing/futurama/0331_expert.txt'), ('drawing/futurama/0336_01.txt', 'drawing/futurama/0336_expert.txt'), ('drawing/futurama/0336_15.txt', 'drawing/futurama/0336_expert.txt'), ('drawing/futurama/0349_05.txt', 'drawing/futurama/0349_expert.txt'), ('drawing/futurama/0338_05.txt', 'drawing/futurama/0338_expert.txt'), ('drawing/futurama/0338_11.txt', 'drawing/futurama/0338_expert.txt'), ('drawing/futurama/0336_14.txt', 'drawing/futurama/0336_expert.txt'), ('drawing/futurama/0326_13.txt', 'drawing/futurama/0326_expert.txt'), ('drawing/futurama/0349_06.txt', 'drawing/futurama/0349_expert.txt'), ('drawing/futurama/0349_12.txt', 'drawing/futurama/0349_expert.txt'), ('drawing/futurama/0334_06.txt', 'drawing/futurama/0334_expert.txt'), ('drawing/futurama/0334_12.txt', 'drawing/futurama/0334_expert.txt'), ('drawing/futurama/0326_12.txt', 'drawing/futurama/0326_expert.txt'), ('drawing/futurama/0331_07.txt', 'drawing/futurama/0331_expert.txt'), ('drawing/futurama/0333_16.txt', 'drawing/futurama/0333_expert.txt'), ('drawing/futurama/0336_19.txt', 'drawing/futurama/0336_expert.txt'), ('drawing/futurama/0349_09.txt', 'drawing/futurama/0349_expert.txt'), ('drawing/futurama/0338_09.txt', 'drawing/futurama/0338_expert.txt'), ('drawing/futurama/0331_11.txt', 'drawing/futurama/0331_expert.txt'), ('drawing/futurama/0326_19.txt', 'drawing/futurama/0326_expert.txt'), ('drawing/futurama/0334_19.txt', 'drawing/futurama/0334_expert.txt'), ('drawing/futurama/0333_10.txt', 'drawing/futurama/0333_expert.txt'), ('drawing/futurama/0333_05.txt', 'drawing/futurama/0333_expert.txt'), ('drawing/futurama/0333_12.txt', 'drawing/futurama/0333_expert.txt'), ('drawing/futurama/0331_03.txt', 'drawing/futurama/0331_expert.txt'), ('drawing/futurama/0330_19.txt', 'drawing/futurama/0330_expert.txt'), ('drawing/futurama/0327_12.txt', 'drawing/futurama/0327_expert.txt'), ('drawing/futurama/0327_13.txt', 'drawing/futurama/0327_expert.txt'), ('drawing/futurama/0327_11.txt', 'drawing/futurama/0327_expert.txt'), ('drawing/futurama/0327_05.txt', 'drawing/futurama/0327_expert.txt'), ('drawing/futurama/0330_08.txt', 'drawing/futurama/0330_expert.txt'), ('drawing/futurama/0341_08.txt', 'drawing/futurama/0341_expert.txt')]
experiments = defaultdict(list)



def load_all_motors():
    motors = {}
    for student_fn, expert_fn in ALPHABET:
        student_motor_key = student_fn.split(".txt")[0]
        expert_motor_key = expert_fn.split(".txt")[0]
        MOTOR_PAIRS.append((student_motor_key, expert_motor_key))
        if(student_motor_key not in motors.keys()):
            motors[student_motor_key] = utils.get_omniglot_actions(utils.load_omniglot_traj("../../data/resources/"+student_fn))
        if(expert_motor_key not in motors.keys()):
            motors[expert_motor_key] = utils.get_omniglot_actions(utils.load_omniglot_traj("../../data/resources/"+expert_fn))
    return motors

motors = load_all_motors()


def get_motor(username):
    experiment = experiments[username][-1]
    student_motor = motors[experiment.curr_student_key]
    expert_motor = motors[experiment.curr_expert_key]
    return student_motor, expert_motor
    

async def index(request):
    path = request._message.path[2:]
    parsed = parse_qs(path)
    if('username' in parsed):
        username = parsed['username'][0]
        experiments[username].append(CorrectionExperiment(username, MOTOR_PAIRS))
        with open("index.html") as f:
            return web.Response(text=f.read(), content_type='text/html')
    else:
        with open("invalid.html") as f:
            return web.Response(text=f.read(), content_type='text/html')


@sio.on('NextStep')
async def next_step(sid, message):
    timestep = message['timestep']
    username = message["username"]
    experiment = experiments[username][-1]
    student_motor, expert_motor = get_motor(username)
    is_end = False
    if(timestep <= 1):
        experiment.curr_student_val = [200,-150] 
        experiment.curr_expert_val = [200,-150]  
    if(timestep < len(expert_motor)):
        experiment.curr_expert_val[0] += expert_motor[timestep][0]*SCALE
        experiment.curr_expert_val[1] += expert_motor[timestep][1]*SCALE
    if(timestep < len(student_motor)):
        experiment.curr_student_val[0] += student_motor[timestep][0]*SCALE
        experiment.curr_student_val[1] += student_motor[timestep][1]*SCALE
    if(timestep >= len(expert_motor) and timestep >= len(student_motor)):
        is_end_correction = True
    else:
        is_end_correction = False
    await sio.emit('showTraj',{'expert_x':experiment.curr_expert_val[0],
                               'expert_y':experiment.curr_expert_val[1],
                               'student_x':experiment.curr_student_val[0],
                               'student_y':experiment.curr_student_val[1],
                               "is_end_correction":is_end_correction,
                               "is_end_experiment":experiment.experiment_end}, to=sid)
    
@sio.on('NextCorrection')
async def next_correction(sid, message):
    print("next"+str(message))
    experiment = experiments[message["username"]][-1]
    if(message['correction_number'] >= NUM_CORRECTIONS):
        experiment.add_correction(message['correction_number'], message['correction_text'], experiment.curr_student_key,experiment.curr_expert_key)
        experiment.save()
        await sio.emit('endData', {}, to=sid)
    else:
        if(message['correction_number'] > 0):
            print("Added Correction!")
            experiment.add_correction(message['correction_number'], message['correction_text'], experiment.curr_student_key,experiment.curr_expert_key)
            experiment.reset_experiment()     
            await sio.emit('nextCorrection', {}, to=sid)
        else:
            experiment.reset_experiment()     
            await sio.emit('nextCorrection', {}, to=sid)
#instructions
#test
app.router.add_get('/', index)
app.router.add_static('/static/',
                          path='./static/',
                          name='static')
if __name__ == '__main__':
    web.run_app(app)


