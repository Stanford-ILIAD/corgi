const socket =  io('http://localhost:8080');
var params = new URLSearchParams(location.search);
var username = params.get('username')
var current_drawing = []
var canvasvar_1 = document.getElementById("student-canvas-1");
var contextvar_1 = canvasvar_1.getContext("2d");
var canvasvar_2 = document.getElementById("student-canvas-2");
var contextvar_2 = canvasvar_2.getContext("2d");
var canvasvar_3 = document.getElementById("student-canvas-3");
var contextvar_3 = canvasvar_3.getContext("2d");


window.onload = event => {
    enable_start_button();
  };


function start_finish() {
    disable_drawing();
    socket.emit('start_finish',{'username':username, 'drawing':current_drawing})
    current_drawing = []
}

function start_feedback_2() {
    document.getElementById("model-score-header-2").hidden = false;
    document.getElementById("model-score-2").hidden = false;
    document.getElementById("model-feedback-2").hidden = false;
    disable_drawing();
    socket.emit('get_feedback_2',{'username':username, 'drawing':current_drawing})
    current_drawing = []
}


function start_feedback_1() {
    document.getElementById("model-score-header-1").hidden = false;
    document.getElementById("model-score-1").hidden = false;
    document.getElementById("model-feedback-1").hidden = false;
    disable_drawing();
    socket.emit('get_feedback_1',{'username':username, 'drawing':current_drawing})
    current_drawing = []
}

function enable_start_button() {
    document.getElementById("start-button").disabled = false;
}

function start() {
    socket.emit('start',{'username':username})
    document.getElementById("start-button").disabled = true;
    contextvar_1.drawImage(imageObj,150,150);
    contextvar_2.drawImage(imageObj,150,150);
    contextvar_3.drawImage(imageObj,150,150);
}

socket.on('respond_feedback_1', function(data) {
    console.log(data["feedback_1"])
    document.getElementById("model-score-1").innerHTML = data["score_1"];
    document.getElementById("model-feedback-1").innerHTML = data["feedback_1"];
    document.getElementById("feedback-button-2").disabled = false;
    document.getElementById("canvas-title-2").style.color = "black"
    document.getElementById("feedback-button-1").disabled = true;
    document.getElementById("canvas-title-1").style.color = "white"
    active_canvas = document.getElementById('student-canvas-2')
    enable_drawing();
});

socket.on('respond_feedback_2', function(data) {
    console.log(data["feedback_2"])
    document.getElementById("model-score-2").innerHTML = data["score_2"];
    document.getElementById("model-feedback-2").innerHTML = data["feedback_2"];
    document.getElementById("finish-button").disabled = false;
    document.getElementById("canvas-title-3").style.color = "black"
    document.getElementById("feedback-button-2").disabled = true;
    document.getElementById("canvas-title-2").style.color = "white"
    active_canvas = document.getElementById('student-canvas-3')
    enable_drawing();
});

var mouse_clicked = false;
var active_canvas = null;

function enable_drawing() {
    active_canvas.style.border = "8px rebeccapurple solid";
    active_canvas.addEventListener('pointermove', pointer_move, false);
    active_canvas.addEventListener('pointerdown', pointer_down, false);
    active_canvas.addEventListener('pointerup', pointer_up, false);
}

function disable_drawing() {
    active_canvas.style.border = "8px lavender solid";
    active_canvas.removeEventListener('pointermove', pointer_move);
    active_canvas.removeEventListener('pointerdown', pointer_down);
    active_canvas.removeEventListener('pointerup', pointer_up);
    mouse_clicked = false;
    active_canvas = null;
}

function getMousePosition(drawing_canvas, event) {
    let rect = drawing_canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    x = (x / rect.width)* drawing_canvas.width;
    y = (y / rect.height)* drawing_canvas.height;
    return [x,y]
}

function pointer_move(evt) {
    if(mouse_clicked && active_canvas) {
        var mousePos = getMousePosition(active_canvas, evt);
        a = [mousePos[0], mousePos[1]]
        active_canvas_context = active_canvas.getContext('2d')
        active_canvas_context.fillRect(a[0], a[1], 5, 5)
        current_drawing.push(a)
    }
}

function pointer_down(evt) {
    if(active_canvas) {
        mouse_clicked = true;
    }
}

function pointer_up(evt) {
    if(active_canvas) {
        mouse_clicked = false;
    }
}

socket.on('start_traj_1', function(data) {
    document.getElementById("feedback-button-1").disabled = false;
    document.getElementById("canvas-title-1").style.color = "black"
    active_canvas = document.getElementById('student-canvas-1')
    enable_drawing();
});

socket.on('endData', function(data) {
    alert("Thank you! You are done :) Your final score is "+data["score_3"]);
    document.getElementById("finish-button").disabled = true;
});