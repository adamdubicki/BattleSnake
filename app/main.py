import bottle
import os
from multiprocessing.pool import ThreadPool
from Board import Board
import BoardService as bs
import time
import gc
from BoardE import BoardE

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
	head_url = '%s://%s/static/devito.png' % (
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
	global gameBoard
	gameBoard = BoardE(board_width, board_height)

	head_url = '%s://%s/static/devito.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	return {
		'color': '#F6FAFB',
		'taunt': 'I EAT GARBAGE.',
		'head_url': head_url,
		'name': 'Trash_Snek'
	}


@bottle.post('/move')
def move():
	startTime = time.time()
	data = bottle.request.json

	global gameBoard
	if(gameBoard == None):
		gameBoard = BoardE(data['width'], data['height'])
	else:
		gameBoard.insertData(data)

	# To find snake S1's next moving direction D, the AI follows the steps below:
	goal = bs.pickFood(gameBoard)
	goodPath = True
	pathToGoal = []

	if (goal != None):
		pathToGoal = bs.shortestPath(gameBoard, gameBoard.ourSnakeHead, goal)
	else:
		goodPath = False

	if (len(pathToGoal) > 0):
		virtualSnake = bs.projectSnakeBodyAlongPath(gameBoard, pathToGoal)
		if (bs.isCyclical(gameBoard,virtualSnake)):
			print("Time to find cyclical goal to path", time.time() - startTime)
			move = bs.getDirectionFromMove(gameBoard.ourSnakeHead, pathToGoal[1])
		else:
			print("Path to goal was not safe")
			goodPath = False
	else:
		print("No path to goal")
		goodPath = False

	if (not goodPath):
		pathToTail = bs.longerPath(gameBoard, gameBoard.ourSnakeHead, gameBoard.ourSnakeTail)
		print("Time to find path to tail", time.time() - start)
		if (len(pathToTail) > 0):
			print("Path to tail exists, will stall")
			move = bs.getDirectionFromMove(gameBoard.ourSnakeHead, pathToTail[1])
		else:
			print("No path to tail, need to find most open space")
			move = bs.findMostOpenSpace(gameBoard)
	print("total", time.time() - startTime)

	return {
		'move': move,
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
