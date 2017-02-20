import collections

from GameBoardEntityEnum import GameBoardEntityEnum
from Tile import Tile

X = 0
Y = 1


class Board():
	def __init__(self, width, height, data):
		self.width = width
		self.height = height
		self.gameBoard = [[] for width in range(width)]
		for i in range(width + 1):
			for j in range(height):
				self.gameBoard[i].append(Tile(i, j, GameBoardEntityEnum.Empty))
		self.foods = []
		self.snakeHeads = []
		self.ourSnakeId = data['you']
		self.ourSnakeBody = []
		self.ourSnakeHead = []

		# Add food
		for food in data['food']:
			self.insertBoardEntity(food, GameBoardEntityEnum.Food)
			self.foods.append(food)

		# Process Our Snake
		for snake in data['snakes']:
			if snake['id'] == self.ourSnakeId:
				self.ourSnakeLength = len(snake['coords'])
				self.ourSnakeHead = tuple((snake['coords'][0]))
				self.snakeHeads.append(self.ourSnakeHead)
				self.ourTail = tuple((snake['coords'][-1]))
				self.ourSnakeBody.append(self.ourSnakeHead)
				self.insertBoardEntity(self.ourSnakeHead, GameBoardEntityEnum.SnakeHead)
				for segment in range(1, len(snake['coords'])-1):
					self.ourSnakeBody.append(tuple(snake['coords'][segment]))
					self.insertBoardEntity(snake['coords'][segment], GameBoardEntityEnum.Obstacle)
				self.ourSnakeBody.append(tuple(self.ourTail))
				self.insertBoardEntity(self.ourTail, GameBoardEntityEnum.SnakeTail)

		# Process Opponents snake
		for snake in data['snakes']:
			if snake['id'] != self.ourSnakeId:
				if len(snake['coords']) >= self.ourSnakeLength:
					neighborMoves = self.getValidTileNeighbors(snake['coords'][0])
					for segment in neighborMoves:
						self.insertBoardEntity(segment, GameBoardEntityEnum.Obstacle)
				self.snakeHeads.append(tuple(snake['coords'][0]))
				for segment in range(0, len(snake['coords'])):
					self.insertBoardEntity(snake['coords'][segment], GameBoardEntityEnum.Obstacle)

	def pickGoal(self):
		goal = (9999, (-1, -1))
		foodDistances = collections.OrderedDict()
		for food in self.foods:
			foodDistances[tuple(food)] = goal
			for snakeHead in self.snakeHeads:
				distance = self.getDistanceBetweenSpaces(food, snakeHead)
				if distance < foodDistances[tuple(food)][0]:
					foodDistances[tuple(food)] = (distance, (snakeHead[X], snakeHead[Y]))
		goalChoice = None
		for food in foodDistances:
			if foodDistances[food][1] == self.ourSnakeHead and foodDistances[food][0] <= goal[0]:
				goalChoice = food
		if(goalChoice!=None):
			return goalChoice
		else:
			return goal[1]

	def getDirectionFromMove(self, move):
		vertical = move[1] - self.ourSnakeHead[1]
		horizontal = move[0] - self.ourSnakeHead[0]
		print(horizontal)
		if vertical == 0:
			if horizontal > 0:
				return 'right'
			else:
				return 'left'
		else:
			if vertical < 0:
				return 'up'
			else:
				return 'down'

	# Helper method
	def isXOutOfBounds(self, xPosition):
		if (xPosition < 0 or xPosition > self.width - 1):
			return True
		else:
			return False

	# Helper method
	def isYOutOfBounds(self, yPosition):
		if (yPosition < 0 or yPosition > self.height - 1):
			return True
		else:
			return False

	# Helper method
	def isTileOutOfBounds(self, tile):
		if (self.isXOutOfBounds(tile[X]) or self.isYOutOfBounds(tile[Y])):
			return True
		return False

	# Insert a board entity into a tile (x,y)
	def insertBoardEntity(self, tile, entity):
		if (self.isTileOutOfBounds(tile)):
			print("Failed to insert " + str(entity) + " at " + str((tile[X], tile[Y])))
			return False
		else:
			self.gameBoard[tile[X]][tile[Y]].entity = entity
			return True

	# Get Manhatten distance between two tiles
	def getDistanceBetweenSpaces(self, tile1, tile2):
		if (tile1[X] == tile2[X] and tile1[Y] == tile2[Y]):
			return 0
		return abs(tile1[X] - tile2[X]) + abs(tile1[Y] - tile2[Y])

	def aStarSearch(self, start, goal):
		if (self.isTileOutOfBounds(start) or self.isTileOutOfBounds(goal)):
			print("Failed to search because start or goal was out of bounds")
			return None
		if (start == goal):
			print("Failed to search because the snake is already at the goal")
			return None
		# Initialize the heurestic values + distance values of the tiles
		normalizedDistanceValue = self.width * self.height
		# Tiles we need to vist
		openList = collections.OrderedDict()

		# A list of tiles updated with the most current path
		closedList = []

		startingTile = self.getTile(start)
		startingTile.fCost = 0
		startingTile.parent = startingTile

		# At initialization add the starting location to the open list and empty the closed list
		openList[startingTile.getPositionTuple()] = startingTile
		foundGoal = self.exploreTilesForShortestPath(openList, closedList, goal)
		if(foundGoal):
			path = self.reconstructPath(start, goal, closedList)
			return path
		else:
			return []

	def findStallingMove(self,pathFromHeadToTail):
		if (len(pathFromHeadToTail) > 0):
			return self.getDirectionFromMove(pathFromHeadToTail[1])
		else:
			# FOCUS HERE, NEED SOMETHING REALLY GOOD HERE
			pass

	def exploreTilesForShortestPath(self, openList, closedList, goal):
		foundGoal = False
		while (bool(openList) and not foundGoal):
			openList = self.sortTiles(openList)
			currentTile = openList.popitem(last=False)[1]
			neighbors = self.getValidTileNeighbors(currentTile.getPositionTuple())
			for neighbor in neighbors:
				neighborTile = self.getTile(neighbor)
				if ((neighborTile.getPositionTuple()) == (self.getTile(goal).getPositionTuple())):
					foundGoal = True
					self.getTile(goal).parent = currentTile
					closedList.append(self.getTile(goal))
					break
				newCost = currentTile.fCost + self.getDistanceBetweenSpaces(neighborTile.getPositionTuple(), self.getTile(goal).getPositionTuple()) + self.getDangerHeurestic(neighborTile.getPositionTuple())
				if (not (neighborTile in closedList) and newCost <= neighborTile.fCost):
					neighborTile.fCost = newCost
					openList[neighborTile.getPositionTuple()] = neighborTile
					neighborTile.parent = currentTile
			closedList.append(currentTile)
		if (not foundGoal):
			print("Goal was not reachable.")
			return False
		else:
			return True

	#Return the coordinates head to tail of our snake moved along the path
	def projectSnakeBodyAlongPath(self, path):
		pathCoords = list(path)
		pathCoords.reverse()
		if(len(path) > len(self.ourSnakeBody)):
			return pathCoords[:len(self.ourSnakeBody)]
		elif(len(self.ourSnakeBody) > len(path)):
			return pathCoords[:-1] + self.ourSnakeBody[:-(len(path)-1)]
		else:
			return pathCoords


	def reconstructPath(self, start, goal, closedList):
		pathFinished = False
		currentTile = 0
		for tile in closedList:
			if (tile.getPositionTuple() == goal):
				currentTile = tile
		path = [currentTile.getPositionTuple()]
		while (not pathFinished):
			if (currentTile.getPositionTuple() == start):
				pathFinished = True
			else:
				parentTile = currentTile.parent
				path.append(parentTile.getPositionTuple())
				currentTile = parentTile
		path.reverse()
		return path

	def sortTiles(self, openList):
		orderedList = collections.OrderedDict(sorted(openList.items(), key=lambda tile: tile[1].fCost))
		return orderedList

	def getValidTileNeighbors(self, tile):
		inBoundNeighbors = self.getInBoundNeighbors(tile)
		invalidNeighbors = []
		for tile in inBoundNeighbors:
			if (self.getTile(tile).entity == GameBoardEntityEnum.Obstacle):
				invalidNeighbors.append(tile)
		for invalidNeighbor in invalidNeighbors:
			inBoundNeighbors.remove(invalidNeighbor)
		return inBoundNeighbors

	# Return a list of tile neightbors which are not out of bounds
	def getInBoundNeighbors(self, tile):
		neighbors = [(tile[X] - 1, tile[Y]), (tile[X] + 1, tile[Y]), (tile[X], tile[Y] - 1), (tile[X], tile[Y] + 1)]
		invalidNeighbors = []
		for neighbor in neighbors:
			invalidTile = False
			if (self.isTileOutOfBounds(neighbor)):
				invalidTile = True
			if (invalidTile):
				invalidNeighbors.append(neighbor)
		for invalidNeighbor in invalidNeighbors:
			neighbors.remove(invalidNeighbor)
		return neighbors

	def getDangerHeurestic(self, tile):
		validNeighbors = self.getValidTileNeighbors(tile)
		return (4 - len(validNeighbors))

	# Given a tile (x,y) return the instance
	def getTile(self, tile):
		if (self.isTileOutOfBounds(tile)):
			return None
		return self.gameBoard[tile[X]][tile[Y]]

	def toString(self):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				tile = self.gameBoard[i][j]
				boardString += "| " + self.gameBoard[i][j].entity + " |"
			boardString += "\n" + rowDividerString
		return boardString

	def showPathString(self, path):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				tile = self.gameBoard[i][j]
				if ((i, j) in path):
					boardString += "| X |"
				else:
					boardString += "| " + self.gameBoard[i][j].entity + " |"
			boardString += "\n" + rowDividerString
		return boardString

	def toCostString(self):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				tile = self.gameBoard[i][j]
				if (tile.entity == GameBoardEntityEnum.Obstacle):
					boardString += "| ooo |"
				else:
					boardString += "| " + str(self.gameBoard[i][j].fCost) + " |"
			boardString += "\n" + rowDividerString
		return boardString
