import copy
from ..base import Piece
from ..base import Move as BaseMove

WHITE = "white"
BLACK = "black"

class Pawn(Piece):
	def legalMoves(self, pos, game, *args, **kargs):
		color = self.color
		x, y = pos
		board = game.board
		direction = 1 if color == WHITE else -1

		moves = []
		if ( (x+1,y+direction) in board and 
				self.noConflict((x+1, y+direction), game, color) ):
			moves.append(Move(self,pos, (x+1,y+direction), capture=True))

		if ( (x-1,y+direction) in board and 
				self.noConflict((x-1, y+direction), game, color) ):
			moves.append(Move(self,pos, (x-1,y+direction), capture=True))

		if ( (x,y+direction) not in board and 
				game.isInBounds((x,y+direction)) ): 
			moves.append(Move(self,pos,(x,y+direction)))

		return moves

PIECE_UNICODE = {WHITE: {Pawn: "♙"},
				 BLACK: {Pawn: "♟"}}

class Move(BaseMove):
	def __init__(self, piece, start, end, capture=False):
		self.piece = piece
		self.start = start
		self.end = end
		self.capture = capture

	def longAlgebraicNotation(self):
		pieceName = str(self.piece).upper()
		if pieceName == "P": 
			pieceName = ""
		start = str(chr(self.start[0]+97))+str(self.start[1]+1)
		end = str(chr(self.end[0]+97))+str(self.end[1]+1)

		seperater = "-" if not self.capture else "x"

		return pieceName+start+seperater+end

	def __repr__(self):
		return "Move({})".format(repr(self.longAlgebraicNotation()))

	def __str__(self):
		return self.longAlgebraicNotation()

class nPawnGame():
	"""
		The coordinate is as follows: 
		
		( 0 ,r-1) - (r-1,c-1) BLACK
		    |           |
		( 0 , 0 ) - (c-1, 0 ) WHITE
	"""
	def __init__(self, size=4): 
		if size is None: 
			size = 4

		if type(size) == int:
			size = (size,size)

		self.size = size
		self.currentColor = WHITE
		self.board = {}

		rowNum, colNum = self.size
		for col in range(colNum): 
			self.board[(col,0)] = Pawn(WHITE, "P", "Pawn")
			self.board[(col,rowNum-1)] = Pawn(BLACK, "p", "Pawn")

	def printBoard(self, style="ascii"):
		rowNum, colNum = self.size

		if style == "ascii":
			for col in range(colNum):
				print(" "+chr(col%26+97),end="")
			print("  ")
			print("--"*colNum)

			for row in range(rowNum)[::-1]:
				for col in range(colNum): 
					item = self.board.get((col,row),".")
					print(" "+str(item), end="")
				print("|"+str(row+1))

		elif style == "unicode":
			for col in range(colNum):
				print(chr(col%26+97),end="|")
			print("  ")
			print("-+"*colNum+"-")

			for row in range(rowNum)[::-1]:
				for col in range(colNum): 
					piece = self.board.get((col,row))
					if not (piece is None):
						print(str(PIECE_UNICODE[piece.color][type(piece)]), end="|")
					else:
						print(" ", end="|")
				print(str(row+1))
				if row != 0:
					print("-+"*colNum+"-")

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
		self.board[end] = piece

		self.currentColor = self.otherColor(self.currentColor)

		return True

	def peek(self, move):
		game = copy.deepcopy(self)
		if not game.isValid(move):
			return None

		game.play(move)
		return game

	def winner(self):
		rowNum, colNum = self.size
		for pos in self.board:
			piece = self.board[pos]

			if piece.color == WHITE and pos[1] == rowNum-1:
				return WHITE
			if piece.color == BLACK and pos[1] == 0:
				return BLACK

		if not self.legalMoves():
			return self.otherColor(self.currentColor)

		return None

	def loser(self):
		self.otherColor(self.winner())