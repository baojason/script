#!/usr/bin/python3
from functiontester import FunctionTester as tester

class tttBoard:
    ''' Tic Tac Toe board data class '''
    def __init__(self, boardSize, rowSize):
        """ Initialize the instance variables of a tttBoard object.
            Disallows a negative boardSize and rowSize. """
        if boardSize < 3 or rowSize < 3 or rowSize > boardSize:
            raise ValueError('boardSize = %d, rowSize = %d ' % (boardSize, rowSize))
        self.__bdSz = boardSize
        self.__roSz = rowSize
        self.__bdSz0 = boardSize - 1
        self.__roSz0 = rowSize - 1

        # Initialize the game board with a boardSize * boardSize list with all 0s
        self.__bd = [ [0 for _ in range(boardSize)] for _ in range(boardSize) ]
        self.__currPlayer = 1
        self.winPt1 = (0,0)
        self.winPt2 = (0,0)

    def getBoardSize(self):
        return self.__bdSz

    def getRowSize(self):
        return self.__roSz

    def getCurrPlayer(self):
        return self.__currPlayer

    def setBoardContent(self, board):
        if len(board) == self.__bdSz and len(board[0]) == self.__bdSz:
            self.__bd = board
            return True
        return False

    def getPlayerAt(self, pt):
        x = pt[0]
        y = pt[1]
        if 0 <= x < self.__bdSz and 0 <= y < self.__bdSz:
            return self.__bd[x][y]

    def play(self, pt):
        x = pt[0]
        y = pt[1]
        if 0 <= x < self.__bdSz and 0 <= y < self.__bdSz:
            if self.__bd[x][y] == 0:
                self.__bd[x][y] = self.__currPlayer
                self.__currPlayer = 1 if self.__currPlayer != 1 else 2
                return True
        return False

    def __checkARow(self, f, t):
        '''
        f: function that calculate the index (x,y)
        t: row lenght
        '''
        ct1 = 0;
        ct2 = 0;
        w = 0
        ii = 0
        for i in range(t):
            x, y = f(i, t)
            if self.__bd[x][y] == 1:
                #player1
                ct1 += 1
                if ct1 == self.__roSz:
                    ii = i
                    w = 1
                    break
                ct2 = 0
            elif self.__bd[x][y] == 2:
                #player2
                ct2 += 1
                if ct2 == self.__roSz:
                    ii = i
                    w = 2
                    break
                ct1 = 0
            else:
                ct1 = ct2 = 0
        if w != 0:
            self.winPt1 = f(ii-self.__roSz + 1, t)
            self.winPt2 = f(ii, t)
            for j in range(ii, ii-self.__roSz, -1):
                x, y = f(j, t)
                self.__bd[x][y] += 10 #indicate this is a place of how it wins
        return w

    def CheckWinner(self):
        '''
        Use x, y as indices of the two dimention list
        There are 4 kinds of row checking
        1. along x direction
        2. along y direction
        3. along (x,y) diagonal North East
        4. along (x,y) diagonal South East
        '''
        w = 0
        # check x direction rows
        for i in range(self.__bdSz):
            w = self.__checkARow(lambda x, t : (x, i), self.__bdSz)
            if w:
                return w
        # check y direction rows
        for i in range(self.__bdSz):
            w = self.__checkARow(lambda x, t : (i, x), self.__bdSz)
            if w:
                return w

        # check 45 degree diagnal direction
        for i in range(self.__bdSz - self.__roSz + 1):
            w = self.__checkARow(lambda x, t : (t-1 - x, x), self.__roSz+i)
            if w:
                return w
            w = self.__checkARow(lambda x, t : (self.__bdSz0 - x, self.__bdSz0 - t + 1 + x), self.__roSz+i)
            if w:
                return w

            w = self.__checkARow(lambda x, t : (self.__bdSz0 - t + 1 + x, x), self.__roSz+i)
            if w:
                return w
            w = self.__checkARow(lambda x, t : (x, self.__bdSz0 - t + 1 + x), self.__roSz+i)
            if w:
                return w
        return w

    def showBoard(self):
        print("   ", end="")
        for x in range(self.__bdSz):
            print("{:>3}".format(x), end="")
        print()
        print("   ", end="")
        for i in range(self.__bdSz):
            print("---", end="")
        print()

        for x in range(self.__bdSz):
            print("%d |" % (x), end="")
            for y in range(self.__bdSz):
                print('{:>3}'.format(self.__bd[x][y]), end="")
            print()

if __name__ == '__main__':
    ttt = tttBoard(5,3)
    print("Board size = %d " % (ttt.getBoardSize()))
    t = tester()
    t.check("tttBoard getBoardSize", 5, ttt.getBoardSize)
    t.check("tttBoard getRowSize", 3, ttt.getRowSize)
    t.check("tttBoard getCurrPlayer", 1, ttt.getCurrPlayer)
    t.check("tttBoard play", True, ttt.play, (3, 2))
    t.check("tttBoard getCurrPlayer", 2, ttt.getCurrPlayer)
    t.check("tttBoard play", False, ttt.play, (3, 2))
    t.check("tttBoard play", False, ttt.play, (3, -1))
    b = [
          [0, 0, 0, 0, 0],
          [0, 0, 1, 1, 1],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]
        ]
    t.check("tttBoard setBoardContent", True, ttt.setBoardContent, b)
    t.check("tttBoard CheckWinner", 1, ttt.CheckWinner)
    b = [
          [0, 0, 0, 0, 0],
          [0, 0, 1, 2, 1],
          [0, 0, 2, 1, 1],
          [0, 0, 2, 0, 0],
          [0, 0, 2, 0, 0]
        ]
    t.check("tttBoard setBoardContent", True, ttt.setBoardContent, b)
    t.check("tttBoard CheckWinner", 2, ttt.CheckWinner)
    b = [
          [0, 0, 0, 0, 0],
          [0, 0, 1, 2, 1],
          [0, 0, 2, 1, 1],
          [0, 0, 1, 0, 0],
          [0, 0, 2, 0, 0]
        ]
    t.check("tttBoard setBoardContent", True, ttt.setBoardContent, b)
    t.check("tttBoard CheckWinner", 1, ttt.CheckWinner)
    b = [
          [0, 0, 0, 0, 0],
          [0, 0, 1, 1, 2],
          [2, 1, 2, 2, 1],
          [0, 1, 2, 0, 0],
          [0, 0, 1, 0, 0]
        ]
    t.check("tttBoard setBoardContent", True, ttt.setBoardContent, b)
    t.check("tttBoard CheckWinner", 2, ttt.CheckWinner)

    ttt.showBoard()
    ttt = tttBoard(3,3)
    b = [
          [1,1,2],
          [0,1,2],
          [2,2,1]
        ]
    t.check("tttBoard setBoardContent", True, ttt.setBoardContent, b)
    t.check("tttBoard CheckWinner", 2, ttt.CheckWinner)
    t.report_results()
    ttt.showBoard()

