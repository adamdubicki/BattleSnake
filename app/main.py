import bottle
import os
from multiprocessing.pool import ThreadPool
from Board import Board
import time


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
	start = time.time()

	data = bottle.request.json
	board = Board(data['width'], data['height'], data)
	directions = ['up', 'down', 'left', 'right']
	# To find snake S1's next moving direction D, the AI follows the steps below:

	goal = board.pickGoal()
	pool = ThreadPool(processes=2)
	pathToGoal = pool.apply_async(board.aStarSearch, (board.ourSnakeHead, goal))
	pathToTail = pool.apply_async(board.longerPath, (board.ourSnakeHead, board.ourSnakeTail))
	pathToGoal = pathToGoal.get()

	# 1. Compute the shortest path P1 from our snakes's head to the goal.
	# If path to the goal exists, go to step 2, Otherwise, go to step 4.
	goodPath = True
	if (len(pathToGoal) > 0):
		# 2. Move a virtual snake to eat the food along path P1.
		virtualSnake = board.projectSnakeBodyAlongPath(pathToGoal)

		# We need the async call to end,
		# the virtual snake modifies board data
		pathToTail.wait()

		# 3. Compute the longest path P2 from virtual snakes's head to its tail.
		# If P2 exists, let D be the first direction in path P1. Otherwise, go to step 4
		if (board.isCyclical(virtualSnake)):
			move = board.getDirectionFromMove(pathToGoal[1], board.ourSnakeHead)
		else:
			goodPath = False
	else:
		goodPath = False

	if (not goodPath):
		# 4. Compute the longest path P3 from snake S1 's head to its tail. If P3 exists,
		# let D be the first direction in path P3. Otherwise, go to step 5.
		pathToTail = pathToTail.get()
		if (len(pathToTail) > 0):
			move = board.getDirectionFromMove(board.ourSnakeHead, pathToTail[1])
		else:
			# THIS IS WHERE WE NEED TO WORRY
			pass

	# print(board.toString())
	print(time.time() - start)
	return {
		'move': move,
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
