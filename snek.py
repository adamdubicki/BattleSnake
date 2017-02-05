from GameBoardEntityEnum import GameBoardEntityEnum
from Board import Board
from Tile import Tile

def main():

	#TEST 1
	board = Board(6,3)
	board.insertBoardEntity((2,0), GameBoardEntityEnum.SnakeHead)
	board.insertBoardEntity((1,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((3,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,2), GameBoardEntityEnum.Food)
	path = board.aStarSearch((2,0),(2,2), True)
	print(board.toString())
	print(board.toCostString())
	print(board.showPathString(path))

	# #TEST 2
	board = Board(20,20)
	board.insertBoardEntity((0,0), GameBoardEntityEnum.SnakeHead)
	board.insertBoardEntity((1,0), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((1,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((1,2), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((0,10), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((1,10), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,10), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((3,10), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((4,9), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((6,9), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((6,10), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((6,11), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((5,11), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((7,11), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,11),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,10),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,9),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,8),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,7),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,6),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,5),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((8,4),GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((19,19), GameBoardEntityEnum.Food)
	path = board.aStarSearch((0,0),(19,19), True)
	print(board.toString())
	print(board.toCostString())
	print(board.showPathString(path))

	#Test 3
	board = Board(3,3)
	board.insertBoardEntity((2,0), GameBoardEntityEnum.SnakeHead)
	board.insertBoardEntity((1,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,2), GameBoardEntityEnum.Food)
	path = board.aStarSearch((2,0),(2,2), True)
	print(board.toString())
	# print(board.toCostString())
	print(board.showPathString(path))

	board = Board(5,5)
	board.insertBoardEntity((0,0), GameBoardEntityEnum.SnakeHead)
	board.insertBoardEntity((1,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((2,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((3,1), GameBoardEntityEnum.Obstacle)
	board.insertBoardEntity((4,4), GameBoardEntityEnum.Food)
	path = board.aStarSearch((0,0),(4,4), True)
	print(board.toString())
	# print(board.toCostString())
	print(board.showPathString(path))

	return 1

main()
