class Piece():
	def __init__(self, color, name, legalMoves=None):
		self.name = name
		self.color = color

		self._legalMoves = legalMoves

	def __repr__(self):
		pieceType = type(self).__name__
		return "{}({})".format(pieceType,self.color)

	def __str__(self):
		return self.name

	def noConflict(self, pos, game, color=None):
		if color is None:
			color = self.color

		board = game.board
		return ( game.isInBounds(pos) and 
				((pos not in board) or board[pos].color != color) )

	def legalMoves(self, board, *args, **kargs):
		if self._legalMoves is None:
			return []
		else:
			return self._legalMoves(board, *args, **kargs)

	def isValid(self, pos, board, *args, **kargs):
		return pos in self.legalMoves(self, board, *args, **kargs)

	def __eq__(self, that):
		return ( self.name == that.name
			and  self.color == that.color )

def posAdd(pos, offs): 
	return tuple(map(sum, zip(pos, offs)))
