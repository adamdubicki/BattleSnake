import collections
from DirectionEnum import DirectionEnum
from GameBoardEntityEnum import GameBoardEntityEnum
from Tile import Tile

X = 0
Y = 1


class Board():
	# Constructor
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.gameBoard = [[] for width in range(width)]
		for i in range(width + 1):
			for j in range(height):
				self.gameBoard[i].append(GameBoardEntityEnum.Empty)
		self.foods = []
		self.snakeHeads = []
		self.ourSnakeId = []
		self.ourSnakeBody = []
		self.ourSnakeHead = []
		self.ourSnakeTail = []
		self.insertedEntities = []
		self.ourHealth = 0
		self.numFoodEaten = 3
		self.ateFoodThisTurn = False

	# Add data to board from json
	def insertData(self, data):
		oldData = list(self.insertedEntities)
		self.ourSnakeBody = []
		self.ourSnakeHead = []
		self.ourSnakeTail = []
		self.snakeHeads = []
		self.foods = []
		self.insertedEntities = []

		self.ourSnakeId = data['you']

		# Add food
		for food in data['food']:
			self.insertBoardEntity(food, GameBoardEntityEnum.Food)
			self.foods.append(food)
			self.insertedEntities.append(tuple(food))

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
				self.ourHealth = snake['health_points']

		for snake in data['snakes']:
			if snake['id'] != self.ourSnakeId:
				if len(snake['coords']) >= self.ourSnakeLength:
					neighborMoves = self.getValidTileNeighbors(snake['coords'][0])
					for segment in neighborMoves:
						self.insertBoardEntity(segment, GameBoardEntityEnum.Obstacle)
						self.insertedEntities.append(segment)
				self.snakeHeads.append(tuple(snake['coords'][0]))
				for segment in range(0, len(snake['coords'])):
					self.insertBoardEntity(snake['coords'][segment], GameBoardEntityEnum.Obstacle)
					self.insertedEntities.append(tuple(snake['coords'][segment]))

		for segment in self.ourSnakeBody:
			self.insertBoardEntity(segment, GameBoardEntityEnum.Obstacle)
			self.insertedEntities.append(tuple(segment))
		self.insertBoardEntity(self.ourSnakeHead, GameBoardEntityEnum.SnakeHead)
		self.insertBoardEntity(self.ourSnakeTail, GameBoardEntityEnum.SnakeTail)

		for diff in list(set(oldData) - set(self.insertedEntities)):
			self.insertBoardEntity(diff, GameBoardEntityEnum.Empty)

		if(self.ourHealth == 100 and self.getDistanceBetweenSpaces(self.ourSnakeHead,self.ourSnakeTail)==1):
			self.ateFoodThisTurn = True
			self.insertBoardEntity(self.ourSnakeTail, GameBoardEntityEnum.Obstacle)
		else:
			self.ateFoodThisTurn = False

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

	# Get the value at (x,y)
	def getTile(self, tile):
		if (self.isTileOutOfBounds(tile)):
			return None
		return self.gameBoard[tile[X]][tile[Y]]

	# Insert GameBoard entity at tile (x,y)
	def insertBoardEntity(self, tile, entity):
		if (self.isTileOutOfBounds(tile)):
			print("Failed to insert " + str(entity) + " at " + str((tile[X], tile[Y])))
			return False
		else:
			self.gameBoard[tile[X]][tile[Y]] = entity
			return True

	# Given a tile (x,y) return the instance
	def getEntity(self, tile):
		if (self.isTileOutOfBounds(tile)):
			return None
		return self.gameBoard[tile[X]][tile[Y]]

	# Return a list of neighbors which are not obstacles, nor out of bounds
	def getValidTileNeighbors(self, tile):
		inBoundNeighbors = self.getInBoundNeighbors(tile)
		invalidNeighbors = []
		for tile in inBoundNeighbors:
			if (self.getEntity(tile) == GameBoardEntityEnum.Obstacle or self.getEntity(tile) == GameBoardEntityEnum.SnakeHead):
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

	def getDistanceBetweenSpaces(self, tile1, tile2):
		if (tile1[X] == tile2[X] and tile1[Y] == tile2[Y]):
			return 0
		return abs(tile1[X] - tile2[X]) + abs(tile1[Y] - tile2[Y])

	def isTailSafe(self):
		if (self.ateFoodThisTurn and self.getDistanceBetweenSpaces(self.ourSnakeHead,self.ourSnakeTail)==1):
			return False
		else:
			return True

	def toPathString(self, path):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				if ((i, j) in path):
					boardString += "| X |"
				else:
					boardString += "| " + self.gameBoard[i][j] + " |"
			boardString += "\n" + rowDividerString
		return boardString

	# Return the board as a string, for pretty printing
	def toString(self):
		rowDividerString = " --- " * self.width + "\n"
		boardString = rowDividerString
		for j in range(self.height):
			for i in range(self.width):
				boardString += "| " + self.gameBoard[i][j] + " |"
			boardString += "\n" + rowDividerString
		return boardString
