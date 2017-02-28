from DirectionEnum import DirectionEnum
from random import shuffle

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
	if(len(validMoves) == 0):
		return DirectionEnum.Unknown
	mostOpen = [0, DirectionEnum.Unknown, 0]
	for move in validMoves:
		direction = board.getDirectionFromMove(board.ourSnakeHead, move)
		reachableTiles = getAllReachableTiles(board, move)
		directionHeuristic = getDirectionHeuristic(move, reachableTiles, direction)
		if(len(reachableTiles) > mostOpen[0]):
			mostOpen = [len(reachableTiles), direction, directionHeuristic]
		elif(len(reachableTiles) == mostOpen[0]):
			if(directionHeuristic > direction[2]):
				mostOpen = [len(reachableTiles), direction, directionHeuristic]
			else:
				pass
		else:
			pass

		return mostOpen[1]
