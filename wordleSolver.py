import curses
import argparse
import os

from src import wordbank, terminalcontroller as tc

def main(stdscr) -> None:
    # Set up args
    parser = argparse.ArgumentParser(description="Wordle Solver")

    args = parser.parse_args()
    
    wordBank = wordbank.WordBank()
    path = os.path.join(os.path.dirname(__file__), "src/wordle-words.txt")
    wordBank.readWords(path)
    terminalController = tc.TerminalController(stdscr, wordBank)
    
    terminalController.main_loop()

if __name__ == "__main__":
    curses.wrapper(main)