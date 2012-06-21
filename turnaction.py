import constants
import cxt
import dataction
import infos
import prints
import inputs

def startgame(context):
    '''Resets context, Starts a game with full setup, runs turn() until game exits at endgame()'''
    del context
    context = cxt.CXT
    context['numplayers'] = inputs.numplayers_ask(context)
    context['player'] = dict([x, {'tilerack':[ ], "cash":6000, "stock":dict([chain, 0] for chain in constants.hotels)}] for x in range(1,context['numplayers']+1))

    #give all players six random tiles, plus initial draw       
    start_draws = {}
    for p in context['player'].keys():
        for n in range(0, 6):
            drawtile(context, p)
        drawn = drawtile(context, p)
        start_draws[p] = drawn
        context['player'][p]['tilerack'].remove(drawn)
        context['grid'][drawn]['filled'] = 1
        print "Player " + str(p) + " draws " + drawn + "." 
    
    #determine first player from initial draw
    min_draw = min(start_draws.values())
    context['cp'] = infos.find_key(start_draws, min_draw)
    print "Player " + str(context['cp']) + " starts the game "
    while 1==1:
        turn(context)

def rungame(context):
    '''Repeatedly calls turn() without performing new game setup'''
    while 1==1:
        turn(context)
       
def turn(context):
    '''cycles through the various actions of a single turn, then moves to the next player'''
    choosetile(context)
    check_endgame(context)
    buystock_ask(context)
    newtile = drawtile(context, context['cp'])
    print "Player " + str(context['cp']) + " has drawn tile " + newtile + " and his turn is over."
    bury_the_dead(context)
    
    if context['cp'] == context['numplayers']: context['cp'] = 1
    else: context['cp'] += 1

    prints.summary(context)

def choosetile(context):
    '''gets input from inputs.tile_input(), sends to placetile()'''
    
    print "Player " + str(context['cp']) + ", your tiles are: " + str(context['player'][context['cp']]["tilerack"])
    prints.print_grid_options(context)
    dataction.placetile(context, inputs.tile_input(context))

def check_endgame(context):
    '''checks whether any chain has reached a size of 41, if yes calls endgame()'''
    for x in constants.hotels:
        if infos.chainsize(context, x) > 40:
            endgame(context)

def buystock_ask(context):  
    '''Prompts current player to choose whether to buy stock this turn'''

    stock_prices = {}

    for h in constants.hotels:
        if infos.chainsize(context, h) > 0:
            stock_prices[h] = infos.price(context, h)
    
    if len(stock_prices) == 0:
        return

    print "Player " + str(context['cp']) + ", you have " + str(context['player'][context['cp']]['cash']) + " dollars."

    if context['player'][context['cp']]['cash'] < min(stock_prices.values()):
        print "You cannot afford any available shares."
        return
    else: print "Would you like to buy stock?"

    buy = inputs.buystock_ask_input(context)

    if buy == 'Y':
        dataction.buystock(context)
    elif buy == 'N':
        print "Player " + str(context['cp']) + " does not purchase stock this turn."   
        return
    else: raise NameError("buystock_ask_input() returned something other than 'Y' or 'N'...")

def drawtile(context, x):
    '''places tile from tilepool in tilereck of player x'''
    tile = context['tilepool'].pop()
    context['player'][x]['tilerack'].append(tile)
    return tile

def bury_the_dead(context): 
    '''scans tileracks and tilepool for dead tiles, removes them from the game'''
    deads = []
    for t in context['tilepool']:
        if infos.deadtile(context, t):
            deads.append(t)

    if deads != []:
        for t in deads:
            context['tilepool'].remove(t)
        print "Dead tiles " + str(deads) + " have been removed from the tile pool."

    for p in range(1, context['numplayers'] + 1):
        for t in context['player'][p]['tilerack']:
            if infos.deadtile(context, t):
                context['player'][p]['tilerack'].remove(t)
                print "Player " + str(p) + " had dead tile " + t + "."
                print "Tile is discarded and a replacement is drawn."
                drawtile(context, p)

