import constants
import infos


def summary(context):
    print_bank(context)
    print_players(context)
    print_hotels(context)
    print_chain_leaders(context)

def print_bank(context):
    print "BANK: STOCK REMAINING"
    print str([[h, context.stock[h]] for h in constants.hotels])

def print_players(context):
    print "PLAYERS HOLD:"
    for p in context.player.keys():
        stock_hold = {}
        for h in constants.hotels:
             if context.player[p]['stock'][h] > 0:
                 stock_hold[h] = context.player[p]['stock'][h]
        print "Player " + str(p) + ": $" + str(context.player[p]['cash']) + ", Stock: " + str(stock_hold)
        
def print_grid_options(context):
    icons = {'Tower':"T", "Luxor":"L", "American":"A", "Worldwide":'W', "Continental":"C", "Festival":"F", "Imperial":"I"}   
    print "|X| = a tile on the board"
    print "|+| = a tile in your hand"
    print "  " + " 1 " + ' 2 ' + ' 3 ' + ' 4 ' + ' 5 ' + ' 6 ' + ' 7 ' + ' 8 ' + ' 9 ' + ' 10' + ' 11' + ' 12'
    for a in constants.letters:
        fil = {}
        for n in constants.num:
            if (context.grid[infos.strin(a, n)]['filled'] == 1) and (context.grid[infos.strin(a, n)]['chain'] != 0):
                fil[n] = "|" + icons[(context.grid[infos.strin(a, n)]['chain'])]  + "|"
            elif (context.grid[infos.strin(a, n)]['filled'] == 1) and (context.grid[infos.strin(a, n)]['chain'] == 0):
                fil[n] = "|X|"
            elif infos.strin(a, n) in context.player[context.cp]['tilerack']:
                fil[n] = "|+|"
            else: fil[n] = "|_|"

        print "  " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ "
        print a + " " +fil[1] + fil[2] + fil[3] + fil[4] + fil[5] + fil[6] + fil[7] + fil[8] + fil[9] + fil[10] + fil[11] + fil[12] 
    print ""
    print ""  

def print_grid(context):
    icons = {'Tower':"T", "Luxor":"L", "American":"A", "Worldwide":'W', "Continental":"C", "Festival":"F", "Imperial":"I"}   
    print "  " + " 1 " + ' 2 ' + ' 3 ' + ' 4 ' + ' 5 ' + ' 6 ' + ' 7 ' + ' 8 ' + ' 9 ' + ' 10' + ' 11' + ' 12'
    for a in constants.letters:
        fil = {}
        for n in constants.num:
            if (context.grid[infos.strin(a, n)]['filled'] == 1) and (context.grid[infos.strin(a, n)]['chain'] != 0):
                fil[n] = "|" + icons[(context.grid[infos.strin(a, n)]['chain'])]  + "|"
            elif (context.grid[infos.strin(a, n)]['filled'] == 1) and (context.grid[infos.strin(a, n)]['chain'] == 0):
                fil[n] = "|X|"
            else: fil[n] = "|_|"
        print "  " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ " + " _ "
        print a + " " +fil[1] + fil[2] + fil[3] + fil[4] + fil[5] + fil[6] + fil[7] + fil[8] + fil[9] + fil[10] + fil[11] + fil[12]      
    print ""
    print ""
    
def print_hotels(context):
    if len(infos.free_hotels(context)) == 7:
        return
    else:
    	print "HOTELS ON THE BOARD:"
    	for h in constants.hotels:
    		if infos.chainsize(context, h) > 1:
    			print h + ": size = " + str(infos.chainsize(context, h))

def print_chain_leaders(context):
    '''Prints each existing chain and its leading shareholders'''
    if len(infos.free_hotels(context)) == 7:
        return
    else:
        print "CHAIN LEADERS:"
        for h in constants.hotels:
            if context.stock[h] < 25:
                bonus_winners = infos.find_holders(context, h)
                if bonus_winners == [[],[]]: #no shareholders at all
                    print h + " has no shareholders!  Tragic!"
                elif len(bonus_winners[0]) > 1: #tie for Majority
                    print h + ": Players " + str(bonus_winners[0]) + "tie for majority shareholder with " + str(context.player[bonus_winners[0][0]]['stock'][h]) + " shares each."
                elif len(bonus_winners[0]) == 1 and bonus_winners[1] == []: #Only one shareholder
                    print h + ": Player " + str(bonus_winners[0][0]) + " is the only shareholder, with " + str(context.player[bonus_winners[0][0]]['stock'][h]) + " shares."
                else: # One maj shareholder, one or more mins
                    print h + ": Player " + str(bonus_winners[0][0]) + " is the Majority shareholder, with " + str(context.player[bonus_winners[0][0]]['stock'][h]) + " shares."
                    if len(bonus_winners[1]) == 1: # single winning minority holder
                        print "   and Player " + str(bonus_winners[1][0]) + " is the highest minority shareholder with " + str(context.player[bonus_winners[1][0]]['stock'][h]) + " shares."
                    else: #tie for min bonus
                        print "   and Players " + str(bonus_winners[1]) + " tie for minority shareholder with " + str(context.player[bonus_winners[1][0]]['stock'][h]) + " shares each."