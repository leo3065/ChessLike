import random

def randomMove(game): 
    return random.choice(game.legalMoves())

def minOpponents(game, eval=None):
    if eval is None: 
        eval = lambda move: len(game.peek(move).legalMoves())

    moves = game.legalMoves()
    random.shuffle(moves)
    moves.sort(key=eval)
    return moves[0]
