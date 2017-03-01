from DirectionEnum import DirectionEnum
from random import shuffle
import collections
from GameBoardEntityEnum import GameBoardEntityEnum

X = 0
Y = 1


def isArticulationPoint(reachableTiles, tile):
	if ((tile[X] + 1, tile[Y]) not in reachableTiles and (tile[X] - 1, tile[Y]) not in reachableTiles):
		return True
	elif ((tile[X], tile[Y - 1]) not in reachableTiles and (tile[X], tile[Y] + 1) not in reachableTiles):
		return True
	else:
		return False


def getAllReachableTiles(board, start):
	closedList = [board.ourSnakeHead]
	openList = [start]
	while (len(openList) != 0):
		currentTile = openList.pop()
		neighbors = board.getValidTileNeighbors(currentTile)
		for neighbor in neighbors:
			if ((neighbor not in closedList) and (neighbor not in openList)):
				openList.append(neighbor)
		closedList.append(currentTile)
	return closedList


def getDirectionHeuristic(start, reachableTiles, direction):
	directionHeurestic = 0
	articulationPoints = 0
	if (direction == DirectionEnum.Up):
		for tile in reachableTiles:
			if (tile[Y] <= start[Y]):
				directionHeurestic += 1
				if (isArticulationPoint(reachableTiles, tile)):
					articulationPoints += 1
		return directionHeurestic - articulationPoints
	elif (direction == DirectionEnum.Left):
		for tile in reachableTiles:
			if (tile[X] <= start[X]):
				directionHeurestic += 1
				if (isArticulationPoint(reachableTiles, tile)):
					articulationPoints += 1
		return directionHeurestic - articulationPoints
	elif (direction == DirectionEnum.Right):
		for tile in reachableTiles:
			if (tile[X] >= start[X]):
				directionHeurestic += 1
				if (isArticulationPoint(reachableTiles, tile)):
					articulationPoints += 1
		return directionHeurestic - articulationPoints
	else:
		for tile in reachableTiles:
			if (tile[Y] >= start[Y]):
				directionHeurestic += 1
				if (isArticulationPoint(reachableTiles, tile)):
					articulationPoints += 1
		return directionHeurestic - articulationPoints


def findMostOpenSpace(board):
	validMoves = board.getValidTileNeighbors(board.ourSnakeHead)
	shuffle(validMoves)
	if (len(validMoves) == 0):
		return DirectionEnum.Unknown
	mostOpen = [0, DirectionEnum.Unknown, 0]
	for move in validMoves:
		direction = board.getDirectionFromMove(board.ourSnakeHead, move)
		reachableTiles = getAllReachableTiles(board, move)
		directionHeuristic = getDirectionHeuristic(move, reachableTiles, direction)
		if (len(reachableTiles) > mostOpen[0]):
			mostOpen = [len(reachableTiles), direction, directionHeuristic]
		elif (len(reachableTiles) == mostOpen[0]):
			if (directionHeuristic > direction[2]):
				mostOpen = [len(reachableTiles), direction, directionHeuristic]
			else:
				pass
		else:
			pass
		return mostOpen[1]


# -----------------------------------------------------------------------
def pickFood(board):
	goal = (9999, (-1, -1))
	foodDistances = collections.OrderedDict()
	for food in board.foods:
		foodDistances[tuple(food)] = goal
		for snakeHead in board.snakeHeads:
			distance = board.getDistanceBetweenSpaces(food, snakeHead)
			if distance < foodDistances[tuple(food)][0]:
				foodDistances[tuple(food)] = (distance, (snakeHead[X], snakeHead[Y]))
	goalChoice = None
	for food in foodDistances:
		if foodDistances[food][1] == board.ourSnakeHead and foodDistances[food][0] <= goal[0]:
			goalChoice = food
	if (goalChoice != None):
		return goalChoice
	else:
		return goal[1]


# Rebuild the path retracing our steps
def reconstructPath(cameFrom, current):
	totalPath = [current]
	while current in cameFrom.keys():
		current = cameFrom[current]
		totalPath.append(current)
	return list(reversed(totalPath))


# A* Search. Returns the shortest path from S to G, else None
def shortestPath(board, start, goal):
	closedSet = []
	openSet = [start]
	cameFrom = {}

	gScore = [[10000 for x in xrange(board.width)] for y in xrange(board.height)]
	gScore[start[X]][start[Y]] = 0

	fScore = [[10000 for x in xrange(board.width)] for y in xrange(board.height)]
	fScore[start[X]][start[Y]] = board.getDistanceBetweenSpaces(start, goal)

	while (len(openSet) > 0):
		current = min(openSet, key=lambda p: fScore[p[X]][p[Y]])
		if (current == goal):
			return reconstructPath(cameFrom, goal)
		openSet.remove(current)
		closedSet.append(current)
		neighbours = board.getValidTileNeighbors(current)
		for neighbour in neighbours:
			if neighbour in closedSet:
				continue
			tentativeGScore = gScore[current[X]][current[Y]] + board.getDistanceBetweenSpaces(current, neighbour)
			if neighbour not in openSet:
				openSet.append(neighbour)
			elif tentativeGScore >= gScore[neighbour[X]][neighbour[Y]]:
				continue
			cameFrom[neighbour] = current
			gScore[neighbour[X]][neighbour[Y]] = tentativeGScore
			fScore[neighbour[X]][neighbour[Y]] = tentativeGScore + board.getDistanceBetweenSpaces(neighbour, goal)
	return None


