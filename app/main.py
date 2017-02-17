import bottle
import os
import random
from Board import Board
from GameBoardEntityEnum import GameBoardEntityEnum


@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	return {
		'color': '#00ff00',
		'head': head_url
	}


@bottle.post('/start')
def start():
	data = bottle.request.json
	game_id = data['game_id']
	board_width = data['width']
	board_height = data['height']

	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	# TODO: Do things with data

	return {
		'color': '#00FF00',
		'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
		'head_url': head_url,
		'name': 'battlesnake-python'
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	board = Board(data['width'], data['height'], data)
	goal = board.pickGoal()
	if(board.isTileOutOfBounds(goal)):
		move = "DO SOMETHING FOR NO GOOD GOAL"
	else:
		path = board.aStarSearch(board.ourSnakeHead, goal)
		if path != len(path) > 0:
			print("Found Path to goal:" + str(path))
			move = board.getDirectionFromMove(path[1])
			print("Moving "+move)
		else:
			move = "DO SOMETHING FOR NO PATH"

	directions = ['up', 'down', 'left', 'right']

	return {
		'move': move,
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
