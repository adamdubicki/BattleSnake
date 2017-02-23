from GameBoardEntityEnum import GameBoardEntityEnum

class Tile():

    def __init__(self, xPosition, yPosition, entity):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.entity = GameBoardEntityEnum.Empty
        self.parent = None

    def getPositionTuple(self):
        return (self.xPosition,self.yPosition)

    def toString(self):
        tileString = "xPosition:" + str(self.xPosition)
        tileString+= " yPosition:"+str(self.yPosition)
        tileString+=" entity:" +str(self.entity)
        return tileString
