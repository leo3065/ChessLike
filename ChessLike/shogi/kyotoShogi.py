import copy
from ..base import Piece
from ..base import Move as BaseMove
from ..rect import posAdd, posMult

WHITE = "white"
BLACK = "black"

class ShogiPiece(Piece):
    def __init__(self, color, original):
        pieceType = type(self)
        self.color = color
        self.symbol = PIECE_SYMBOL[pieceType].lower() if color == BLACK else PIECE_SYMBOL[pieceType].upper()
        self.name = PIECE_NAME[pieceType]
        self.original = original
        

class King(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                end = xx, yy = x+dx, y+dy
                if self.noConflict(end, game, color):
                    capture = not(game.board.get(end) is None)
                    moves.append(Move(self,pos, end, capture=capture))

        return moves

class Pawn(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        end = xx, yy = x, y+direction
        if self.noConflict(end, game, color):
            capture = not(game.board.get(end) is None)
            moves.append(Move(self,pos, end, capture=capture))
            moves.append(Move(self,pos, end, capture=capture, promote=True))

        return moves

class Rook(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(0,1),(1,0),(0,-1),(-1,0)]:
            end = posAdd(pos,dd)
            while self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))
                end = posAdd(end,dd)

        return moves

class Silver(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(1,1),(0,1),(-1,1),(1,-1),(-1,-1)]:
            end = posAdd(pos,posMult(dd,direction))
            if self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))

        return moves

class Bishop(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(1,1),(1,-1),(-1,-1),(-1,1)]:
            end = posAdd(pos,dd)
            while self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))
                end = posAdd(end,dd)

        return moves

class Gold(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(1,1),(0,1),(-1,1),(1,0),(-1,0),(0,-1)]:
            end = posAdd(pos,posMult(dd,direction))
            if self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))

        return moves

class Knight(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(1,2),(-1,2)]:
            end = posAdd(pos,posMult(dd,direction))
            if self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))

        return moves

