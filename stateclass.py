import constants
import pickle

class State:
	name = '' #set by startgame
	numplayers = 4 #default value, can be changed by startgame()
	grid = dict([('{0}{1}'.format(l,n),{'filled':0, 'chain':0}) for l in constants.letters for n in constants.num])
	stock = dict([[h, 25] for h in constants.hotels])
	tilepool = grid.keys()
	player = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in constants.hotels)}] for x in range(1, numplayers+1))
	cp = 1

	def statesave(self): #name must be a string 
	    '''pickles the instance in named file'''
	    gamefile = open("psg"+ self.name, 'w')
	    pickle.dump(self, gamefile)
	    gamefile.close()


	    





