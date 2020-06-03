# -*- coding: utf-8 -*-
from flask import Flask, render_template,request
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd1234'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            message = ws.wait()
            ws.send(message)
    return

if __name__ == '__main__':
    # socketio.run(app.run(host='0.0.0.0',port=8000), debug=False) #  we define 0.0.0.0 as global ip
    http_server = WSGIServer(('0.0.0.0',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
# if server already run use sudo kill -9 'PID'
# check port listen by lsof -i :port number