# SSBM-Trainer
A Melee Training Pack with reactive AI using Smashbot's libmelee python library
BY Colin Sullivan - Playittillyouwin

CODE TLDR:

SSBMTrainer.py - Runner class that starts the GUI and takes a user button click to select which
scenario file to initialize. Also initializes console and controllers and does while(True) frame
by frame. Each loop uses the .act() method in the situation classes to decide action.

Situation classes - Is initialized in the runner class, with access to the controller and console.
Defines a .act() method which takes a gamestate object for the current frame, and based on its 
attributes, decides it's own course of action and executes it.

TechSkill.py - A class that defines methods, which when called frame by frame will perform a specific
tech. Each method both checks if it can act, and acts, so if it should act is left to the caller. Import 
in situation classes and call the methods with the character specific attributes 