class Lance(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        end = posAdd(pos,(0,direction))
        while self.noConflict(end, game, color):
            capture = not(game.board.get(end) is None)
            moves.append(Move(self,pos, end, capture=capture))
            moves.append(Move(self,pos, end, capture=capture, promote=True))
            end = posAdd(end,(0,direction))

        return moves

class Tokin(ShogiPiece):
    def legalMoves(self, pos, game, *args, **kargs):
        color = self.color
        x, y = pos
        board = game.board
        direction = -1 if color == WHITE else 1

        moves = []
        for dd in [(1,1),(0,1),(-1,1),(1,0),(-1,0),(0,-1)]:
            end = posAdd(pos,posMult(dd,direction))
            if self.noConflict(end, game, color):
                capture = not(game.board.get(end) is None)
                moves.append(Move(self,pos, end, capture=capture))
                moves.append(Move(self,pos, end, capture=capture, promote=True))

        return moves

PIECE_PROMOTE = {King  : None  , 
                 Tokin : Lance , Lance : Tokin ,
                 Silver: Bishop, Bishop: Silver,
                 Gold  : Knight, Knight: Gold  ,
                 Pawn  : Rook  , Rook  : Pawn  }

PIECE_SYMBOL = {King  : "K", 
                Tokin : "T", Lance : "L",
                Silver: "S", Bishop: "B",
                Gold  : "G", Knight: "N",
                Pawn  : "P", Rook  : "R"}

PIECE_NAME = {King  : "King"  , 
              Tokin : "Tokin" , Lance : "Lance" ,
              Silver: "Silver", Bishop: "Bishop",
              Gold  : "Gold"  , Knight: "Knight",
              Pawn  : "Pawn"  , Rook  : "Rook"  }

PIECE_SYMBOLS_KANJI = {King  : "玉", 
                       Tokin : "と", Lance : "香",
                       Silver: "銀", Bishop: "角",
                       Gold  : "金", Knight: "桂",
                       Pawn  : "歩", Rook  : "飛"}

class Move(BaseMove):
    def __init__(self, piece, start, end, capture=False, promote=False, drop=False):
        self.piece = piece
        self.start = start
        self.end = end
        self.capture = capture
        self.promote = promote
        self.drop = drop

    def longAlgebraicNotation(self):
        pieceName = str(self.piece).upper()
        if not self.drop:
            start = str(self.start[1]+1)+str(chr(self.start[0]+97))
            end = str(self.end[1]+1)+str(chr(self.end[0]+97))

            seperater = "-" if not self.capture else "x"
            promote = "=" if not self.promote else "+"
            if PIECE_PROMOTE[type(self.piece)] is None:
                promote = ""

            return pieceName+start+seperater+end+promote
        else:
            end = str(self.end[1]+1)+str(chr(self.end[0]+97))

            seperater = "*"
            promote = ""

            return pieceName+start+seperater+end+promote

    def __repr__(self):
        return "Move({})".format(repr(self.longAlgebraicNotation()))

    def __str__(self):
        return self.longAlgebraicNotation()

class kyotoShogiGame():
    """
        The coordinate is as follows: 
        
        (c-1, 0 ) - ( 0 , 0 ) BLACK
            |           |
        (c-1,r-1) - ( 0 ,r-1) WHITE
    """
    def __init__(self): 
        self.size = (5,5)
        self.currentColor = WHITE
        self.board = {}
        self.captured = {WHITE:[], BLACK:[]}

        rowNum, colNum = self.size
        placement = [Tokin, Silver, King, Gold, Pawn]
        for col in range(colNum): 
            pieceType = placement[col]
            self.board[(col,0)]                 = pieceType(BLACK, pieceType)
            self.board[(colNum-1-col,rowNum-1)] = pieceType(WHITE, pieceType)

    def printBoard(self, style="ascii"):
        rowNum, colNum = self.size

        if style == "ascii":
            for col in range(colNum)[::-1]:
                print(" "+chr(col%26+97),end="")
            print("  ")
            print("--"*colNum)

            for row in range(rowNum):
                for col in range(colNum)[::-1]: 
                    item = self.board.get((col,row),".")
                    print(" "+str(item), end="")
                print("|"+str(row+1))

    def isInBounds(self, pos):
        x, y = pos
        rowNum, colNum = self.size

        return (0 <= x < colNum) and (0 <= y < rowNum) 

    def legalMoves(self, color=None):
        if color is None:
            color = self.currentColor

        moves = []
        for pos in self.board:
            piece = self.board[pos]
            if piece.color == color:
                moves += piece.legalMoves(pos, self)
        return moves

    def isAttacked(self, pos, color=None):
        if color is None:
            color = self.otherColor(self.currentColor)

        for pos in self.board:
            piece = self.board[pos]
            if piece.color == color:
                if piece.isValid(pos, self):
                    return True
        return False

    def isValid(self, move):
        return move in self.legalMoves()

    def otherColor(self,color=None):
        if color == WHITE:
            return BLACK
        if color == BLACK:
            return WHITE
        return None

    def play(self, move): 
        if not self.isValid(move):
            return False

        start = move.start 
        end = move.end

        piece = self.board.pop(start)
        if move.capture:
            captured = self.board[end].original
            self.captured[self.currentColor].append(
                    captured(self.currentColor, captured))

        if move.promote:
            pieceType = type(piece)
            promoted = PIECE_PROMOTE[pieceType]
            piece = promoted(piece.color, pieceType)
        self.board[end] = piece

        self.currentColor == self.otherColor(self.currentColor)

        return True

    def peek(self, move):
        game = copy.deepcopy(self)
        if not game.isValid(move):
            return None

        game.play(move)
        return game

    def winner(self):
        rowNum, colNum = self.size

        if not self.legalMoves():
            return self.otherColor(self.currentColor)

        return None

    def loser(self):
        self.otherColor(self.winner())