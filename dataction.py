import constants
import turnaction
import infos
import inputs

def placetile(context, x): #place tile x

    context['player'][context['cp']]['tilerack'].remove(x)
    #determine result:
    # Tile has no neighbors: nothing happens
    if infos.filled_neighbors(context, x) == []:
        context['grid'][x]['filled'] = 1
        return

    # neighors all of chain x, or some chain x and some unaffiliated: grow chain x
    elif len(infos.neighbor_chains(context, x)) == 1:
        context['grid'][x]['chain'] = infos.neighbor_chains(context, x)[0]
        for f in infos.filled_neighbors(context, x):
            context['grid'][f]['chain'] = infos.neighbor_chains(context, x)[0]
        context['grid'][x]['filled'] = 1

    # neighbor(s) that are all no chain: new chain
    elif len(infos.neighbor_chains(context, x)) == 0:
        newchain_at(context, x)
        context['grid'][x]['filled'] = 1

    # neighbors of more than one chain: MERGER!
    elif len(infos.neighbor_chains(context, x)) > 1:
        merger_at(context, x)
        context['grid'][x]['filled'] = 1


def newchain_at(context, x):
    """creates a new hotel chain with tile placed at x"""
    print "You have created a new chain."
    print "Available hotels are " + str(infos.free_hotels(context))
    new = inputs.newchain_input(context)
    for tile in infos.filled_neighbors(context, x):
        context['grid'][tile]['chain'] = new
    
    context['grid'][x]['chain'] = new
    context['player'][context['cp']]['stock'][new] = context['player'][context['cp']]['stock'][new] + 1
    context['stock'][new] = context['stock'][new]-1
    print "Player " + str(context['cp']) + " gets 1 free share of " + new + "."

def merger_at(context, x):
    """executes chain merger with tile placed at x"""
    print "Placing this tile creates a merger!"
    
    #find sizes of neighboring chains
    n_chain_sizes = {}
    for r in infos.neighbor_chains(context, x):
        n_chain_sizes[r] = infos.chainsize(context, r)

    # If two or more largest neighbor chains are the same size, player must choose merge direction
    maxsize = max(set(n_chain_sizes.values()))
    if n_chain_sizes.values().count(maxsize) > 1:
        contenders = []
        for n in n_chain_sizes.keys():
            if n_chain_sizes[n] == maxsize:
                contenders.append(n)
        
        dom = inputs.merge_dir_input(context, contenders)

    # if one chain is largest, merge direction is set automatically
    else:
        dom = find_key(n_chain_sizes, maxsize)
        print dom + " dominates this merger."

    # Shareholders in chains getting eaten now get bonuses and choose what to do with their stock
    non_doms = infos.neighbor_chains(context, x)
    non_doms.remove(dom)  #this is now a list of the chains getting eaten

    for liquid in non_doms:
        bonus_winners = infos.find_holders(context, liquid)

        if bonus_winners == [[],[]]: #no shareholders at all
            print liquid + " has no shareholders!  Tragic!"

        elif len(bonus_winners[0]) > 1: #tie for Majority
            print "Players " + str(bonus_winners[0]) + " tie for majority shareholder in " + liquid + "."
            split_bonus = infos.sole_bonus(context, liquid)/len(bonus_winners[0])
            print "Each receives an exit bonus of $" + str(split_bonus)

            for tied_maj in bonus_winners[0]:
                context['player'][tied_maj]['cash'] += split_bonus
                sell_stock(context, tied_maj, liquid)
                trade_stock(context, tied_maj, liquid, dom)

        elif len(bonus_winners[0]) == 1 and bonus_winners[1] == []: #Only one shareholder
            print "Player " + str(bonus_winners[0][0]) + " is the only shareholder."
            context['player'][bonus_winners[0][0]]['cash'] += infos.sole_bonus(context, liquid)
            print "Player " + str(bonus_winners[0][0]) + " receives a buyout bonus of $" + str(infos.sole_bonus(context, liquid))
            sell_stock(context, bonus_winners[0][0], liquid)
            trade_stock(context, bonus_winners[0][0], liquid, dom)

        else: # One maj shareholder, one or more mins
            print "Player " + str(bonus_winners[0][0]) + " is the Majority shareholder in " + liquid + '.'
            context['player'][bonus_winners[0][0]]['cash'] += infos.maj_bonus(context, liquid)
            print "Player " + str(bonus_winners[0][0]) + " receives a buyout bonus of $" + str(infos.maj_bonus(context, liquid))
            sell_stock(context, bonus_winners[0][0], liquid)
            trade_stock(context, bonus_winners[0][0], liquid, dom)

            if len(bonus_winners[1]) == 1: # single winning minority holder
                print "Player " + str(bonus_winners[1][0]) + " is the winning minority shareholder in " + liquid + '.'
                context['player'][bonus_winners[1][0]]['cash'] += infos.min_bonus(context, liquid)
                print "Player " + str(bonus_winners[1][0]) + " receives a buyout bonus of $" + str(infos.min_bonus(context, liquid))
                sell_stock(context, bonus_winners[1][0], liquid)
                trade_stock(context, bonus_winners[1][0], liquid, dom)
            
            elif len(bonus_winners[1]) > 1: #tie for min bonus
                print "Players " + str(bonus_winners[1]) + " tie for minority shareholder in " + liquid + "."
                split_bonus = infos.min_bonus(context, liquid)/len(bonus_winners[1])
                print "Each receives an exit bonus of $" + str(split_bonus)

                for tied_min in bonus_winners[1]:
                    context['player'][tied_min]['cash'] += split_bonus
                    sell_stock(context, tied_min, liquid)
                    trade_stock(context, tied_min, liquid, dom)

    for chain in non_doms: #add all acquired chains to dominant chain.
        for tile in context['grid'].keys():
            if context['grid'][tile]['chain'] == chain:
                context['grid'][tile]['chain'] = dom

    context['grid'][x]['chain'] = dom #add merger tile to dominant chain            

