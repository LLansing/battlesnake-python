import bottle
import os
import random



@bottle.route('/')
def static():
    return 'the server is running'


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():

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

    tail = data['you']['body']['data'][-1]
    head = data['you']['body']['data'][0]

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    hc_x_diff = data.get('width')
    hc_y_diff = data.get('height')
    c_tot_diff = hc_x_diff + hc_y_diff
    
    hx = head['x']
    hy = head['y']
    tx = tail['x']
    ty = tail['y']
    
    ht_x_diff = hx - tx
    ht_y_diff = hy - ty
    
    if data.get('you').get('health') < 61 :
        for crumb in data.get('food').get('data'):
            xtemp = hx - crumb.get('x')
            ytemp = hy - crumb.get('y')
            temp_tot = abs(xtemp) + abs(ytemp)
            if temp_tot <= c_tot_diff:
                hc_x_diff = xtemp
                hc_y_diff = ytemp
                c_tot_diff = temp_tot
        direction = set_direction(hc_x_diff, hc_y_diff, hx, hy, data)
    else:
        direction = set_direction(ht_x_diff, ht_y_diff, hx, hy, data)
      
    print direction
    return {
        'move': direction,
        'taunt': 'Kachow'
    }
def set_direction(x_diff, y_diff, hx, hy, data):
    if x_diff > 0 and check_move(hx - 1, hy, data):
            return 'left'
    elif x_diff < 0 and check_move(hx + 1, hy, data):
            return 'right'
    elif y_diff > 0 and check_move(hx, hy - 1, data):
            return 'up'
    elif y_diff < 0 and check_move(hx, hy + 1, data):
            return 'down'
    else:
        if check_move(hx - 1, hy, data):
            return 'left'
        if check_move(hx + 1, hy, data):
            return 'right'
        if check_move(hx, hy - 1, data):
            return 'up'
        if check_move(hx, hy + 1, data):
            return 'down'
    return random.choice(['up', 'down', 'left', 'right'])
    
def check_move(ourx, oury, data):
    
    board_width = data.get('width')
    board_height = data.get('height')
    if ourx >= board_width or ourx < 0 or oury >= board_height or oury < 0:
        return 0
    #if ourx == ourbody[1].get('x') and oury ==  ourbody[1].get('y'):
    #    return 0
    
    for seg in data['you']['body']['data']:
        if seg['x'] == ourx and seg['y'] == oury:
            return 0
    #for snek in data['snakes']['data']:
        #if abs(snek['body']['data'][0]['x'] - ourx) +  abs(snek['body']['data'][0]['y'] - oury) == 1:
        #    return 0 
        
    #for snek in data.get('snakes').get('data'):
    #    for bod_seg in snek.get('body').get('data'):
    #        if bod_seg.get('x') == ourx and bod_seg.get('y') == oury:
    #            return 0
    for s in data['snakes']['data']:
        s_x = s['body']['data'][0].get('x')
        s_y = s['body']['data'][0].get('y')
        if abs((ourx - s_x) +  (oury - s_y)) == 1:
            return 0
        for sb in s['body']['data']:
            if sb['x'] == ourx and sb['y'] == oury:
                return 0
    return 1
    
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
