import datetime
import random
import sys
import pickle

import constants
import context
import turnaction
import dataction
import infos
import prints
import inputs

context = context.CXT

def start(context):
    '''Starts the game'''
    turnaction.startgame(context)

def run(context):
    '''runs the game'''
    turnaction.rungame(context)

def psave(context, name): #name must be a string 
    '''pickles the game context in named file'''
    gamefile = open(name, 'w')
    pickle.dump(context, gamefile)
    gamefile.close()

def pload(name): #name must be a string
    global context
    '''unpickles context from named file'''
    gamefile = open(name, 'r')
    context = pickle.load(gamefile)
    gamefile.close()
    turnaction.rungame(context)

def save(name): #name must be a string!
	'''shortcut for calling saveload.picklesave(context, name)'''
	psave(context, name)

def load(name): #name must be a string!
	'''shortcut for calling saveload.pickleload(context, name)'''
	pload(name)
