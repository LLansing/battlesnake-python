import bottle
import os
import random



@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():

    last_move = 'up'
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FFFFFF',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    tail = data["you"]["body"]["data"][-1]
    head = data["you"]["body"]["data"][0]

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    
    hx = head["x"]
    hy = head["y"]
    tx = tail["x"]
    ty = tail["y"]
    
    x_diff = hx - tx
    y_diff = hy - ty
    
    if x_diff > 0 and check_move(hx - 1, hy, data):
            direction = 'left'
    elif x_diff < 0 and check_move(hx + 1, hy, data):
            direction = 'right'
    elif y_diff > 0 and check_move(hx, hy - 1, data):
            direction = 'up'
    else:
        direction = random.choice(directions)
    #elif y_diff < 0 and check_move(hx, hy + 1, data):
    #        direction = 'down'
    #else:
    #    if check_move(hx + 1, hy, data):
    #        direction = 'right'
    #    elif check_move(hx - 1, hy, data):
    #        direction = 'left'
    #    elif check_move(hx, hy - 1, data):
    #        direction = 'up'
    #    elif check_move(hx, hy + 1, data):
    #        direction = 'down'
    #    else:
    #        direction = random.choice(directions)
            

      
    print direction
    return {
        'move': direction,
        'taunt': 'Kachow'
    }
    
def check_move(ourx, oury, data):
    if ourx >= board_width or ourx < 0:
        return false
    if oury >= board_height or oury < 0:
        return false
    #for s in data["snakes"]["data"]:
    #    for sb in s["body"]["data"]:
    #        if(sb.x == ourx and sb.y == oury):
    #            return false
    return true
    
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
