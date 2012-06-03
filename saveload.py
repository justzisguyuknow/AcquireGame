import turnaction

def savegame(context):	
    game = open("savedgame.py", 'w')
    now = datetime.datetime.now()
    game.write("### Game" + str(n))
    game.write("/n")
    game.write("### Saved on " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " at " + str(now.hour) + ":" + str(now.minute) + "." + str(now.second))
    game.write("/n")
    game.write("context = " + str(context))
    game.close()
	
def loadgame(context):
    import savedgame
    context = savedgame.context
    
    turnaction.rungame(context)
