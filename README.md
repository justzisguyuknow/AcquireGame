AcquireGame
===========

This is a work-in-progress text-based version of the classic board game Acquire.

It's not very useful now, because it only works on one screen.

I am planning to add an actual GUI and get it running on an online server so people can play remotely.

acquiremain.py is the core of the program, use acquiremain.start(acquiremain.context) to start a game and acquiremain.run(acquiremain.context) to continue an ongoing game.


TO DO:
Make pickle savegame functions work
Fix problem where adjacent filled tiles from initial draw don't become chain together
