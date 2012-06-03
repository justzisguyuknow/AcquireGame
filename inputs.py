import constants
import infos


def numplayers_ask(context):
    """Asks for number of players, returns input"""
    response = 0
    while response == 0:
        response = int(raw_input("How many players? (2-6):"))
        if response in [2,3,4,5,6]:
            return response
        else: 
            print "Bad Input"
            response = 0

def buystock_ask_input(context):
    '''Prompts for Y/N input whether current player wants to buy stock'''
    response = 0
    while response == 0:
        response = raw_input("Player " + str(context['cp']) + ", Would you like to buy stock this turn? (Y/N):")
        if response in ['Y', 'Yes', "y", 'yes']:
            return "Y"
        elif response in ['N', 'No', "n", 'no']:
            return "N"
        else:
            print "Bad Input"
            response = 0

def tile_input(context):
    tiletoplay = 0
    while tiletoplay == 0:   
        tiletoplay = raw_input("Which tile would you like to play?")       
        if tiletoplay not in context['player'][context['cp']]["tilerack"]:
            print "Bad Input"
            tiletoplay = 0
            continue
        elif infos.unusable(context, tiletoplay):
            print "playing that tile would create a new chain, but all hotels are already on the board!"
            tiletoplay = 0
            continue
        elif tiletoplay in context['player'][context['cp']]['tilerack']:
            return tiletoplay
        else: 
            raise NameError("Tile Input Not Caught!")

def newchain_input(context):
    new = 0
    while new == 0:
        new = raw_input("Which hotel would you like to found?")
        if new not in infos.free_hotels(context):
            print "Bad Input."
            new = 0
    return new

def merge_dir_input(context, contenders):
    print str(contenders) + " are the options to dominate this merger."
    dom = 0
    while dom == 0:
        dom = raw_input("Which hotel do you choose to dominate the merger?")
        if dom not in contenders:
            print "Not an option"
            dom = 0
        else: return dom

def sell_stock_ask_input(context, p, chain):
    "Tells player how many shares of the chain they have and asks if they want to sell any"
    print "Player "  + str(p) + ", you have " + str(context['player'][p]['stock'][chain]) + " shares of " + chain + " stock."
    sell = 0
    while sell == 0:
        sell = raw_input("Do you want to sell any stock for $" + str(infos.price(context, chain)) + " per share? (Y/N):")
        if sell in ["Y", 'y', 'Yes', "yes"]:
            return 'Y'
            break
        elif sell in ['n', 'N', 'no', 'No']:
            return 'N'
            break
        else:
            print "Bad Input."
            sell = 0

def sell_stock_shares_input(context, p, chain):
    print "How many shares would you like to sell?"
    sell_shares = -1
    while sell_shares == -1:
        sell_shares = int(raw_input("Enter a number:"))
        if sell_shares > context['player'][p]['stock'][chain]:
            print "You don't have that many shares!"
            sell_shares = -1
        else: return sell_shares          

def done_input():
    ans = 0
    while ans == 0:   
        ans = raw_input("Would you like to make additional purcahses?")
        if ans in ["Y", 'y', 'Yes', "yes"]:
            return 'y'
            break
        elif ans in ['n', 'N', 'no', 'No']:
            return 'N'
            break
        else:
            print "Bad Input."
            ans = 0
            