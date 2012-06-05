import constants
import random

CXT = {}

CXT['numplayers'] = 4 #default value, can be changed by startgame()
CXT['grid'] = dict([('{0}{1}'.format(l,n),{'filled':0, 'chain':0}) for l in constants.letters for n in constants.num])
CXT['stock'] = dict([[h, 25] for h in constants.hotels])
CXT['tilepool'] = CXT['grid'].keys()
#Players are created with no tiles in tilerack, startgame populates with random draws from tilepool
CXT['player'] = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in constants.hotels)}] for x in range(1,CXT['numplayers']+1))
CXT['cp'] = 1

random.shuffle(CXT['tilepool'])