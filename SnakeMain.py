from GameBoardEntityEnum import GameBoardEntityEnum
from Board import Board
from Tile import Tile

class SnakeMain():

    def __init__(self, json):
        self.board = self.jsonToBoard(json)

    # Need to populate the board with the JSON received
    # from the server
    def jsonToBoard(self,json):
        return Board(0,0)

    def pickGoal(self):
        return (0,0)

    #Get the next move
    def getNextMove(self):

        # 1.Compute the shortest path P1 from
        # snake S1 's head to the food.
        # If P1 exists, go to step 2.
        # Otherwise go to step 4.

        # 2. Direct a virtual snake, S2 (the same as S1), to eat the food along path P1.

        #3. Compute the longest path P2 from snake S2 's head to its tail.
        # If P2 exists, let D be the first direction in path P1. Otherwise go to step 4.

        # 4. Compute the longest path P3 from snake S1 's head to its tail.
        # If P3 exists, let D be the first direction in path P3. Otherwise go to step 5.

        # 5. Let D be the direction that furthers the snake from the food.
        return 0