def endgame(context):
    '''calls final_selloff(), calculates the final score, and ends the game'''

    print "The game is over!"
    print "All chains are sold."

    final_selloff(context)
    
    print "Final Score:"
    scores = {}
    for p in context['player']:
            print "Player " + str(p) + ": $" + str(context['player'][p]['cash'])
            scores[p] = context['player'][p]['cash']
    
    max_score = max(scores.values())
    
    if scores.values().count(max_score) > 1: #There is a tie for high score
            tied_players = []
            for p in context['player']:
                    if context['player'][p]["cash"] == max_score:
                            tied_players.append(p)
            print str(tied_players) + " tie for the win!"
    else: #there is one winner
            winner = infos.find_key(scores, max_score)
            print ""
            print "Player " + str(winner) + " wins the game."

            print ""
            print 'FIN.'
    raise KeyboardInterrupt

def final_selloff(context):
    '''Automatically liquidates (with no player input) all existing chains, and awards shareholder bonuses and stock sale earnings'''
    chains_left = []
    for h in constants.hotels:
        if infos.chainsize(context, h)>1:
            chains_left.append(h)

    for h in chains_left:
        print "Liquidating " + h + ":"
        shareholders = {}
        for p in context['player'].keys():
            if context['player'][p]['stock'][h] > 0:
                shareholders[p] = context['player'][p]['stock'][h]
        
        if len(shareholders.keys()) == 0: #No shareholders
            print "No one owns stock in " + h + "? Tragic!"
            continue

        max_held =  max(set(shareholders.values()))

        if len(shareholders.keys()) == 1: # Only one shareholder
            big_winner = shareholders.keys()[0]
            print "Player " + str(big_winner) + " is the only shareholder in " + h + "."
            context['player'][big_winner]['cash'] += infos.sole_bonus(context, h)
            print "Player " + str(big_winner) + ' earns the mega-bonus of $' + str(infos.sole_bonus(context, h)) 
        elif shareholders.values().count(max_held) > 1: #Tie for max shareholder
            tied_holders = []
            for p in shareholders.keys():
                if shareholders[p] == max_held:
                    tied_holders.append(p)

            tied_bonus = (infos.maj_bonus(context, h) + infos.min_bonus(context, h)) / len(tied_holders)

            for th in tied_holders:
                print "Player " + str(th) + " is a tied max shareholder in " + h + "."
                context['player'][th]['cash'] += (tied_bonus)
                print "Player " + str(th) + " gets his split of the bounus: $" + str(tied_bonus) + "."

        else: #one max shareholder
            maj_holder = infos.find_key(shareholders, max_held)
            print "Player " + str(maj_holder) + " is the Majority Shareholder in " + h +"."
            context['player'][maj_holder]['cash'] += infos.maj_bonus(context, h)
            print "Player " + str(maj_holder) + " receives the Majority bonus of $" + str(infos.maj_bonus(context, h)) + "."

            # find the minority shareholder(s)...
            minority_holders = shareholders
            del minority_holders[maj_holder]
            max2_held = max(set(minority_holders.values()))
            
            if minority_holders.values().count(max2_held) == 1:  #There is one winning minority shareholder
                min_holder = minority_holders.keys()[0]
                print "Player " + str(min_holder) + " is the Minority Shareholder in " + h +"."
                context['player'][min_holder]['cash'] += infos.min_bonus(context, h)
                print "Player " + str(min_holder) + " receives the Minority bonus of $" + str(infos.min_bonus(context, liquid)) + "."

            else: #there is a tie for winning minority holder
                print "There is a tie for minority shareholder in " + liquid + '.'
                tied_holders = []
                for p in minority_holders.keys():
                    if minority_holders[p] == max2_held:
                        tied_holders.append(p)

                tie_min_bonus = infos.min_bonus(context, liquid)/minority_holders.values().count(max2_held)

                for th in tied_holders:
                    print "Player " + str(th) + " is a tied minority shareholder in " + h + "."
                    context['player'][th]['cash'] += (tie_min_bonus)
                    print "Player " + str(th) + " gets a split of the bounus, $:" + str(tie_min_bonus) + "."

        #Sell off all stock in chain
        for p in shareholders:
            context['player'][p]['cash'] += (context['player'][p]['stock'][h] * infos.price(context, h))
            print "Player " + str(p) + " earns $" + str((context['player'][p]['stock'][h] * infos.price(context, h))) + " from the sale of " + str(context['player'][p]['stock'][h]) + " shares of " + h + " stock."
            context['player'][p]['stock'][h] = 0     
