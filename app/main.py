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
        'color': '#30005B',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    tail = data['you']['body']['data'][-1]
    head = data['you']['body']['data'][0]
    
    last_snake = False;

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)
    hc_x_diff = data.get('width')
    hc_y_diff = data.get('height')
    c_tot_diff = hc_x_diff + hc_y_diff
    
    hx = head['x']
    hy = head['y']      #coords of your head and tail
    tx = tail['x']
    ty = tail['y']
    
    ht_x_diff = hx - tx     #differences between you head coords and tail coords
    ht_y_diff = hy - ty
    
    if len(data.get('snakes').get('data')) == 2:        #sets last_snake to the last snake other than you when there are only 2 left
        for rival in [snek for snek in data['snakes']['data'] if snek['id'] != data['you']['id']]:      
            last_snake = rival
    
    #go for food if hunger <61 or it is 1v1 and the rival is longer or has equal length to you
    if data.get('you').get('health') < 61 or (rival and rival['length'] >= data['you']['length']):
        for crumb in data.get('food').get('data'):
            xtemp = hx - crumb.get('x')
            ytemp = hy - crumb.get('y')
            temp_tot = abs(xtemp) + abs(ytemp)      #calculating closest crumb
            if temp_tot <= c_tot_diff:
                hc_x_diff = xtemp
                hc_y_diff = ytemp
                c_tot_diff = temp_tot
        direction = set_direction(hc_x_diff, hc_y_diff, hx, hy, data)   #set direction to closest crumb
    else:
        direction = set_direction(ht_x_diff, ht_y_diff, hx, hy, data)   #otherwise set direction to tail
      
    print direction
    return {
        'move': direction,
        'taunt': 'Kachow'
    }
def set_direction(x_diff, y_diff, hx, hy, data):
    if x_diff > 0 and check_move(hx - 1, hy, data):
            return 'left'
    elif x_diff < 0 and check_move(hx + 1, hy, data):
            return 'right'                                  #goes the direction based on the difference between head coords and destination coords
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
    tail = data['you']['body']['data'][-1]
    tx = tail['x']
    ty = tail['y']
    
    board_width = data.get('width')
    board_height = data.get('height')
    #check if our proposed direction is out of bounds  - this is to avoid walls
    if ourx >= board_width or ourx < 0 or oury >= board_height or oury < 0:
        return 0
    #if ourx == ourbody[1].get('x') and oury ==  ourbody[1].get('y'):
    #    return 0
    
    #check if our proposed direction is where any of our body segments except the tail are
    for seg in data['you']['body']['data'][:-1]:
        if seg['x'] == ourx and seg['y'] == oury:
            return 0
    #for snek in data['snakes']['data']:
        #if abs(snek['body']['data'][0]['x'] - ourx) +  abs(snek['body']['data'][0]['y'] - oury) == 1:
        #    return 0 
        
    #for snek in data.get('snakes').get('data'):
    #    for bod_seg in snek.get('body').get('data'):
    #        if bod_seg.get('x') == ourx and bod_seg.get('y') == oury:
    #            return 0
    
    #checks proposed direction for body segments of any other snake, and if their head can move into our destination
    for s in [snek for snek in data['snakes']['data'] if snek['id'] != data['you']['id']]:
        s_x = s['body']['data'][0].get('x')
        s_y = s['body']['data'][0].get('y')
        #checking if an opponent's head can move into our destination this turn, only if they are longer than us
        if abs((ourx - s_x)) + abs((oury - s_y)) == 1 and s['length'] >= data['you']['length']:  #WTF doesn't this work when == 1?
            return 0
        #checking for opponent snake body segments
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
