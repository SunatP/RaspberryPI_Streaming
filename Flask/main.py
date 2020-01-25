# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd1234'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app.run(host='0.0.0.0',port=8081), debug=True) #  we define 0.0.0.0 as global ip

# if server already run use sudo kill -9 'PID'
# check port listen by lsof -i :port number