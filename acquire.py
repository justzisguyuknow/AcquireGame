import datetimeimport randomimport sysimport jsondef find_key(dic, val):    """return the key of dictionary dic given the value"""    return [k for k, v in dic.iteritems() if v == val][0]##CONSTANTSletters = "abcdefghi"num = range(1, 13)hotels = ['Luxor', 'Tower', 'American', 'Worldwide', 'Festival', 'Imperial', 'Continental']tier = {'Tower':0, 'Luxor':0, 'American':1, 'Festival':1, 'Worldwide':1, 'Continental':2, 'Imperial':2}##CHANGING ASSIGNMENTS (CONTEXT VARS)context = {}context['numplayers'] = 4 #default value, can be changed by startgame()context['grid'] = dict([('{0}{1}'.format(l,n),{'filled':0, 'chain':0}) for l in letters for n in num])context['stock'] = dict([[h, 25] for h in hotels])context['tilepool'] = context['grid'].keys()context['player'] = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in hotels)}] for x in range(1,context['numplayers']+1))context['cp'] = 1random.shuffle(context['tilepool'])    ###TURN ACTIONSdef start():    '''starts game with context (avoids need to pass context to startgame())'''    startgame(context)def run():    '''Passes context to rungame()'''    rungame(context)def startgame(context):    '''Starts a game with full setup, runs turn() until game exits at endgame()'''    context['numplayers'] = numplayers_ask(context)    context['player'] = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in hotels)}] for x in range(1,context['numplayers']+1))    for x in range(1, context['numplayers'] + 1): #give all players six random tiles        for n in range(0, 6):            drawtile(context, x)    lowtile = min([tup(context['tilepool'][n]) for n in range(1, context['numplayers']+1)])    context['cp'] = context['tilepool'].index(lowtile[0] + str(lowtile[1]))    for n in range(1, context['numplayers'] + 1):        print "Player " + str(n) + " draws " + context['tilepool'][n]        print ""    print "Player " + str(context['cp']) + " starts the game "    while 1==1:        turn(context)def rungame(context):    '''Repeatedly calls turn() without performing new game setup'''    while 1==1:        turn(context)       def turn(context):        choosetile(context)    check_endgame(context)    buystock_ask(context)    newtile = drawtile(context, context['cp'])    print "Player " + str(context['cp']) + " has drawn tile " + newtile + " and his turn is over."    bury_the_dead(context)        if context['cp'] == context['numplayers']: context['cp'] = 1    else: context['cp'] += 1    summary(context)def choosetile(context):    '''gets input from tile_input(), sends to placetile()'''        print "Player " + str(context['cp']) + ", your tiles are: " + str(context['player'][context['cp']]["tilerack"])    print_grid_options(context)    placetile(context, tile_input(context))def check_endgame(context):    '''checks whether any chain has reached a size of 41, if yes calls endgame()'''    for x in hotels:        if chainsize(context, x) > 40:            endgame(context)def buystock_ask(context):      '''Prompts current player to choose whether to buy stock this turn'''    stock_prices = {}    for h in hotels:        if chainsize(context, h) > 0:            stock_prices[h] = price(context, h)        if len(stock_prices) == 0:        return    print "Player " + str(context['cp']) + ", you have " + str(context['player'][context['cp']]['cash']) + " dollars."    if context['player'][context['cp']]['cash'] < min(stock_prices.values()):        print "You cannot afford any available shares."        return    else: print "Would you like to buy stock?"    buy = buystock_ask_input(context)    if buy == 'Y':        buystock(context)    elif buy == 'N':        print "Player " + str(context['cp']) + " does not purchase stock this turn."           return    else: raise NameError("buystock_ask_input() returned something other than 'Y' or 'N'...")def drawtile(context, x):    '''places tile from tilepool in tilereck of player x'''    tile = context['tilepool'].pop()    context['player'][x]['tilerack'].append(tile)    return tiledef bury_the_dead(context): #scans tileracks and tilepool for dead tiles, removes them from the game    deads = []    for t in context['tilepool']:        if deadtile(context, t):            deads.append(t)    if deads != []:        for t in deads:            context['tilepool'].remove(t)        print "Dead tiles " + str(deads) + " have been removed from the tile pool."    for p in range(1, context['numplayers'] + 1):        for t in context['player'][p]['tilerack']:            if deadtile(context, t):                context['player'][p]['tilerack'].remove(t)                print "Player " + str(p) + " had dead tile " + t + "."                print "Tile is discarded and a replacement is drawn."                drawtile(context, p)def endgame(context): #calculates the score and ends the game    print "The game is over!"    print "All chains are sold."    final_selloff(context)        print "Final Score:"    scores = {}    for p in context['player']:            print "Player " + str(p) + ": $" + str(context['player'][p]['cash'])            scores[p] = context['player'][p]['cash']        max_score = max(scores.values())        if scores.values().count(max_score) > 1: #There is a tie for high score            tied_players = []            for p in context['player']:                    if context['player'][p]["cash"] == max_score:                            tied_players.append(p)            print str(tied_players) + " tie for the win!"    else: #there is one winner            winner = find_key(scores, max_score)            print ""            print "Player " + str(winner) + " wins the game."    sys.exit()def final_selloff(context):    chains_left = []    for h in hotels:        if chainsize(context, h)>1:            chains_left.append(h)    for h in chains_left:        print "Liquidating " + h + ":"        shareholders = {}        for p in context['player'].keys():            if context['player'][p]['stock'][h] > 0:                shareholders[p] = context['player'][p]['stock'][h]                if len(shareholders.keys()) == 0: #No shareholders            print "No one owns stock in " + h + "? Tragic!"            continue        max_held =  max(set(shareholders.values()))        if len(shareholders.keys()) == 1: # Only one shareholder            big_winner = shareholders.keys()[0]            print "Player " + str(big_winner) + " is the only shareholder in " + h + "."            context['player'][big_winner]['cash'] += sole_bonus(context, h)            print "Player " + str(big_winner) + ' earns the mega-bonus of $' + str(sole_bonus(context, h))         elif shareholders.values().count(max_held) > 1: #Tie for max shareholder            tied_holders = []            for p in shareholders.keys():                if shareholders[p] == max_held:                    tied_holders.append(p)            tied_bonus = (maj_bonus(context, h) + min_bonus(context, h)) / len(tied_holders)            for th in tied_holders:                print "Player " + str(th) + " is a tied max shareholder in " + h + "."                context['player'][th]['cash'] += (tied_bonus)                print "Player " + str(th) + " gets his split of the bounus: $" + str(tied_bonus) + "."        else: #one max shareholder            maj_holder = find_key(shareholders, max_held)            print "Player " + str(maj_holder) + " is the Majority Shareholder in " + h +"."            context['player'][maj_holder]['cash'] += maj_bonus(context, h)            print "Player " + str(maj_holder) + " receives the Majority bonus of $" + str(maj_bonus(context, h)) + "."            # find the minority shareholder(s)...            minority_holders = shareholders            del minority_holders[maj_holder]            max2_held = max(set(minority_holders.values()))                        if minority_holders.values().count(max2_held) == 1:  #There is one winning minority shareholder                min_holder = minority_holders.keys()[0]                print "Player " + str(min_holder) + " is the Minority Shareholder in " + h +"."                context['player'][min_holder]['cash'] += min_bonus(context, h)                print "Player " + str(min_holder) + " receives the Minority bonus of $" + str(min_bonus(context, liquid)) + "."            else: #there is a tie for winning minority holder                print "There is a tie for minority shareholder in " + liquid + '.'                tied_holders = []                for p in minority_holders.keys():                    if minority_holders[p] == max2_held:                        tied_holders.append(p)                tie_min_bonus = min_bonus(context, liquid)/minority_holders.values().count(max2_held)                for th in tied_holders:                    print "Player " + str(th) + " is a tied minority shareholder in " + h + "."                    context['player'][th]['cash'] += (tie_min_bonus)                    print "Player " + str(th) + " gets a split of the bounus, $:" + str(tie_min_bonus) + "."        #Sell off all stock in chain        for p in shareholders:            context['player'][p]['cash'] += (context['player'][p]['stock'][h] * price(context, h))            print "Player " + str(p) + " earns $" + str((context['player'][p]['stock'][h] * price(context, h))) + " from the sale of " + str(context['player'][p]['stock'][h]) + " shares of " + h + " stock."            context['player'][p]['stock'][h] = 0     ### DATA ACTIONS  def placetile(context, x): #place tile x    context['player'][context['cp']]['tilerack'].remove(x)    #determine result:    # Tile has no neighbors: nothing happens    if filled_neighbors(context, x) == []:        context['grid'][x]['filled'] = 1        return    # neighors all of chain x, or some chain x and some unaffiliated: grow chain x    elif len(neighbor_chains(context, x)) == 1:        context['grid'][x]['chain'] = neighbor_chains(context, x)[0]        for f in filled_neighbors(context, x):            context['grid'][f]['chain'] = neighbor_chains(context, x)[0]        context['grid'][x]['filled'] = 1    # neighbor(s) that are all no chain: new chain    elif len(neighbor_chains(context, x)) == 0:        newchain_at(context, x)        context['grid'][x]['filled'] = 1    # neighbors of more than one chain: MERGER!    elif len(neighbor_chains(context, x)) > 1:        merger_at(context, x)        context['grid'][x]['filled'] = 1def newchain_at(context, x):    """creates a new hotel chain with tile placed at x"""    print "You have created a new chain."    print "Available hotels are " + str(free_hotels(context))    new = newchain_input(context)    for tile in filled_neighbors(context, x):        context['grid'][tile]['chain'] = new        context['grid'][x]['chain'] = new    context['player'][context['cp']]['stock'][new] = context['player'][context['cp']]['stock'][new] + 1    context['stock'][new] = context['stock'][new]-1    print "Player " + str(context['cp']) + " gets 1 free share of " + new + "."def merger_at(context, x):    """executes chain merger with tile placed at x"""    print "Placing this tile creates a merger!"        #find sizes of neighboring chains    n_chain_sizes = {}    for r in neighbor_chains(context, x):        n_chain_sizes[r] = chainsize(context, r)    # If two or more largest neighbor chains are the same size, player must choose merge direction    maxsize = max(set(n_chain_sizes.values()))    if n_chain_sizes.values().count(maxsize) > 1:        contenders = []        for n in n_chain_sizes.keys():            if n_chain_sizes[n] == maxsize:                contenders.append(n)                dom = merge_dir_input(context, contenders)    # if one chain is largest, merge direction is set automatically    else:        dom = find_key(n_chain_sizes, maxsize)        print dom + " dominates this merger."    # Shareholders in chains getting eaten now get bonuses and choose what to do with their stock    non_doms = neighbor_chains(context, x)    non_doms.remove(dom)  #this is now a list of the chains getting eaten    for liquid in non_doms:        bonus_winners = find_holders(context, liquid)        if bonus_winners == [[],[]]: #no shareholders at all            print liquid + " has no shareholders!  Tragic!"        elif len(bonus_winners[0]) > 1: #tie for Majority            print "Players " + str(bonus_winners[0]) + " tie for majority shareholder in " + liquid + "."            split_bonus = sole_bonus(context, liquid)/len(bonus_winners[0])            print "Each receives an exit bonus of $" + str(split_bonus)            for tied_maj in bonus_winners[0]:                context['player'][tied_maj]['cash'] += split_bonus                sell_stock(context, tied_maj, liquid)                trade_stock(context, tied_maj, liquid, dom)        elif len(bonus_winners[0]) == 1 and bonus_winners[1] == []: #Only one shareholder            print "Player " + str(bonus_winners[0][0]) + " is the only shareholder."            context['player'][bonus_winners[0][0]]['cash'] += sole_bonus(context, liquid)            print "Player " + str(bonus_winners[0][0]) + " receives a buyout bonus of $" + str(sole_bonus(context, liquid))            sell_stock(context, bonus_winners[0][0], liquid)            trade_stock(context, bonus_winners[0][0], liquid, dom)        else: # One maj shareholder, one or more mins            print "Player " + str(bonus_winners[0][0]) + " is the Majority shareholder in " + liquid + '.'            context['player'][bonus_winners[0][0]]['cash'] += maj_bonus(context, liquid)            print "Player " + str(bonus_winners[0][0]) + " receives a buyout bonus of $" + str(maj_bonus(context, liquid))            sell_stock(context, bonus_winners[0][0], liquid)            trade_stock(context, bonus_winners[0][0], liquid, dom)            if len(bonus_winners[1]) == 1: # single winning minority holder                print "Player " + str(bonus_winners[1][0]) + " is the winning minority shareholder in " + liquid + '.'                context['player'][bonus_winners[1][0]]['cash'] += min_bonus(context, liquid)                print "Player " + str(bonus_winners[1][0]) + " receives a buyout bonus of $" + str(min_bonus(context, liquid))                sell_stock(context, bonus_winners[1][0], liquid)                trade_stock(context, bonus_winners[1][0], liquid, dom)                        elif len(bonus_winners[1]) > 1: #tie for min bonus                print "Players " + str(bonus_winners[1]) + " tie for minority shareholder in " + liquid + "."                split_bonus = min_bonus(context, liquid)/len(bonus_winners[1])                print "Each receives an exit bonus of $" + str(split_bonus)                for tied_min in bonus_winners[1]:                    context['player'][tied_min]['cash'] += split_bonus                    sell_stock(context, tied_min, liquid)                    trade_stock(context, tied_min, liquid, dom)    for chain in non_doms: #add all acquired chains to dominant chain.        for tile in context['grid'].keys():            if context['grid'][tile]['chain'] == chain:                context['grid'][tile]['chain'] = dom    context['grid'][x]['chain'] = dom #add merger tile to dominant chain            def sell_stock(context, p, chain): # shareholder chooses how much stock to sell upon being acquired    print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][chain]) + " shares of " + chain + " stock."    print "Do you want to sell any stock for $" + str(price(context, chain)) + " per share?"    sell = sell_stock_ask_input(context, p, chain)    if sell == "Y":                print "How many shares would you like to sell?"        sell_shares = sell_stock_shares_input(context, p, chain)            context['player'][p]['stock'][chain] -= sell_shares        context['player'][p]['cash'] += (sell_shares * price(context, chain))        context['stock'][chain] += sell_shares        print "Player " + str(p) + " sells " + str(sell_shares) + " shares of " + chain + " for a total of $" + str(sell_shares * price(context, chain)) + "."            else: #Player chooses not to sell stock this turn        print "Player " + str(p) + " does not sell any " + chain + " stock."                 def trade_stock(context, p, liquid, dom): ## shareholder chooses how many shares of liquid to exchange for shares of dom    if context['stock'][dom] == 0:        print "There are no shares of " + dom + " in the bank for which to exchange."        return    elif context['player'][p]['stock'][liquid] < 2:        print "You do not have enough shares of " + liquid + "to make a trade."        return    else:        print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][liquid]) + " shares of " + liquid + " stock."        print "There are " + str(context['stock'][dom]) + " shares of " + dom + " in the bank."        print "How many shares of " + liquid + " would you like to trade in, at 2 to 1?"        trade_shares = int(raw_input("Enter an even number"))        if (trade_shares % 2) != 0:            print "Not an even number."            trade_shares = str(raw_input("Enter an even number"))        elif  trade_shares > context['player'][p]['stock'][liquid]:            print "You don't have that many shares."            trade_stock(context, p, liquid, dom)            return        elif trade_shares % 2 > context['stock'][dom]:            print "There are only " + str(context['stock'][dom]) + " shares of " + dom + " in the bank."            print "The maximum number of shares you can trade in is " + str(context['stock'][dom] * 2) +"."            trade_stock(context, p, liquid, dom)            return        else:            context['player'][p]['stock'][liquid] -= trade_shares            context['stock'][liquid] += trade_shares            context['player'][p]['stock'][dom] += (trade_shares / 2)            context['stock'][dom] -= (trade_shares % 2)            print "Player "  + str(p) + " traded " + str(trade_shares) + " " + liquid + " for " + str(trade_shares / 2) + " " + dom + "."            return            def buystock(context):    avail_stock = {}    shares_bought = 0    while 1 == 1:        print "Available purchases are:"        for h in hotels:            if context['stock'][h] > 0 and chainsize(context, h) > 0:                avail_stock[h] = context['stock'][h]                for h in avail_stock.keys():            print h + ": " + str(avail_stock[h]) + " shares available at $" + str(price(context, h)) + " per share."                print "Which stock would you like to buy?"        buy_chain = raw_input("Select from: " + str(avail_stock.keys()))        if buy_chain not in avail_stock.keys():            print "Invalid Selection"            continue        else:            print "You have " + str(context['player'][context['cp']]['cash']) + " dollars."                        buy_shares = int(raw_input("How many shares of " + buy_chain + " would you like to buy?"))                              if (shares_bought + buy_shares) > 3:            print "Maximum 3 shares per turn."            continue        elif (buy_shares * price(context, buy_chain)) > context['player'][context['cp']]['cash']:            print "You don't have enough money!"            continue        else:            context['player'][context['cp']]['cash'] -= (buy_shares * price(context, buy_chain))            context['player'][context['cp']]['stock'][buy_chain] += buy_shares            context['stock'][buy_chain] -= buy_shares            shares_bought += buy_shares        if shares_bought > 2:                return        else:            done = done_input()            if done == "N":                return## INFO FUNCTIONS (provide information about game state etc)def prev_let(a):    return letters[letters.index(a)-1]def next_let(a):    return letters[letters.index(a)+1]def tup(x):    '''splits str coordinates into tuple coordinates'''    if len(x) == 3:        return (x[0], int(x[1]+x[2]))    else: return (x[0], int(x[1]))def strin(x, y):    '''turns tuple coordinates into strings'''    return str(x) + str(y)def filled_tiles(context): ##Apparently not called anywhere... good for checking during testing    '''returns list of keys of all tiles placed on the board'''    n = []    for t in context['grid'].keys():        if context['grid'][t]['filled'] == 1:            n.append(t)    return ndef chainsize(context, x):    '''returns the number of tiles with chain value x (string)'''    c = 0    for t in context['grid']:	    if context['grid'][t]["chain"] == x:		    c = c+1    return cdef free_hotels(context):    '''returns list of hotels with chainsize 0'''    list = []    for h in hotels:        if chainsize(context, h) == 0:            list.append(h)    return listdef price(context, name):    '''the current stock shareprice for hotel chain name'''    t = tier[name]    size = chainsize(context, name)    if size<7:        return 100*(size + t)    if 6<size<11:        return 100*(6 + t)    if 10<size<21:        return 100*(7 + t)    if 20<size<31:        return 100*(8 + t)    if 30<size<41:        return 100*(9 + t)    else: return 100*(10 + t)def maj_bonus(context, name):    '''majority shareholder merger bonus for chain name'''    return price(context, name)*10def min_bonus(context, name):    '''minority shareholder merger bonus for chain name name'''    return price(context, name)*5def sole_bonus(context, name):    '''sole shareholder merger bonus for chain name name'''    return price(context, name)*15def neighbors(context, x):    '''creates a dict of a given tile's cardinal neighbors, returns fewer than 4 members if tile is on edge or corner'''    neigh = {}    if tup(x)[0] == 'a': pass    else: neigh['n'] = prev_let(tup(x)[0]) + str(tup(x)[1])    if tup(x)[0] == 'i': pass    else: neigh['s'] = next_let(tup(x)[0]) + str(tup(x)[1])    if tup(x)[1] == 1: pass    else: neigh['w'] = tup(x)[0] + str(tup(x)[1] - 1)    if tup(x)[1] == 12: pass    else: neigh['e'] = tup(x)[0] + str(tup(x)[1] + 1)    return neighdef filled_neighbors(context, x):    '''returns list of neighbors ids to x that are filled'''    n = []    for t in neighbors(context, x).values():        if context['grid'][t]['filled'] == 1:            n.append(t)        else: pass    return ndef neighbor_chains(context, x):    '''returns the list of non-zero chain values of neighbor tiles'''    nlist = [context['grid'][n]['chain'] for n in neighbors(context, x).values()] #list neigbors' chain values    nlist = list(set(nlist)) #removes duplicates    if nlist.count(0) > 0:        nlist.remove(0) #removes zeros       return nlistdef unusable(context, x):    '''tests whether a tile is temporarily unusable #because it would create a new chain,  all chains are already on the board'''    if (len(filled_neighbors(context, x)) > 0) and (len(neighbor_chains(context, x)) == 0) and (len(free_hotels(context)) == 0):        return True    else: return Falsedef deadtile(context, x):    '''tests whether tile is dead because it would merge two safe companies'''    if len(neighbor_chains(context, x)) > 1:                safelist = [] # list of 'safe' neighbors        for h in neighbor_chains(context, x):            if chainsize(context, h) > 10: safelist.append(h)                if len(safelist) > 1: return True        else: return False    else: return Falsedef networth(context, p):    '''calculates a player p's net worth (not including potential final liquidation bonuses)'''    stockworth = 0    for s in context['player'][p]['stock'].keys():            stockworth = stockworth + (price(context, s) * context['player'][p]['stock'][s])    worth = context['player'][p]['cash'] + stockworth    return worthdef find_holders(context, hotel):    """Finds the shareholders of a hotel chain who win bonuses upon liquidation, returns a list of lists: [[Majority holders],[minority holders]]"""    shareholders = []    for p in context['player'].keys():        if context['player'][p]['stock'][hotel] > 0:            shareholders[p] = context['player'][p]['stock'][hotel]        if len(shareholders.keys()) == 0: #No shareholders        return [[],[]]    max_held =  max(set(shareholders.values()))    if len(shareholders.keys()) == 1: # Only one shareholder        return [[shareholders.keys()[0]], []]            elif shareholders.values().count(max_held) > 1: #Tie for max shareholder        tied_holders = []        for p in shareholders.keys():            if shareholders[p] == max_held:                tied_holders.append(p)        return [tied_holders, []]    else: #one max shareholder        maj_holder = find_key(shareholders, max_held)        # find the minority shareholder(s)...        minority_holders = shareholders        del minority_holders[maj_holder]        max2_held = max(set(minority_holders.values()))                if minority_holders.values().count(max2_held) == 1:  #There is one winning minority shareholder            return [[maj_holder],[minority_holders.keys()[0]]]        else: #there is a tie for winning minority holder            tied_holders = []            for p in minority_holders.keys():                if minority_holders[p] == max2_held:                    tied_holders.append(p)            return [[maj_holder], tied_holders]## PRINT FUNCTIONSdef summary(context):    print_bank(context)    print_players(context)    print_hotels(context)def print_bank(context):    print "BANK: STOCK REMAINING"    print str([[h, context['stock'][h]] for h in hotels])def print_players(context):    print "PLAYERS HOLD:"    for p in context['player'].keys():        stock_hold = {}        for h in hotels:             if context['player'][p]['stock'][h] > 0:                 stock_hold[h] = context['player'][p]['stock'][h]        print "Player " + str(p) + ": $" + str(context['player'][p]['cash']) + ", Stock: " + str(stock_hold)        def print_grid_options(context):    icons = {'Tower':"T", "Luxor":"L", "American":"A", "Worldwide":'W', "Continental":"C", "Festival":"F", "Imperial":"I"}       print "|X| = a tile on the board"    print "|+| = a tile in your hand"    print "  " + " 1 " + ' 2 ' + ' 3 ' + ' 4 ' + ' 5 ' + ' 6 ' + ' 7 ' + ' 8 ' + ' 9 ' + ' 10' + ' 11' + ' 12'    for a in letters:        fil = {}        for n in num:            if (context['grid'][strin(a, n)]['filled'] == 1) and (context['grid'][strin(a, n)]['chain'] != 0):                fil[n] = "|" + icons[(context['grid'][strin(a, n)]['chain'])]  + "|"            elif (context['grid'][strin(a, n)]['filled'] == 1) and (context['grid'][strin(a, n)]['chain'] == 0):                fil[n] = "|X|"            elif strin(a, n) in context['player'][context['cp']]['tilerack']:                fil[n] = "|+|"            else: fil[n] = "|_|"        print "  " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ "        print a + " " +fil[1] + fil[2] + fil[3] + fil[4] + fil[5] + fil[6] + fil[7] + fil[8] + fil[9] + fil[10] + fil[11] + fil[12]     print ""    print ""  def print_grid(context):    icons = {'Tower':"T", "Luxor":"L", "American":"A", "Worldwide":'W', "Continental":"C", "Festival":"F", "Imperial":"I"}       print "  " + " 1 " + ' 2 ' + ' 3 ' + ' 4 ' + ' 5 ' + ' 6 ' + ' 7 ' + ' 8 ' + ' 9 ' + ' 10' + ' 11' + ' 12'    for a in letters:        fil = {}        for n in num:            if (context['grid'][strin(a, n)]['filled'] == 1) and (context['grid'][strin(a, n)]['chain'] != 0):                fil[n] = "|" + icons[(context['grid'][strin(a, n)]['chain'])]  + "|"            elif (context['grid'][strin(a, n)]['filled'] == 1) and (context['grid'][strin(a, n)]['chain'] == 0):                fil[n] = "|X|"            else: fil[n] = "|_|"        print "  " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ "        print a + " " +fil[1] + fil[2] + fil[3] + fil[4] + fil[5] + fil[6] + fil[7] + fil[8] + fil[9] + fil[10] + fil[11] + fil[12]          print ""    print ""    def print_hotels(context):	print "HOTELS ON THE BOARD:"	for h in hotels:		if chainsize(context, h) > 1:			print h + ": size = " + str(chainsize(context, h)) ### INPUT FUNCTIONS prompt user for input and check that it is valid before returningdef numplayers_ask(context):    """Asks for number of players, returns input"""    response = 0    while response == 0:        response = int(raw_input("How many players? (2-6):"))        if response in [2,3,4,5,6]:            return response        else:             print "Bad Input"            response = 0def buystock_ask_input(context):    '''Prompts for Y/N input whether current player wants to buy stock'''    response = 0    while response == 0:        response = raw_input("Player " + str(context['cp']) + ", Would you like to buy stock this turn? (Y/N):")        if response in ['Y', 'Yes', "y", 'yes']:            return "Y"        elif response in ['N', 'No', "n", 'no']:            return "N"        else:            print "Bad Input"            response = 0def tile_input(context):    tiletoplay = 0    while tiletoplay == 0:           tiletoplay = raw_input("Which tile would you like to play?")               if tiletoplay not in context['player'][context['cp']]["tilerack"]:            print "Bad Input"            tiletoplay = 0            continue        elif unusable(context, tiletoplay):            print "playing that tile would create a new chain, but all hotels are already on the board!"            tiletoplay = 0            continue        elif tiletoplay in context['player'][context['cp']]['tilerack']:            return tiletoplay        else:             raise NameError("Tile Input Not Caught!")def newchain_input(context):    new = 0    while new == 0:        new = raw_input("Which hotel would you like to found?")        if new not in free_hotels(context):            print "Bad Input."            new = 0    return newdef merge_dir_input(context, contenders):    print str(contenders) + " are the options to dominate this merger."    dom = 0    while dom == 0:        dom = raw_input("Which hotel do you choose to dominate the merger?")        if dom not in contenders:            print "Not an option"            dom = 0        else: return domdef sell_stock_ask_input(context, p, chain):    "Tells player how many shares of the chain they have and asks if they want to sell any"    print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][chain]) + " shares of " + chain + " stock."    sell = 0    while sell == 0:        sell = raw_input("Do you want to sell any stock for $" + str(price(context, chain)) + " per share? (Y/N):")        if sell in ["Y", 'y', 'Yes', "yes"]:            return 'Y'            break        elif sell in ['n', 'N', 'no', 'No']:            return 'N'            break        else:            print "Bad Input."            sell = 0def sell_stock_shares_input(context, p, chain):    print "How many shares would you like to sell?"    sell_shares = -1    while sell_shares == -1:        sell_shares = int(raw_input("Enter a number:"))        if sell_shares > context['player'][p]['stock'][chain]:            print "You don't have that many shares!"            sell_shares = -1        else: return sell_shares          def done_input():    ans = 0    while ans == 0:           ans = raw_input("Would you like to make additional purcahses?")        if ans in ["Y", 'y', 'Yes', "yes"]:            return 'y'            break        elif ans in ['n', 'N', 'no', 'No']:            return 'N'            break        else:            print "Bad Input."            ans = 0            ### SAVE AND LOAD GAMEdef savegame(context):	    game = open("savedgame.py", 'w')    now = datetime.datetime.now()    game.write("### Game" + str(n))    game.write("/n")    game.write("### Saved on " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " at " + str(now.hour) + ":" + str(now.minute) + "." + str(now.second))    game.write("/n")    game.write("context = " + str(context))    game.close()	def loadgame(context):    import savedgame    context = savedgame.context        rungame()def saver():    savegame(context)def runner():    rungame(context)