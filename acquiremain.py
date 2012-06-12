import datetime
import random
import sys
import pickle

import constants
import cxt
import turnaction
import dataction
import infos
import prints
import inputs

cont = cxt.CXT

def start():
    '''Resets context to game opening, and starts a new game'''
    turnaction.startgame(cont)

def run():
    '''runs the game'''
    global cont
    turnaction.rungame(cont)

def psave(context, name): #name must be a string 
    '''pickles the game context in named file'''
    gamefile = open("psg"+name, 'w')
    pickle.dump(context, gamefile)
    gamefile.close()

def pload(name): #name must be a string
    global cont
    '''unpickles context from named file'''
    gamefile = open("psg"+name, 'r')
    cont = pickle.load(gamefile)
    gamefile.close()
    turnaction.rungame(cont)