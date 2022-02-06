import pygame as py
import chess
import discord


# some of the following code is taken from the chess minimax project

class chessGame:
    def __init__(self, id):
        self.moveCount = 0
        self.imagePath = "chessImages/"+str(id)+"board.png"
        self.board = chess.Board()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.imageNames = ['b', 'k', 'n', 'p', 'q', 'r', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        self.white, self.black = (252, 204, 116), (87, 58, 46)
        self.SQDI = self.WIDTH // 8
        self.screen = py.display.set_mode((self.WIDTH, self.HEIGHT))

        # this is very inefficient, however more efficient ways seem to break it
        b = py.transform.scale(py.image.load("chessImages/b.png"), (self.SQDI, self.SQDI))
        k = py.transform.scale(py.image.load("chessImages/k.png"), (self.SQDI, self.SQDI))
        n = py.transform.scale(py.image.load("chessImages/n.png"), (self.SQDI, self.SQDI))
        p = py.transform.scale(py.image.load("chessImages/p.png"), (self.SQDI, self.SQDI))
        q = py.transform.scale(py.image.load("chessImages/q.png"), (self.SQDI, self.SQDI))
        r = py.transform.scale(py.image.load("chessImages/r.png"), (self.SQDI, self.SQDI))
        wB = py.transform.scale(py.image.load("chessImages/wB.png"), (self.SQDI, self.SQDI))
        wK = py.transform.scale(py.image.load("chessImages/wK.png"), (self.SQDI, self.SQDI))
        wN = py.transform.scale(py.image.load("chessImages/wN.png"), (self.SQDI, self.SQDI))
        wP = py.transform.scale(py.image.load("chessImages/wP.png"), (self.SQDI, self.SQDI))
        wQ = py.transform.scale(py.image.load("chessImages/wQ.png"), (self.SQDI, self.SQDI))
        wR = py.transform.scale(py.image.load("chessImages/wR.png"), (self.SQDI, self.SQDI))

        self.IMAGES = {
            "b": b,
            "k": k,
            "n": n,
            "p": p,
            "r": r,
            "q": q,
            "B": wB,
            "K": wK,
            "N": wN,
            "P": wP,
            "Q": wQ,
            "R": wR
        }

    def updateBoard(self):
        count = 0
        self.screen.fill(self.white)
        for n in range(8):
            for j in range(8):
                if count % 2 == 0:
                    py.draw.rect(self.screen, self.white, [self.SQDI * j, self.SQDI * n, self.SQDI, self.SQDI])
                    count += 1

                else:
                    py.draw.rect(self.screen, self.black, [self.SQDI * j, self.SQDI * n, self.SQDI, self.SQDI])
                    count += 1
            count += 1

        for m in range(8):
            for j in range(1, 9):
                if self.board.piece_at(int(j + m * 8 - 1)) is not None:
                    self.screen.blit(self.IMAGES[str(self.board.piece_at((j + m * 8) - 1))], (
                        self.SQDI * j - (self.WIDTH / 8), ((self.WIDTH / 8 * 7) - self.SQDI * m)))
                    # uses m and j values to work out which piece it has, and where it should go

        py.image.save(self.screen, self.imagePath)

    def legalMoves(self):
        lmoves = []
        for moves in self.board.legal_moves:
            lmoves.append(str(moves))
        return lmoves

    def makeMove(self, playerMove):
        self.moveCount += 1
        self.board.push_uci(playerMove)

    def resetBoard(self):
        self.board = chess.Board()
        self.updateBoard()
