from flask import Flask, request, render_template, Response
from app.opencv_streaming import VideoCamera
from flask_socketio import SocketIO, emit
from threading import Thread


# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Indaboski Bahose#'
socketio = SocketIO(app)

# thread
thread = Thread()


@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('connect', namespace='/web')
def connect_web():
    emit('my response', {'data': 'Connected'})



@socketio.on('disconnect', namespace='/web')
def disconnect_web():
    print ('[INFO] Web client disconnected: {}'.format(request.sid))


def gen(opencv_streaming):
    while True:
        frame = opencv_streaming.get_frame()
        emit('stream', {
                'image': frame
            }, namespace='/web')


@socketio.on('video feed', namespace='/web')
def video_feed (data):
    # need visibility of the global thread object
    global thread
    video_url = data['src']

    print('Client connected: {}'.format(video_url))
    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = gen(VideoCamera(video_url))
        thread.start()


if __name__ == '__main__':
    socketio.run(host='0.0.0.0', debug=True)