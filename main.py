"""
Main file of the project. 
This script works as programm launcher, imports and runs game instance.

Author: WK-K
"""

# Project modules
import Classes.Game as game
# Standard modules
import os

# MAIN
if __name__ == "__main__":
    # Get current directory for easy relative paths
    scripts_directory: str = os.path.dirname(os.path.abspath(__file__))
    # Run the program
    game.Game(scripts_directory)



