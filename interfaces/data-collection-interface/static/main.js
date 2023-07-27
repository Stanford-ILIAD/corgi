const socket =  io('http://localhost:8080'); 
var params = new URLSearchParams(location.search);
var username = params.get('username')
var expert_coord_x = 0;
var expert_coord_y = 0;
var student_coord_x = 0;
var student_coord_y = 0;
var timestep  = 0;
var correction_number = 0;

window.onload = event => {
    start();
  };


function clear_canvasi() {
    expert_canvas = document.getElementById('expert-canvas')
    const expert_ctx = expert_canvas.getContext('2d');
    expert_ctx.clearRect(0, 0, expert_canvas.width, expert_canvas.height);
    student_canvas = document.getElementById('student-canvas')
    const student_ctx = student_canvas.getContext('2d');
    student_ctx.clearRect(0, 0, student_canvas.width, student_canvas.height);
    document.getElementById('feedback').value="";
}
function start_correction() {
    timestep = 0;
    document.getElementById('nextbutton').value="submit ("+(correction_number+1)+"/10)";
    clear_canvasi();
    setInterval(get_draw_data, 25);
    document.getElementById("replay-button").style.background = "gray";
    document.getElementById("replay-button").disabled = true;
}

function enable_replay_correction() {
    clearInterval(get_draw_data);
    document.getElementById("replay-button").style.background = "orange";
    document.getElementById("replay-button").disabled = false;
}

function prepare_next_correction() {
    clearInterval(get_draw_data);
    timestep = 0;
    correction_number = correction_number + 1;
}

function get_draw_data() {
    timestep = timestep + 1;
    socket.emit('NextStep', {'timestep': timestep, 'username':username});
}

function draw_expert() {
    const ctx = document.getElementById('expert-canvas').getContext('2d');
    ctx.strokeStyle = 'rgba(0, 153, 255, 0.4)';
    ctx.save();
    ctx.fillRect((expert_coord_x), -expert_coord_y, 5, 5);
}

function draw_student() {
    const ctx = document.getElementById('student-canvas').getContext('2d');
    ctx.strokeStyle = 'rgba(0, 153, 255, 0.4)';
    ctx.save();
    ctx.fillRect((student_coord_x), -student_coord_y, 5, 5);
}

function submitCorrection() {
    var correction = document.getElementById("feedback").value
    confirmed = confirm("Are you sure you want to submit:\n \n"+correction+"?");
    if(confirmed) {
        prepare_next_correction();
        socket.emit('NextCorrection', {'correction_number':correction_number, 'correction_text':correction, 'username':username});
    }
}

function start() {
    socket.emit('NextCorrection',{'correction_number':correction_number, 'correction_text':'', 'username':username})
}

socket.on('showTraj', function(data) {
    if(data["is_end_correction"] && !data["is_end_experiment"] ) {
        enable_replay_correction();
    }
    else if (!data["is_end_experiment"]) {
        console.log("Show Trajectory");
        expert_coord_x = parseInt(data["expert_x"]);
        expert_coord_y = parseInt(data["expert_y"]);
        draw_expert();
        student_coord_x = parseInt(data["student_x"]);
        student_coord_y = parseInt(data["student_y"]);
        draw_student();
    }
});

socket.on('nextCorrection', function(data) {
    console.log('next correction')
    start_correction();
});

socket.on('endData', function(data) {
    clearInterval(get_draw_data);
    alert("Thank you! You are done :) Please close the window and fill out this survey form [REDACTED]");
    document.getElementById('nextbutton').disabled = true;
    document.getElementById("nextbutton").style.background = "gray";
    document.getElementById('replay-button').disabled = true;
    document.getElementById("replay-button").style.background = "gray";
});