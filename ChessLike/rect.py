def posAdd(pos, offs): 
	return tuple(map(sum, zip(pos, offs)))

def posMult(pos, r): 
	return tuple(p*r for p in pos)
