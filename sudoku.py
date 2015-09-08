import sys
import copy

DEBUG = False

class Tile:
    value = None
    eliminatedValues = None
    def __init__(self, char):
        self.eliminatedValues = set()
        if char != ' ':
            self.value = int(char)

    def print(self):
        if self.value is not None:
            print(self.value, end="")
        else:
            print(" ", end="")
        if DEBUG:
            print("("+str(self.eliminatedValues)+")")

class Board:
    board = []  # 2d array of tiles
    def __init__(self, contents):
        for line in contents.split('\n'):
            l = list(line)
            tiles = []
            for char in l:
                tiles.append(Tile(char))
            self.board.append(tiles)

    
    def print(self):
        for row in self.board:
            for tile in row:
                tile.print()
            print("")

    def __eliminateHorizontally(self):
        for row in self.board:
            for tile in row:
                tile.eliminatedValues.update(set(t.value for t in row))

    def __eliminateVertically(self):
        for i in range(9):
            valuesInColumn = set()
            copyOfBoard = copy.copy(self.board)
            for copyOfRow in copyOfBoard:
                if(len(copyOfRow) > 0):
                    valuesInColumn.add(copyOfRow[i].value)
            for row in self.board:
                if(len(row) > 0):
                    row[i].eliminatedValues.update(valuesInColumn)

    def __eliminateInBox(self):
        for rowBoxNum in range(3):
            for colBoxNum in range(3):
                valuesInBox = set()
                for i in range(3):
                    for j in range(3):
                        valuesInBox.add(self.board[3*rowBoxNum + i][3*colBoxNum + j].value)
                for i in range(3):
                    for j in range(3):
                        self.board[3*rowBoxNum + i][3*colBoxNum + j].eliminatedValues.update(valuesInBox)

    def __eliminatePossibilities(self):
        self.__eliminateHorizontally()
        self.__eliminateVertically()
        self.__eliminateInBox()

    def __setValues(self):
        for row in self.board:
            for tile in row:
                if tile.value is None:
                    if tile.eliminatedValues is not None:
                        if len([t for t in tile.eliminatedValues if t is not None]) == 8:
                            valueOfTile = list(set([1, 2, 3, 4, 5, 6, 7, 8, 9]) - tile.eliminatedValues)
                            if len(valueOfTile) == 1:
                                tile.value = valueOfTile[0]
                            else:
                                raise AssertionError("Something is Wrong!")

    def __findTilesWithValue(self, n):
        posWithValue = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == n:
                    posWithValue.append((i, j))
        return posWithValue

    def __findCandidatesForTwoOfThreeRule(self, n):
        positions = self.__findTilesWithValue(n)
        twoOfThreeCandidates = []
        for t1 in positions:
            for t2 in positions:
                if t1 != t2:
                    if t1[0] >= t2[0]:
                        if t1[0] // 3 == t2[0] // 3:
                            twoOfThreeCandidates.append((t1, t2))
                    if t2[0] >= t2[1]:
                        if t1[1] // 3 == t2[1] // 3:
                            twoOfThreeCandidates.append((t1, t2))
        return twoOfThreeCandidates

    def __findSubgroupsForNumber(self, n):
        # TODO FINISH THIS
        twoOfThreePairs = self.__findCandidatesForTwoOfThreeRule(n)
        print(twoOfThreePairs)
        for pair in twoOfThreePairs:
            if pair[0][0] // 3 == pair[1][0] // 3: # if x-coordinates in same box group
                pass


    def __twoOfThreeRuleForNumber(self, n):
        print(self.__findSubgroupsForNumber(n))

    def __twoOfThreeRule(self):
        for i in range(1, 10):
            self.__twoOfThreeRuleForNumber(i)

    def __done(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value is None:
                    return False
        return True

    def solve(self):
        while not self.__done():
            self.__eliminatePossibilities()
            self.__setValues()
            self.__twoOfThreeRule()

 
f = open(sys.argv[1], "r")
contents = f.read()
board = Board(contents)
f.close()

board.print()
board.solve()
board.print()

