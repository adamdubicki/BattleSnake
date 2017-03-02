import bottle
import os
from BoardDepreacted import Board
import BoardService as bs
from Board import Board
import time
from GameBoardEntityEnum import GameBoardEntityEnum

gameBoard = None


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
	gameBoard = Board(board_width, board_height)

	head_url = '%s://%s/static/devito.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	return {
		'color': '#660000',
		'taunt': 'I EAT GARBAGE.',
		'head_url': head_url,
		'name': 'Trash_Snek'
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	startTime = time.time()
	global gameBoard
	if (gameBoard == None):
		gameBoard = Board(data['width'], data['height'])
		print("Made new board")
	else:
		gameBoard.insertData(data)

	# To find snake S1's next moving direction D, the AI follows the steps below:
	goal = bs.pickFood(gameBoard)
	goodPath = True
	pathToGoal = None

	# If we eat food, then our tail is not safe for adjacent moves
	if(not gameBoard.isTailSafe()):
		gameBoard.insertBoardEntity(gameBoard.ourSnakeTail, GameBoardEntityEnum.Obstacle)

	if (goal != None):
		pathToGoal = bs.shortestPath(gameBoard, gameBoard.ourSnakeHead, goal)
	else:
		goodPath = False

	if (pathToGoal != None):
		print("Found path to goal")
		virtualSnake = bs.projectSnakeBodyAlongPath(gameBoard, pathToGoal)
		if (bs.isCyclical(gameBoard, virtualSnake)):
			move = bs.getDirectionFromMove(gameBoard.ourSnakeHead, pathToGoal[1])
			gameBoard.ateFoodThisTurn = True
		else:
			print("path was not safe")
			goodPath = False
	else:
		goodPath = False

	if (not goodPath):
		pathToTail = bs.longerPath(gameBoard, gameBoard.ourSnakeHead, gameBoard.ourSnakeTail)
		if (pathToTail != None and len(pathToTail)>1):
			move = bs.getDirectionFromMove(gameBoard.ourSnakeHead, pathToTail[1])
			gameBoard.ateFoodThisTurn = False
		else:
			print("Searching for most open space")
			move = bs.findMostOpenSpace(gameBoard)
			gameBoard.ateFoodThisTurn = False
	print("Endtime",startTime - time.time())
	return {
		'move': move,
		'taunt': 'battlesnake-python!'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
