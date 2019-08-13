from functools import total_ordering

class Piece():
    def __init__(self, color, symbol, name, legalMoves=None):
        self.symbol = symbol
        self.name = name
        self.color = color

        self._legalMoves = legalMoves

    def __repr__(self):
        pieceType = self.name
        return "{}({})".format(pieceType,self.color)

    def __str__(self):
        return self.symbol

    def noConflict(self, pos, game, color=None):
        if color is None:
            color = self.color

        board = game.board
        return ( game.isInBounds(pos) and 
                ((pos not in board) or board[pos].color != color) )

    def legalMoves(self, game, *args, **kargs):
        if self._legalMoves is None:
            return []
        else:
            return self._legalMoves(game, *args, **kargs)

    def isValid(self, pos, game, *args, **kargs):
        return pos in self.legalMoves(self, game, *args, **kargs)

    def __eq__(self, that):
        return ( self.name == that.name
            and  self.color == that.color )

@total_ordering
class Move():
    def __init__(self, piece, start, end):
        self.piece = piece
        self.start = start
        self.end = end

    def __eq__(self, that):
        return ( self.piece == that.piece
            and  self.start == that.start
            and  self.end   == that.end )

    def __lt__(self, that):
        if self.start < that.start:
            return True
        if self.end < that.end:
            return True
        return False
