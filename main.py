import os
import eventlet
import socketio

from config.timer import TimeoutThread
from core.position import Position
from core.scene import Scene
from game.action import Action
from game.player import Player
from script.movement import Movement

sio = socketio.Server()
app = socketio.WSGIApp(sio)

scene = Scene()
players = dict({})

@sio.on('message')
def print_message(sid: str, message: str):
    print('Socket ID:', sid)
    print('Message:', message)

@sio.event
def connect(sid: str, environ):
    player = Player(sid)
    players[sid] = player
    print(f'Player connected: {sid}')
    sio.emit('connected', sid)

@sio.event
def disconnect(sid: str):
    player: Player = players[sid]
    if player != None:
        scene.remove(player)
        players.pop(sid)
        print(f'Player disconnected: {sid}')

@sio.on('player:initialize')
def initialize_player(sid: str, data = ''):
    player: Player = players[sid]
    if player != None:
        movement: Movement = player.get('Movement')
        movement.position = Position(0, 10, 0)
        scene.add(player)
        def send_player_position():
            sio.emit('player:moved', {
                'position': {
                    'x': movement.position.x,
                    'y': movement.position.y,
                    'z': movement.position.z
                },
                'direction': movement.direction,
                'status': movement.status
            })
        movement.on_updated.append(send_player_position)
        sio.emit('player:initialized', {
            'position': {
                'x': movement.position.x,
                'y': movement.position.y,
                'z': movement.position.z
            },
            'direction': movement.direction,
            'status': movement.status
        })

@sio.on('player:move')
def move_player(sid: str, action: str):
    player: Player = players[sid]
    if player != None:
        movement: Movement = player.get('Movement')
        movement.action = action
        def reset_action():
            last_scheduler: TimeoutThread = movement.scheduler
            last_scheduler.stop()
            movement.action = Action.STAND
        movement.scheduler = TimeoutThread(target=reset_action, timeout=500)
        movement.scheduler.setName(f'#{player.player_id}-{movement.action}')
        movement.scheduler.start()
    print(f'Player move: {action}')

if __name__ == '__main__':
    try:
        eventlet.wsgi.server(eventlet.listen(('localhost', int(os.environ['PORT']))), app)
    except Exception as ex:
        print(ex)
        scene.stop()