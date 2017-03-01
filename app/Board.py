import collections
from DirectionEnum import DirectionEnum
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

		# Get our snake data, is used for ptrocessing of opponents snakes
		for snake in data['snakes']:
			if snake['id'] == self.ourSnakeId:
				self.ourSnakeLength = len(snake['coords'])
				self.ourSnakeHead = tuple((snake['coords'][0]))
				self.snakeHeads.append(self.ourSnakeHead)
				self.ourSnakeTail = tuple((snake['coords'][-1]))
				self.ourSnakeBody.append(self.ourSnakeHead)
				self.insertBoardEntity(self.ourSnakeHead, GameBoardEntityEnum.SnakeHead)
				for segment in range(1, len(snake['coords']) - 1):
					self.ourSnakeBody.append(tuple(snake['coords'][segment]))
				self.ourSnakeBody.append(tuple(self.ourSnakeTail))

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

		# Add our snake body
		for segment in self.ourSnakeBody:
			self.insertBoardEntity(segment, GameBoardEntityEnum.Obstacle)
		self.insertBoardEntity(self.ourSnakeHead, GameBoardEntityEnum.SnakeHead)
		self.insertBoardEntity(self.ourSnakeTail, GameBoardEntityEnum.SnakeTail)

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
		if (goalChoice != None):
			return None
		else:
			return goal[1]

	def getDirectionFromMove(self, start, move):
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
			self.gameBoard[tile[X]][tile[Y]].fCost = 9999999
			return True

	# Get Manhatten distance between two tiles
	def getDistanceBetweenSpaces(self, tile1, tile2):
		if (tile1[X] == tile2[X] and tile1[Y] == tile2[Y]):
			return 0
		return abs(tile1[X] - tile2[X]) + abs(tile1[Y] - tile2[Y])

	def extendPath(self, currentTile, nextTile, visited, newPath, index):
		visited.append(currentTile)
		visited.append(nextTile)
		if (currentTile not in newPath and nextTile not in newPath):
			newPath.insert(index + 1, currentTile)
			newPath.insert(index + 2, nextTile)

	def isExtensionValid(self, currentTile, nextTile, visited):
		if (self.isTileOutOfBounds(currentTile) or self.isTileOutOfBounds(nextTile)):
			return False
		elif (self.getTile(currentTile).entity == GameBoardEntityEnum.Obstacle):
			return False
		elif (self.getTile(nextTile).entity == GameBoardEntityEnum.Obstacle):
			return False
		elif (currentTile in visited and nextTile in visited):
			return False
		else:
			return True

	# Longest path is NP Complete, this is a rough estimate
	def longerPath(self, start, goal):
		basePath = self.aStarSearch(start, goal)
		pathFinished = False
		visited = list(basePath)
		if (len(basePath) > 0):

			if(len(basePath)>30):
				basePath = basePath[:30]

			while (not pathFinished and len(basePath)<50):
				changesMade = False
				for i in range(len(basePath) - 1):
					currentTile = basePath[i]
					nextTile = basePath[i + 1]
					direction = self.getDirectionFromMove(currentTile, nextTile)
					if (direction == DirectionEnum.Left or direction == DirectionEnum.Right):
						currentUp = (currentTile[X], currentTile[Y] - 1)
						nextUp = (nextTile[X], nextTile[Y] - 1)
						if (self.isExtensionValid(currentUp, nextUp, visited)):
							# print("Extending down: " + str(currentUp) + " " + str(nextUp))
							self.extendPath(currentUp, nextUp, visited, basePath, i)
							changesMade = True
						else:
							currentDown = (currentTile[X], currentTile[Y] + 1)
							nextDown = (nextTile[X], nextTile[Y] + 1)
							if (self.isExtensionValid(currentDown, nextDown, visited)):
								# print("Extending down: " + str(currentDown) + " " + str(nextDown))
								self.extendPath(currentDown, nextDown, visited, basePath, i)
								changesMade = True
					else:
						currentLeft = (currentTile[X] - 1, currentTile[Y])
						nextLeft = (nextTile[X] - 1, nextTile[Y])
						if (self.isExtensionValid(currentLeft, nextLeft, visited)):
							# print("Extending Left: " + str(currentLeft) + " " + str(nextLeft))
							self.extendPath(currentLeft, nextLeft, visited, basePath, i)
							changesMade = True
						else:
							currentRight = (currentTile[X], currentTile[Y] + 1)
							nextRight = (nextTile[X], nextTile[Y] + 1)
							if (self.isExtensionValid(currentRight, nextRight, visited)):
								# print("Extending right: " + str(currentRight) + " " + str(nextRight))
								self.extendPath(currentRight, nextRight, visited, basePath, i)
								changesMade = True
				if (not changesMade):
					pathFinished = True
			return basePath
		else:
			return []

	# Path finding algorithm
	def aStarSearch(self, start, goal):
		# startTime = time.time()
		if (self.isTileOutOfBounds(start) or self.isTileOutOfBounds(goal)):
			print("Failed to search because start or goal was out of bounds")
			return []
		if (start == goal):
			print("Failed to search because the snake is already at the goal")
			return []
		# Initialize the heurestic values + distance values of the tiles
		normalizedDistanceValue = self.width * self.height
		# Tiles we need to vist
		openList = collections.OrderedDict()

		# A list of tiles updated with the most current path
		closedList = []
		fCost = {}

		startingTile = self.getTile(start)
		startingTile.fCost = 0
		for i in range(self.width):
			for j in range(self.height):
				fCost[(i, j)] = 9999999
		fCost[startingTile.getPositionTuple()] = 0
		startingTile.parent = startingTile

		# At initialization add the starting location to the open list and empty the closed list
		openList[startingTile.getPositionTuple()] = startingTile
		foundGoal = self.exploreTilesForShortestPath(openList, closedList, goal, fCost)
		if (foundGoal):
			path = self.reconstructPath(start, goal, closedList)
			# print("Time to find goal", time.time() - startTime)
			return path
		else:
			return []

	# Try and find the goal
	def exploreTilesForShortestPath(self, openList, closedList, goal, fCost):
		foundGoal = False
		while (bool(openList) and not foundGoal):
			openList = self.sortTiles(openList, fCost)
			currentTile = openList.popitem(last=False)[1]
			neighbors = self.getValidTileNeighbors(currentTile.getPositionTuple())
			# print(str(currentTile.getPositionTuple()) + " neighbors " + str(neighbors))
			for neighbor in neighbors:
				neighborTile = self.getTile(neighbor)
				if ((neighborTile.getPositionTuple()) == (self.getTile(goal).getPositionTuple())):
					foundGoal = True
					self.getTile(goal).parent = currentTile
					closedList.append(self.getTile(goal))
					break
				newCost = fCost[currentTile.getPositionTuple()] + self.gCost(neighborTile, goal)
				if (not (neighborTile in closedList) and newCost <= fCost[neighborTile.getPositionTuple()]):
					fCost[neighborTile.getPositionTuple()] = newCost
					openList[neighborTile.getPositionTuple()] = neighborTile
					neighborTile.parent = currentTile
			closedList.append(currentTile)
		if (not foundGoal):
			print("Goal was not reachable.")
			return False
		else:
			return True

	# The heuristic cost of moving to a tile
	def gCost(self, neighborTile, goal):
		return self.getDistanceBetweenSpaces(neighborTile.getPositionTuple(), self.getTile(goal).getPositionTuple()) + \
			   self.getDangerHeurestic(neighborTile.getPositionTuple())

	# Return the coordinates head to tail of our snake moved along the path
	def projectSnakeBodyAlongPath(self, path):
		pathCoords = list(path)
		pathCoords.reverse()
		if (len(path) > len(self.ourSnakeBody)):
			return pathCoords[:len(self.ourSnakeBody)]
		elif (len(self.ourSnakeBody) > len(path)):
			return pathCoords[:-1] + self.ourSnakeBody[:-(len(path) - 1)]
		else:
			return pathCoords

	# Check to see if a path is cyclical
	def isCyclical(self, virtualSnake):
		originalSnake = self.ourSnakeBody
		originalHead = self.ourSnakeHead
		originalTail = self.ourSnakeTail
		for snake in originalSnake:
			self.insertBoardEntity(snake, GameBoardEntityEnum.Empty)
		for projection in virtualSnake:
			self.insertBoardEntity(projection, GameBoardEntityEnum.Obstacle)
		self.insertBoardEntity(virtualSnake[-1], GameBoardEntityEnum.SnakeTail)
		self.insertBoardEntity(virtualSnake[0], GameBoardEntityEnum.SnakeHead)
		cycle = self.aStarSearch(virtualSnake[0], virtualSnake[-1])
		for projection in virtualSnake:
			self.insertBoardEntity(projection, GameBoardEntityEnum.Empty)
		for snake in originalSnake:
			self.insertBoardEntity(snake, GameBoardEntityEnum.Obstacle)
		self.insertBoardEntity(originalHead, GameBoardEntityEnum.SnakeHead)
		self.insertBoardEntity(originalTail, GameBoardEntityEnum.SnakeTail)
		self.insertBoardEntity(virtualSnake[0], GameBoardEntityEnum.Food)
		if (len(cycle) > 0):
			return True
		else:
			return False

	# Given the list of what was visited, create list [h,p1,..,pn,g]
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

	# Sort the tiles by current shortest path for a*
	def sortTiles(self, openList, fCost):
		orderedList = collections.OrderedDict(
			sorted(openList.items(), key=lambda tile: fCost[tile[1].getPositionTuple()]))
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

	# Get a heuristic on how dangerous a tile is
	# Dangerous tiles are close to walls
	def getDangerHeurestic(self, tile):
		validNeighbors = self.getValidTileNeighbors(tile)
		return (4 - len(validNeighbors))

	# Given a tile (x,y) return the instance
	def getTile(self, tile):
		if (self.isTileOutOfBounds(tile)):
			return None
		return self.gameBoard[tile[X]][tile[Y]]

	# To string, pretty print
	def toString(self):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				tile = self.gameBoard[i][j]
				boardString += "| " + self.gameBoard[i][j].entity + " |"
			boardString += "\n" + rowDividerString
		return boardString

	# Print the board, with the path injected
	def toPathString(self, path):
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
