import turnaction
import pickle

def picklesave(context, name): #name must be a string 
    '''saves the game context in a file named name'''
    gamefile = open(name, 'w')
    pickle.dump(context, gamefile)
    gamefile.close()

def pickleload(context, name): #name must be a string
    '''loads the game file named to context'''
    gamefile = open(name, 'r')
    context = pickle.load(gamefile)
    gamefile.close()


##OLD SAVE AND LOAD FUNCTIONS:

# def savegame(context):	
#     game = open("savedgame.py", 'w')
#     now = datetime.datetime.now()
#     game.write("### Game" + str(n))
#     game.write("/n")
#     game.write("### Saved on " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " at " + str(now.hour) + ":" + str(now.minute) + "." + str(now.second))
#     game.write("/n")
#     game.write("context = " + str(context))
#     game.close()
	
# def loadgame(context):
#     import savedgame
#     context = savedgame.context
#     turnaction.rungame(context)