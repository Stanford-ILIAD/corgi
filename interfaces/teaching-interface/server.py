import numpy as np
import io
import socketio
from aiohttp import web
from src import utils
import random
from collections import defaultdict
from experiment import DrawingExperiment
from urllib.parse import parse_qs

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


experiments = defaultdict(list)

async def index(request):
    path = request._message.path[2:]
    parsed = parse_qs(path)
    if('username' in parsed and 'mode' in parsed):
        username = parsed['username'][0]
        mode = parsed['mode'][0]
        experiments[username].append(DrawingExperiment(username, mode))
        with open("index.html") as f:
            return web.Response(text=f.read(), content_type='text/html')
    else:
        with open("invalid.html") as f:
            return web.Response(text=f.read(), content_type='text/html')

@sio.on('start_finish')
async def start_finish(sid, message):
    print("Finishing..")
    username = message["username"]
    drawing = message["drawing"]
    experiment = experiments[username][-1]
    score, feedback = experiment.add_drawing(drawing)
    # save user experiment log
    experiment.save()
    await sio.emit('endData', {"score_3":str(score)+"%"}, to=sid)
    
@sio.on('get_feedback_2')
async def get_feedback_2(sid, message):
    username = message["username"]
    drawing = message["drawing"]
    experiment = experiments[username][-1]
    score, feedback = experiment.add_drawing(drawing)
    await sio.emit('respond_feedback_2', {"feedback_2":feedback, "score_2":str(score)+"%"}, to=sid)
    
@sio.on('get_feedback_1')
async def get_feedback_1(sid, message):
    username = message["username"]
    drawing = message["drawing"]
    experiment = experiments[username][-1]
    score, feedback = experiment.add_drawing(drawing)
    print("feedback 1 getting!")
    await sio.emit('respond_feedback_1', {"feedback_1":feedback, "score_1":str(score)+"%"}, to=sid)
    
@sio.on('start')
async def start(sid, message):
    print("start")
    username = message["username"]
    experiment = experiments[username][-1]
    await sio.emit('start_traj_1', {}, to=sid)


app.router.add_get('/', index)
app.router.add_static('/static/',
                          path='./static/',
                          name='static')
if __name__ == '__main__':
    web.run_app(app)
    