# Given two tiles, return the direction 'up', 'down' ...
def getDirectionFromMove(start, move):
	vertical = move[1] - start[1]
	horizontal = move[0] - start[0]
	if vertical == 0:
		if horizontal > 0:
			return DirectionEnum.Right
		else:
			return DirectionEnum.Left
	else:
		if vertical < 0:
			return DirectionEnum.Up
		else:
			return DirectionEnum.Down


# Return the coordinates head to tail of our snake moved along the path
def projectSnakeBodyAlongPath(board, path):
	pathCoords = list(path)
	pathCoords.reverse()

	if (len(path) > len(board.ourSnakeBody)):
		return pathCoords[:len(board.ourSnakeBody)]
	elif (len(board.ourSnakeBody) > len(path)):
		return pathCoords[:-1] + board.ourSnakeBody[:-(len(path) - 1)]
	else:
		return pathCoords


# Determine if a path is cyclical, that is...
# If I move to the goal, will I be trapped?
def isCyclical(board, virtualSnake):
	originalSnake = board.ourSnakeBody
	originalHead = board.ourSnakeHead
	originalTail = board.ourSnakeTail

	for snake in originalSnake:
		board.insertBoardEntity(snake, GameBoardEntityEnum.Empty)
	for projection in virtualSnake:
		board.insertBoardEntity(projection, GameBoardEntityEnum.Obstacle)

	board.insertBoardEntity(virtualSnake[-1], GameBoardEntityEnum.SnakeTail)
	board.insertBoardEntity(virtualSnake[0], GameBoardEntityEnum.SnakeHead)
	cycle = shortestPath(board, virtualSnake[0], virtualSnake[-1])

	for projection in virtualSnake:
		board.insertBoardEntity(projection, GameBoardEntityEnum.Empty)
	for snake in originalSnake:
		board.insertBoardEntity(snake, GameBoardEntityEnum.Obstacle)

	board.insertBoardEntity(originalHead, GameBoardEntityEnum.SnakeHead)
	board.insertBoardEntity(originalTail, GameBoardEntityEnum.SnakeTail)
	board.insertBoardEntity(virtualSnake[0], GameBoardEntityEnum.Food)
	if (len(cycle) > 0):
		return True
	else:
		return False


# Extend the path, if the extension is valid
def extendPath(currentTile, nextTile, visited, newPath, index):
	visited.append(currentTile)
	visited.append(nextTile)
	if (currentTile not in newPath and nextTile not in newPath):
		newPath.insert(index + 1, currentTile)
		newPath.insert(index + 2, nextTile)


def isExtensionValid(board, currentTile, nextTile, visited):
	if (board.isTileOutOfBounds(currentTile) or board.isTileOutOfBounds(nextTile)):
		return False
	elif (board.getTile(currentTile) == GameBoardEntityEnum.Obstacle):
		return False
	elif (board.getTile(nextTile) == GameBoardEntityEnum.Obstacle):
		return False
	elif (currentTile in visited and nextTile in visited):
		return False
	else:
		return True


# Heuristic longer path
def longerPath(board, start, goal):
	basePath = shortestPath(board, start, goal)
	pathFinished = False
	visited = list(basePath)

	if (basePath != None):

		if (len(basePath) > 10):
			basePath = basePath[:10]

		while (not pathFinished and len(basePath) < 20):
			changesMade = False

			for i in range(len(basePath) - 1):
				currentTile = basePath[i]
				nextTile = basePath[i + 1]
				direction = getDirectionFromMove(currentTile, nextTile)

				if (direction == DirectionEnum.Left or direction == DirectionEnum.Right):
					currentUp = (currentTile[X], currentTile[Y] - 1)
					nextUp = (nextTile[X], nextTile[Y] - 1)
					if (isExtensionValid(board, currentUp, nextUp, visited)):
						extendPath(currentUp, nextUp, visited, basePath, i)
						changesMade = True
					else:
						currentDown = (currentTile[X], currentTile[Y] + 1)
						nextDown = (nextTile[X], nextTile[Y] + 1)
						if (isExtensionValid(board, currentDown, nextDown, visited)):
							extendPath(currentDown, nextDown, visited, basePath, i)
							changesMade = True
				else:
					currentLeft = (currentTile[X] - 1, currentTile[Y])
					nextLeft = (nextTile[X] - 1, nextTile[Y])
					if (isExtensionValid(board, currentLeft, nextLeft, visited)):
						extendPath(currentLeft, nextLeft, visited, basePath, i)
						changesMade = True
					else:
						currentRight = (currentTile[X], currentTile[Y] + 1)
						nextRight = (nextTile[X], nextTile[Y] + 1)
						if (isExtensionValid(board, currentRight, nextRight, visited)):
							extendPath(currentRight, nextRight, visited, basePath, i)
							changesMade = True
			if (not changesMade):
				pathFinished = True
		return basePath
	else:
		return None

	return basePath
