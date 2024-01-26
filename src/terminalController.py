import curses
import time
from typing import Dict, Set, List


def waitForInput(func):
    def wrapper(*args, **kwargs):
        result = None
        while result is None:
            result = func(*args, **kwargs)
        return result
    return wrapper


class TerminalController:
    def __init__(self, stdscr) -> None:
        self.nextLine = 0
        self.stdscr = stdscr
        self.box_index = 0
        self.temp_int, self.temp_str, self.temp_list = 0, "", []
        self.gameround = 0
        self.board = None

        self.setup()

    def init_board(self):
        self.board = [{i: {"letter": "_", "color": 0}
                       for i in range(5)} for _ in range(6)]

    def setup(self):
        self.initialize_colors()
        self.init_board()

    def initialize_colors(self):
        curses.start_color()
        curses.use_default_colors()

        # Initialize color pairs for each box
        curses.init_pair(1, curses.COLOR_WHITE, -1)

        if curses.can_change_color():
            curses.init_color(8, 784, 713, 325)  # Yellow
            curses.init_color(9, 423, 662, 396)  # Green

            curses.init_pair(2, curses.COLOR_WHITE, 8)
            curses.init_pair(3, curses.COLOR_WHITE, 9)
        else:
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    def print(self, msg: str) -> None:
        self._print(self.nextLine, 0, msg)

    def _print(self, y, x, msg):
        self.stdscr.addstr(y, x, msg)
        # Update nextLine to be the next line after the last line printed (accounting for newlines)
        self.nextLine = y + msg.count('\n') + 1
        self.stdscr.refresh()

    def clear(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.nextLine = 0

    def handle_key_input(self):
        key = self.stdscr.getch()
        if key == curses.KEY_BACKSPACE or key == 127 or key == ord('\b'):
            return 'BACKSPACE', key
        elif key >= 32 and key <= 126:
            return 'CHAR', chr(key)
        return 'OTHER', key

    def print_box(self, letter, color_pair_id, x, y):
        box_lines = ['┌───┐', f'│ {letter} │', '└───┘']
        self.stdscr.attron(curses.color_pair(color_pair_id))
        for i, line in enumerate(box_lines):
            self._print(y + i, x, line)
        self.stdscr.attroff(curses.color_pair(color_pair_id))

    def print_all_boxes(self):
        box_width = 5
        box_height = 3  # Height of each box (including borders)
        for round in range(1, self.gameround + 1):
            for i, letter in self.board[round].items():
                x = i * box_width
                y = (round - 1) * box_height
                self.print_box(letter["letter"], letter["color"], x, y)

    def calculate_arrow_position(self, index):
        return " " * ((index * 5) + 2) + "↑\n"

    def selectCorrect(self, index):
        # Set letter to correct color if not already correct
        if self.board[self.gameround][index]["color"] == 3:
            self.board[self.gameround][index]["color"] = 0
        else:
            self.board[self.gameround][index]["color"] = 3

    def selectWrongPos(self, index):
        if self.board[self.gameround][index]["color"] == 2:
            self.board[self.gameround][index]["color"] = 0
        else:
            self.board[self.gameround][index]["color"] = 2

    def addWord(self, word):
        # Add word to board
        for i, letter in enumerate(word):
            self.board[self.gameround][i]["letter"] = letter
        # self.gameround += 1

    @waitForInput
    def selectBox(self, func, msg=None):
        self.clear()
        self.print_all_boxes()
        self.print(self.calculate_arrow_position(self.box_index))
        if msg:
            self.print(msg)
        self.print("Select letters using arrow keys and enter\nPress q to quit")
        _, key = self.handle_key_input()
        if key == curses.KEY_LEFT:
            self.box_index = max(0, self.box_index - 1)
        elif key == curses.KEY_RIGHT:
            self.box_index = min(4, self.box_index + 1)
        elif key == ord('\n'):
            # TODO: Make array of initial colors and reset to that instead of 0
            func(self.box_index)
        elif key == 'q':
            self.box_index = 0
            return -1

    @waitForInput
    def handle_input(self, question):
        # Get user input
        self.clear()
        self.print_all_boxes()
        self.print(question + self.temp_str)
        type_, key = self.handle_key_input()
        if key == ord('\n'):
            ans = self.temp_str[:]
            self.temp_str = ""
            return ans
        elif type_ == 'BACKSPACE':
            self.temp_str = self.temp_str[:-1]
        elif type_ == 'CHAR':
            self.temp_str += str(key)

    @waitForInput
    def handle_select(self, question, options):
        # Get user input from list of options
        self.clear()
        self.print_all_boxes()
        self.print(question)
        for i, option in enumerate(options):
            if i == self.temp_int:
                self.print(f"→ {option}")
                # self.stdscr.addstr(4 + i, 0, f"→ {option}")
            else:
                # self.stdscr.addstr(4 + i, 0, f"  {option}")
                self.print(f"  {option}")
        _, key = self.handle_key_input()
        if key == ord('\n'):
            ans = self.temp_int
            self.temp_int = 0
            return ans
        elif key == curses.KEY_UP:
            self.temp_int = max(0, self.temp_int - 1)
        elif key == curses.KEY_DOWN:
            self.temp_int = min(len(options) - 1, self.temp_int + 1)
        elif key == ord('q'):
            self.temp_int = 0
            return -1

    @waitForInput
    def handle_multi_select(self, question, options):
        self.clear()
        self.print_all_boxes()
        self.print(question)
        if "Done" not in options:
            options.append("Done")
        for i, option in enumerate(options):
            if i in self.temp_list:
                # Set background color to green
                self.stdscr.attron(curses.color_pair(3))
            if i == self.temp_int:
                self.print(f"→ {option}")
            else:
                self.print(f"  {option}")
            if i in self.temp_list:
                self.stdscr.attroff(curses.color_pair(3))
        _, key = self.handle_key_input()
        if key == ord('\n'):
            if self.temp_int == len(options) -1:
                # Done
                ans = self.temp_list
                self.temp_list = []
                self.temp_int = 0
                return ans
            # Add to temp_list if not already in it
            if self.temp_int not in self.temp_list:
                self.temp_list.append(self.temp_int)
            else:
                self.temp_list.remove(self.temp_int)
        elif key == curses.KEY_UP:
            self.temp_int = max(0, self.temp_int - 1)
        elif key == curses.KEY_DOWN:
            self.temp_int = min(len(options) - 1, self.temp_int + 1)
        elif key == ord('q'):
            self.temp_int = 0
            self.temp_list = []
            return -1
        
    def askGuess(self):
        # TODO: Write Guess in boxes
        # Get user input
        question = "What was your guess? "
        guess = self.handle_input(question)
        while not guess or len(guess) != 5:
            question = ("Woops! Your guess must be 5 letters long, "
                        f"your guess was only {str(len(guess) if guess else 0)} long\nTry again:")
            guess = self.handle_input(question)
        self.addWord(guess.upper())
        return guess

    @waitForInput
    def help(self):
        # self.stdscr.clear()
        self.clear()
        self.print("Help Menu:")
        self.print("""
    Commands:
        start (s):          Start a new game
        restart (r):        Restart the current game
        help (h):           Show this help menu
        quit (q, exit):     Quit the game
    
    Gameplay:
        Guess a 5 letter word and then select the letters that are correct or in the wrong position.
        You will then recieve the 10 best guesses for the next round.
        Continue until you find the word or run out of guesses.
""")
        if self.handle_key_input():
            return True

    def check_win(self):
        # Check if all letters are correct
        for letter in self.board[self.gameround].values():
            if letter["color"] != 3:
                return False
        return True
    
    @waitForInput
    def run_game(self):
        self.clear()
        self.print_all_boxes()
        self.askGuess()
        ans = self.handle_multi_select("Were any letters correct or in the wrong position?", ["Correct", "Wrong position" ])
        if 0 in ans:
            self.selectBox(self.selectCorrect, msg="Select correct letters")
        if 1 in ans:
            self.selectBox(self.selectWrongPos, msg="Select letters in the wrong position")
        
        if self.gameround == 6 and not self.check_win():
            self.print("Oh no we couldn't find the word!")
            self.print("Better luck next time!")
            return -1
        self.gameround += 1
    
    def check_commands(self, command):
        # List of standard commands to check against
        if command in ['start', 's', 'restart', 'r']:
            self.reset()
            self.gameround = 1
            self.run_game()
            return False
        elif command in ['help', 'h']:
            self.help()
            return False
        elif command in ['quit', 'q', 'exit']:  # Quit on 'q'
            return True
    
    @waitForInput
    def main_loop(self):
        self.clear()
        command = self.handle_input("Enter a command ('help' for more info): ").lower()
        return self.check_commands(command)

    def reset(self):
        self.clear()
        self.setup()


if __name__ == "__main__":
    def main(stdscr):
        tc = TerminalController(stdscr)
        tc.main_loop()
    curses.wrapper(main)
