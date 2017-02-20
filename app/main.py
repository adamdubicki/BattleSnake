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
	directions = ['up', 'down', 'left', 'right']
	# To find snake S1's next moving direction D, the AI follows the steps below:
	goal = board.pickGoal()
	pathFromHeadToTail = board.aStarSearch(board.ourSnakeHead, board.ourTail)

	#No good goal
	if(board.isTileOutOfBounds(goal)):
		move = board.findStallingMove(pathFromHeadToTail)
	else:
		# 1. Compute the shortestpath P1 from snake S1 's '
		# head to the food. If P1 exists, go to step 2. Otherwise, go to step 4.
		pathToGoal = board.aStarSearch(board.ourSnakeHead, goal)
		if (len(pathToGoal) > 0):

			# 2. Move a virtual snake S2(the same as S1) to eat the food along path P1.
			virtualSnake = board.projectSnakeBodyAlongPath(pathToGoal)

			# 3. Compute the path from S2's head to its tail, if it exists, let D be the direction of P1
			#Otherwise go to step 4
			#board.computePathForVirtualSnake()
			move = board.getDirectionFromMove(pathToGoal[1])
		else:
			move = board.findStallingMove(pathFromHeadToTail)

	return {
		'move': move,
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
