import datetimeimport randomimport sysimport jsonimport constantsimport turnactionimport datactionimport infosimport printsimport inputsimport saveloaddef find_key(dic, val):    """return the key of dictionary dic given the value"""    return [k for k, v in dic.iteritems() if v == val][0]##CHANGING ASSIGNMENTS (CONTEXT VARS)context = {}context['numplayers'] = 4 #default value, can be changed by startgame()context['grid'] = dict([('{0}{1}'.format(l,n),{'filled':0, 'chain':0}) for l in constants.letters for n in constants.num])context['stock'] = dict([[h, 25] for h in constants.hotels])context['tilepool'] = context['grid'].keys()#Players are created with no tiles in tilerack, startgame populates with random draws from tilepoolcontext['player'] = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in constants.hotels)}] for x in range(1,context['numplayers']+1))context['cp'] = 1random.shuffle(context['tilepool'])def start():    '''starts game with context (avoids need to pass context to startgame())'''    turnaction.startgame(context)def run():    '''Passes context to rungame()'''    turnaction.rungame(context)def saver():	'''shortcut for calling saveload.savegame(context)'''    saveload.savegame(context)def loader():	'''shortcut for calling saveload.loadgame(context)'''    saveload.loadgame(context)