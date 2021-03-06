import sys

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
        for a in range(3):
            for b in range(3):
                for i in range(3):
                    for j in range(3):
                        print(" ", end="")
                        self.board[3*a + b][3*i + j].print()
                        print(" ", end="")
                    if i != 2:    
                        print("|", end="")
                if b != 2:
                    print("")
            if a != 2:
                print("\n-----------------------------")
        print("\n\n")

    def __eliminateHorizontally(self):
        for row in self.board:
            for tile in row:
                tile.eliminatedValues.update(set(t.value for t in row))

    def __getValuesInColumn(self, i):
        valuesInColumn = set()
        for row in self.board:
            if len(row) > 0:
                valuesInColumn.add(row[i].value)
        return valuesInColumn


    def __eliminateVertically(self):
        for i in range(9):
            valuesInColumn = self.__getValuesInColumn(i)
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
                    if t1[1] >= t2[1]:
                        if t1[1] // 3 == t2[1] // 3:
                            twoOfThreeCandidates.append((t1, t2))
        return twoOfThreeCandidates

    def __findSubgroupsForNumber(self, n):
        # TODO REFACTOR THIS CAUSE ITS GROSS
        twoOfThreePairs = self.__findCandidatesForTwoOfThreeRule(n)
        possibleTriples = []
        for pair in twoOfThreePairs:
            if pair[0][0] // 3 == pair[1][0] // 3: # if y-coordinates in same box group
                boxGroup = pair[0][0] // 3
                possibleYcos = set([3*boxGroup, 3*boxGroup + 1, 3*boxGroup+2]) 
                y1 = pair[0][0]
                y2 = pair[1][0]
                takenYcos = set([y1, y2])
                thirdCoordSet = possibleYcos - takenYcos
                if len(thirdCoordSet) == 1:
                    yCo = list(thirdCoordSet)[0]
                    xBoxGroup1 = pair[0][1] // 3
                    xBoxGroup2 = pair[1][1] // 3
                    xBoxGroupSet = set([0,1,2]) - set([xBoxGroup1, xBoxGroup2])
                    if len(xBoxGroupSet) == 1:
                        xBoxGroup = list(xBoxGroupSet)[0]
                        possibleSpots = ((yCo, 3*xBoxGroup), (yCo, 3*xBoxGroup+1), (yCo, 3*xBoxGroup+2))  # one of these three spots must be n
                        possibleTriples.append(possibleSpots)
                    else:
                        raise AssertionError("dsfsfdsfdsfdsf")
                else:
                    raise AssertionError("KLDSJFDKLSFJDKLSFJ")
            if pair[0][1] // 3 == pair[1][1] // 3: # x-cos are in same box group
                boxGroup = pair[0][1] // 3
                possibleXcos = set([3*boxGroup, 3*boxGroup + 1, 3*boxGroup+2]) 
                x1 = pair[0][1]
                x2 = pair[1][1]
                takenXcos = set([x1, x2])
                thirdCoordSet = possibleXcos - takenXcos
                if len(thirdCoordSet) == 1:
                    xCo = list(thirdCoordSet)[0]
                    yBoxGroup1 = pair[0][0] // 3
                    yBoxGroup2 = pair[1][0] // 3
                    yBoxGroupSet = set([0,1,2]) - set([yBoxGroup1, yBoxGroup2])
                    if len(yBoxGroupSet) == 1:
                        yBoxGroup = list(yBoxGroupSet)[0]
                        possibleSpots = ((3*yBoxGroup, xCo), (3*yBoxGroup+1, xCo), (3*yBoxGroup+2, xCo))  # one of these three spots must be n
                        possibleTriples.append(possibleSpots)
                    else:
                        raise AssertionError("dsfsfdsfdsfdsf")
                else:
                    raise AssertionError("KLDSJFDKLSFJDKLSFJ")
           
        return possibleTriples

    # TODO REFACTOR THESE 3 elimante methods into one method
    def __eliminateHorizontallyTwoOfThreeRule(self, n, remTrips):
        stillRemTrips = []
        for triple in remTrips:
            stillRemSpots = []
            for spot in triple:
                rowNum = spot[0]
                if n not in [t.value for t in self.board[rowNum]]:
                    stillRemSpots.append(spot)
            stillRemTrips.append(stillRemSpots)
        return stillRemTrips

    def __eliminateVerticallyTwoOfThreeRule(self, n, remTrips):
        stillRemTrips = []
        for triple in remTrips:
            stillRemSpots = []
            for spot in triple:
                colNum = spot[1]
                if n not in self.__getValuesInColumn(colNum):
                    stillRemSpots.append(spot)
            stillRemTrips.append(stillRemSpots)
        return stillRemTrips

    def __eliminateAlreadyFilledIn(self, remTrips):
        stillRemTrips = []
        for triple in remTrips:
            stillRemSpots = []
            for spot in triple:
                rowNum = spot[0]
                colNum = spot[1]
                if self.board[rowNum][colNum].value is None:
                    stillRemSpots.append(spot)
            stillRemTrips.append(stillRemSpots)
        return stillRemTrips

    def __twoOfThreeRuleForNumber(self, n):
        triples = self.__findSubgroupsForNumber(n)
        remaining = self.__eliminateHorizontallyTwoOfThreeRule(n, triples)
        remaining = self.__eliminateVerticallyTwoOfThreeRule(n, remaining)
        remaining = self.__eliminateAlreadyFilledIn(remaining)
        for remOfTriple in remaining:
            if len(remOfTriple) == 1:
                spot = list(remOfTriple)[0]
                if self.board[spot[0]][spot[1]].value == None:
                    self.board[spot[0]][spot[1]].value = n
                    print(str(n) + str(spot))
                    self.print()


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

    def checkValidSolve(self):
        #TODO PUT IN MORE VALID CHECKS TO MAKE SURE THE BOARD IS SOLVED CORRECTLY
        for row in self.board:
            if len(row) > 0:
                valuesInRow = set([t.value for t in row])
                if len(set([1,2,3,4,5,6,7,8,9]) - valuesInRow) > 0:
                    return False
                if len(valuesInRow) != 9:
                    return False
        return True
 
f = open(sys.argv[1], "r")
contents = f.read()
board = Board(contents)
f.close()

board.print()
board.solve()
board.print()
print(board.checkValidSolve())