def sell_stock(context, p, chain): # shareholder chooses how much stock to sell upon being acquired
    print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][chain]) + " shares of " + chain + " stock."
    print "Do you want to sell any stock for $" + str(infos.price(context, chain)) + " per share?"

    sell = inputs.sell_stock_ask_input(context, p, chain)
    if sell == "Y":
        
        print "How many shares would you like to sell?"
        sell_shares = inputs.sell_stock_shares_input(context, p, chain)
    
        context['player'][p]['stock'][chain] -= sell_shares
        context['player'][p]['cash'] += (sell_shares * infos.price(context, chain))
        context['stock'][chain] += sell_shares
        print "Player " + str(p) + " sells " + str(sell_shares) + " shares of " + chain + " for a total of $" + str(sell_shares * infos.price(context, chain)) + "."
        
    else: #Player chooses not to sell stock this turn
        print "Player " + str(p) + " does not sell any " + chain + " stock."
         
        
def trade_stock(context, p, liquid, dom): ## shareholder chooses how many shares of liquid to exchange for shares of dom
    if context['stock'][dom] == 0:
        print "There are no shares of " + dom + " in the bank for which to exchange."
        return
    elif context['player'][p]['stock'][liquid] < 2:
        print "You do not have enough shares of " + liquid + "to make a trade."
        return
    else:
        print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][liquid]) + " shares of " + liquid + " stock."
        print "There are " + str(context['stock'][dom]) + " shares of " + dom + " in the bank."
        print "How many shares of " + liquid + " would you like to trade in, at 2 to 1?"
        trade_shares = int(raw_input("Enter an even number"))
        if (trade_shares % 2) != 0:
            print "Not an even number."
            trade_shares = str(raw_input("Enter an even number"))
        elif  trade_shares > context['player'][p]['stock'][liquid]:
            print "You don't have that many shares."
            trade_stock(context, p, liquid, dom)
            return
        elif trade_shares % 2 > context['stock'][dom]:
            print "There are only " + str(context['stock'][dom]) + " shares of " + dom + " in the bank."
            print "The maximum number of shares you can trade in is " + str(context['stock'][dom] * 2) +"."
            trade_stock(context, p, liquid, dom)
            return
        else:
            context['player'][p]['stock'][liquid] -= trade_shares
            context['stock'][liquid] += trade_shares
            context['player'][p]['stock'][dom] += (trade_shares / 2)
            context['stock'][dom] -= (trade_shares % 2)
            print "Player "  + str(p) + " traded " + str(trade_shares) + " " + liquid + " for " + str(trade_shares / 2) + " " + dom + "."
            return        
    
def buystock(context):
    avail_stock = {}
    shares_bought = 0
    while 1 == 1:
        print "Available purchases are:"
        for h in constants.hotels:
            if context['stock'][h] > 0 and infos.chainsize(context, h) > 0:
                avail_stock[h] = context['stock'][h]
        
        for h in avail_stock.keys():
            print h + ": " + str(avail_stock[h]) + " shares available at $" + str(infos.price(context, h)) + " per share."
        
        print "Which stock would you like to buy?"
        buy_chain = raw_input("Select from: " + str(avail_stock.keys()))
        if buy_chain not in avail_stock.keys():
            print "Invalid Selection"
            continue
        else:
            print "You have " + str(context['player'][context['cp']]['cash']) + " dollars."
            
            buy_shares = int(raw_input("How many shares of " + buy_chain + " would you like to buy?"))                      

        if (shares_bought + buy_shares) > 3:
            print "Maximum 3 shares per turn."
            continue
        elif (buy_shares * infos.price(context, buy_chain)) > context['player'][context['cp']]['cash']:
            print "You don't have enough money!"
            continue
        else:
            context['player'][context['cp']]['cash'] -= (buy_shares * infos.price(context, buy_chain))
            context['player'][context['cp']]['stock'][buy_chain] += buy_shares
            context['stock'][buy_chain] -= buy_shares
            shares_bought += buy_shares

        if shares_bought > 2:
                return
        else:
            done = inputs.done_input()
            if done == "N":
                return