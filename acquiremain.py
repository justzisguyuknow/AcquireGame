import datetime
import random
import sys
import pickle

import constants
import stateclass
import turnaction
import dataction
import infos
import prints
import inputs

cont = stateclass.State()

def start():
    '''Resets context to game opening, and starts a new game'''
    turnaction.startgame(cont)

def run():
    '''runs the game'''
    global cont
    turnaction.rungame(cont)

def save(name): #name must be a string 
    cont.statesave(name)

def load(name): #name must be a string
    '''unpickles context from named file'''
    global cont
    gamefile = open("psg"+ name, 'r')
    cont = pickle.load(gamefile)
    gamefile.close()
    
    turnaction.rungame(cont)