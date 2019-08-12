import copy
from base import Piece
from functools import total_ordering

WHITE = "white"
BLACK = "black"

class Pawn(Piece):
	def __init__(self, color, name, direction):
		self.name = name
		self.color = color
		self.direction = direction

	def legalMoves(self, pos, game, *args, **kargs):
		if "color" in kargs:
			color = kargs.color
		else:
			color = self.color

		x, y = pos
		board = game.board

		moves = []
		if ( (x+1,y+self.direction) in board and 
				self.noConflict((x+1, y+self.direction), game, color) ):
			moves.append((x+1,y+self.direction))
		if ( (x-1,y+self.direction) in board and 
				self.noConflict((x-1, y+self.direction), game, color) ):
			moves.append((x-1,y+self.direction))
		if ( (x,y+self.direction) not in board and 
				game.isInBounds((x,y+self.direction)) ): 
			moves.append((x,y+self.direction))

		return moves

	def __eq__(self, that):
		return ( self.name == that.name
			and  self.color == that.color
			and  self.direction == that.direction )

pieceName = {WHITE: {Pawn: "♙"},
			 BLACK: {Pawn: "♟"}}

@total_ordering
class Move():
	def __init__(self, piece, start, end):
		self.piece = piece
		self.start = start
		self.end = end

	def longAlgebraicNotation(self):
		pieceName = str(self.piece).upper()
		if pieceName == "P": 
			pieceName = ""
		start = str(chr(self.start[0]+97))+str(self.start[1])
		end = str(chr(self.end[0]+97))+str(self.end[1])

		seperater = "-"

		return pieceName+start+seperater+end

	def __repr__(self):
		return "Move({})".format(self.longAlgebraicNotation())

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
			self.board[(col,0)] = Pawn(WHITE, "P", 1)
			self.board[(col,rowNum-1)] = Pawn(BLACK, "p", -1)

	def printBoard(self, style="ascii"):
		rowNum, colNum = self.size

		if style == "ascii":
			for col in range(colNum):
				print(chr(col%26+97),end="")
			print("| ")
			print("-"*colNum+"+-")
			for row in range(rowNum)[::-1]:
				for col in range(colNum): 
					item = self.board.get((col,row),".")
					print(str(item), end="")
				print("|"+str(row+1))
		elif style == "unicode":
			for col in range(colNum):
				print(chr(col%26+97),end="|")
			print("  ")
			print("-"*(colNum*2-1)+"+--")

			for row in range(rowNum)[::-1]:
				for col in range(colNum): 
					piece = self.board.get((col,row))
					if not (piece is None):
						print(str(pieceName[piece.color][type(piece)]), end="|")
					else:
						print(" ", end="|")
				print(str(row+1))
				print("-"*(colNum*2-1)+"+--")

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
				moves += [Move(piece, pos, endPos) 
							for endPos in piece.legalMoves(pos, self)]
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

		if self.currentColor == WHITE:
			self.currentColor = BLACK
		else:
			self.currentColor = WHITE

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