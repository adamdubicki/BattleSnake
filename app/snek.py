from GameBoardEntityEnum import GameBoardEntityEnum
from BoardDepreacted import Board
from Tile import Tile
import numpy as np
from Board import BoardE
import time
import BoardService as bs


def main():
	start = time.time()
	board = BoardE(20, 20)
	# for i in range(1000):
	# board.insertData({
	# 	"you": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
	# 	"width": 20,
	# 	"turn": 0,
	# 	"snakes": [
	# 		{
	# 			"taunt": "git gud",
	# 			"name": "my-snake",
	# 			"id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
	# 			"health_points": 93,
	# 			"coords": [
	# 				[
	# 					1,
	# 					0
	# 				],
	# 				[
	# 					1,
	# 					1
	# 				],
	# 				[
	# 					1,
	# 					2
	# 				]
	# 			]
	# 		}
	# 	],
	# 	"height": 20,
	# 	"game_id": "870d6d79-93bf-4941-8d9e-944bee131167",
	# 	"food": [
	# 		[
	# 			19,
	# 			19
	# 		]
	#
	# 	],
	# 	"dead_snakes": [
	# 		{
	# 			"taunt": "gotta go fast",
	# 			"name": "other-snake",
	# 			"id": "c4e48602-197e-40b2-80af-8f89ba005ee9",
	# 			"health_points": 50,
	# 			"coords": [
	# 				[
	# 					5,
	# 					0
	# 				],
	# 				[
	# 					5,
	# 					0
	# 				],
	# 				[
	# 					5,
	# 					0
	# 				]
	# 			]
	# 		}
	# 	]
	# })
	board.insertData({
		"you": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
		"width": 20,
		"turn": 0,
		"snakes": [
			{
				"taunt": "git gud",
				"name": "my-snake",
				"id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
				"health_points": 93,
				"coords": [
					[
						1,
						0
					],
					[
						1,
						1
					]
				]
			}
		],
		"height": 20,
		"game_id": "870d6d79-93bf-4941-8d9e-944bee131167",
		"food": [
			[
				19,
				19
			]

		],
		"dead_snakes": [
			{
				"taunt": "gotta go fast",
				"name": "other-snake",
				"id": "c4e48602-197e-40b2-80af-8f89ba005ee9",
				"health_points": 50,
				"coords": [
					[
						5,
						0
					],
					[
						5,
						0
					],
					[
						5,
						0
					]
				]
			}
		]
	})
	print("Time to create board", float((time.time() - start)))
	bs.shortestPath(board, board.ourSnakeHead, (19, 19))
	print("Time to create board", float((time.time() - start)))
	bs.longerPath(board, board.ourSnakeHead, (19, 19))
	# print (board.toString())
	print("Time to create board", float((time.time() - start)))

	# da = np.genfromtxt('README.md', delimiter = ',')

	# TEST 1
	# board = Board(20, 20, {
	# 	"you": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
	# 	"width": 20,
	# 	"turn": 0,
	# 	"snakes": [
	# 		{
	# 			"taunt": "git gud",
	# 			"name": "my-snake",
	# 			"id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
	# 			"health_points": 93,
	# 			"coords": [
	# 				[
	# 					1,
	# 					0
	# 				],
	# 				[
	# 					1,
	# 					1
	# 				],
	# 				[
	# 					1,
	# 					2
	# 				]
	# 			]
	# 		}
	# 	],
	# 	"height": 20,
	# 	"game_id": "870d6d79-93bf-4941-8d9e-944bee131167",
	# 	"food": [
	# 		[
	# 			19,
	# 			19
	# 		]
	#
	# 	],
	# 	"dead_snakes": [
	# 		{
	# 			"taunt": "gotta go fast",
	# 			"name": "other-snake",
	# 			"id": "c4e48602-197e-40b2-80af-8f89ba005ee9",
	# 			"health_points": 50,
	# 			"coords": [
	# 				[
	# 					5,
	# 					0
	# 				],
	# 				[
	# 					5,
	# 					0
	# 				],
	# 				[
	# 					5,
	# 					0
	# 				]
	# 			]
	# 		}
	# 	]
	# })
	# print("-asdasd")
	# path = board.aStarSearch((1, 0), (2, 2))
	# print(board.toString())
	# # path = [(8, 0), (9, 0), (9, 1), (9, 2)]
	# print(path)
	# virtualSnake = board.projectSnakeBodyAlongPath(path)
	# print(virtualSnake)
	# board.isCyclical(virtualSnake)
	# print(board.toCostString())
	# print(board.showPathString(path))

	# # #TEST 2
	# board = Board(20, 20)
	# board.insertBoardEntity((0, 0), GameBoardEntityEnum.SnakeHead)
	# board.insertBoardEntity((1, 0), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((1, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((1, 2), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((0, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((1, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((2, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((3, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((4, 9), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((6, 9), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((6, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((6, 11), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((5, 11), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((7, 11), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 11), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 10), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 9), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 8), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 7), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 6), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 5), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((8, 4), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((19, 19), GameBoardEntityEnum.Food)
	# path = board.aStarSearch((0, 0), (19, 19))
	# # print(board.toString())
	# # print(board.toCostString())
	# # print(board.showPathString(path))
	#
	# # Test 3
	# board = Board(3, 3)
	# board.insertBoardEntity((2, 0), GameBoardEntityEnum.SnakeHead)
	# board.insertBoardEntity((1, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((2, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((2, 2), GameBoardEntityEnum.Food)
	# path = board.aStarSearch((2, 0), (2, 2))
	# # print(board.toString())
	# # print(board.toCostString())
	# # print(board.showPathString(path))
	#
	# board = Board(5, 5)
	# board.insertBoardEntity((0, 0), GameBoardEntityEnum.SnakeHead)
	# board.insertBoardEntity((1, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((2, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((3, 1), GameBoardEntityEnum.Obstacle)
	# board.insertBoardEntity((4, 4), GameBoardEntityEnum.Food)
	# path = board.aStarSearch((0, 0), (4, 4))
	# # print(board.toString())
	# # print(board.toCostString())
	# print(board.showPathString(path))




	return 1


main()
