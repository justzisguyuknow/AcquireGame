import constants
import dataction
import turnaction


def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]

def prev_let(a):
    return constants.letters[constants.letters.index(a)-1]

def next_let(a):
    return constants.letters[constants.letters.index(a)+1]

def tup(x):
    '''splits str coordinates into tuple coordinates'''
    if len(x) == 3:
        return (x[0], int(x[1]+x[2]))
    else: return (x[0], int(x[1]))

def strin(x, y):
    '''turns tuple coordinates into strings'''
    return str(x) + str(y)

def filled_tiles(context): ##Apparently not called anywhere... good for checking during testing
    '''returns list of keys of all tiles placed on the board'''
    n = []
    for t in context.grid.keys():
        if context.grid[t]['filled'] == 1:
            n.append(t)
    return n

def chainsize(context, x):
    '''returns the number of tiles with chain value x (string)'''
    c = 0
    for t in context.grid:
	    if context.grid[t]["chain"] == x:
		    c = c+1
    return c

def free_hotels(context):
    '''returns list of hotels with chainsize 0'''
    list = []
    for h in constants.hotels:
        if chainsize(context, h) == 0:
            list.append(h)
    return list

def price(context, name):
    '''the current stock shareprice for hotel chain name'''
    t = constants.tier[name]
    size = chainsize(context, name)
    if size<7:
        return 100*(size + t)
    if 6<size<11:
        return 100*(6 + t)
    if 10<size<21:
        return 100*(7 + t)
    if 20<size<31:
        return 100*(8 + t)
    if 30<size<41:
        return 100*(9 + t)
    else: return 100*(10 + t)

def maj_bonus(context, name):
    '''majority shareholder merger bonus for chain name'''
    return price(context, name)*10

def min_bonus(context, name):
    '''minority shareholder merger bonus for chain name name'''
    return price(context, name)*5

def sole_bonus(context, name):
    '''sole shareholder merger bonus for chain name name'''
    return price(context, name)*15

def avail_stock(context):
    avail_stock = {}
    for h in constants.hotels:
        if context.stock[h] > 0 and chainsize(context, h) > 0:
            avail_stock[h] = context.stock[h]

    return avail_stock

def neighbors(context, x):
    '''creates a dict of a given tile's cardinal neighbors, returns fewer than 4 members if tile is on edge or corner'''
    neigh = {}
    if tup(x)[0] == 'a': pass
    else: neigh['n'] = prev_let(tup(x)[0]) + str(tup(x)[1])
    if tup(x)[0] == 'i': pass
    else: neigh['s'] = next_let(tup(x)[0]) + str(tup(x)[1])
    if tup(x)[1] == 1: pass
    else: neigh['w'] = tup(x)[0] + str(tup(x)[1] - 1)
    if tup(x)[1] == 12: pass
    else: neigh['e'] = tup(x)[0] + str(tup(x)[1] + 1)
    return neigh

def filled_neighbors(context, x):
    '''returns list of neighbors ids to x that are filled'''
    n = []
    for t in neighbors(context, x).values():
        if context.grid[t]['filled'] == 1:
            n.append(t)
        else: pass
    return n

def neighbor_chains(context, x):
    '''returns the list of non-zero chain values of neighbor tiles'''
    nlist = [context.grid[n]['chain'] for n in neighbors(context, x).values()] #list neigbors' chain values
    nlist = list(set(nlist)) #removes duplicates
    if nlist.count(0) > 0:
        nlist.remove(0) #removes zeros   
    return nlist

def unusable(context, x):
    '''tests whether a tile is temporarily unusable #because it would create a new chain,  all chains are already on the board'''
    if (len(filled_neighbors(context, x)) > 0) and (len(neighbor_chains(context, x)) == 0) and (len(free_hotels(context)) == 0):
        return True
    else: return False

def deadtile(context, x):
    '''tests whether tile is dead because it would merge two safe companies'''
    if len(neighbor_chains(context, x)) > 1:
        
        safelist = [] # list of 'safe' neighbors
        for h in neighbor_chains(context, x):
            if chainsize(context, h) > 10: safelist.append(h)
        
        if len(safelist) > 1: return True
        else: return False
    else: return False

def networth(context, p):
    '''calculates a player p's net worth (not including potential final liquidation bonuses)'''
    stockworth = 0
    for s in context.player[p]['stock'].keys():
            stockworth = stockworth + (price(context, s) * context.player[p]['stock'][s])
    worth = context.player[p]['cash'] + stockworth
    return worth

def find_holders(context, hotel):
    """Finds the shareholders of a hotel chain who win bonuses upon liquidation, returns a list of lists: [[Majority holders],[minority holders]]"""
    shareholders = {}
    for p in context.player.keys():
        if context.player[p]['stock'][hotel] > 0:
            shareholders[p] = context.player[p]['stock'][hotel]
    
    if len(shareholders.keys()) == 0: #No shareholders
        return [[],[]]

    max_held =  max(set(shareholders.values()))

    if len(shareholders.keys()) == 1: # Only one shareholder
        return [[shareholders.keys()[0]], []]  
    elif shareholders.values().count(max_held) > 1: #Tie for max shareholder
        tied_holders = []
        for p in shareholders.keys():
            if shareholders[p] == max_held:
                tied_holders.append(p)

        return [tied_holders, []]
    else: #one max shareholder
        maj_holder = find_key(shareholders, max_held)

        # find the minority shareholder(s)...
        minority_holders = shareholders
        del minority_holders[maj_holder]
        max2_held = max(set(minority_holders.values()))
        
        if minority_holders.values().count(max2_held) == 1:  #There is one winning minority shareholder
            return [[maj_holder],[minority_holders.keys()[0]]]
        else: #there is a tie for winning minority holder
            tied_holders = []
            for p in minority_holders.keys():
                if minority_holders[p] == max2_held:
                    tied_holders.append(p)
            return [[maj_holder], tied_holders]