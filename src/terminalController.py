import curses
import time

class TerminalController:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.letters = {
            0: {"letter": "_", "color": 0},
            1: {"letter": "_", "color": 0},
            2: {"letter": "_", "color": 0},
            3: {"letter": "_", "color": 0},
            4: {"letter": "_", "color": 0},
        }
        self.setup()

    def setup(self):
        curses.start_color()
        curses.use_default_colors()
        
        # Initialize color pairs for each box
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        
        if curses.can_change_color():
            curses.init_color(8, 784,713,325) # Yellow
            curses.init_color(9, 423,662,396) # Green
            
            curses.init_pair(2, curses.COLOR_WHITE, 8)
            curses.init_pair(3, curses.COLOR_WHITE, 9)
        else:
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

    def print_box(self, letter, color_pair_id, x, y):
        box_lines = ['┌───┐', f'│ {letter} │', '└───┘']
        self.stdscr.attron(curses.color_pair(color_pair_id))
        for i, line in enumerate(box_lines):
            self.stdscr.addstr(y + i, x, line)
        self.stdscr.attroff(curses.color_pair(color_pair_id))

    def print_all_boxes(self):
        box_width = 5
        
        for i, letter in self.letters.items():
            self.print_box(letter["letter"], letter["color"], i * box_width, 0)  # 5 is the y-coordinate
        self.stdscr.addstr(3, 0, "\n")

    def _selectBox(self, index):
        arrow = "↑"
        spaces = " " * ((index * 5) + 2)
        return spaces + arrow + "\n"
    
    def selectCorrect(self, index):
        # Set letter to correct color if not already correct
        if self.letters[index]["color"] == 3:
            self.letters[index]["color"] = 0
        else:
            self.letters[index]["color"] = 3

    def selectWrongPos(self, index):
        if self.letters[index]["color"] == 2:
            self.letters[index]["color"] = 0
        else:
            self.letters[index]["color"] = 2
    
    def selectBox(self, func, msg = None):
        current_box_index = 0
        while True:
            self.stdscr.clear()
            self.print_all_boxes()
            self.stdscr.addstr(3, 0, self._selectBox(current_box_index))
            if msg: self.stdscr.addstr(4, 0, msg)
            self.stdscr.addstr(5, 0, "Select letters using arrow keys and enter\nPress q to quit")
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.stdscr.addstr(3, 0, str(key))
            if key == curses.KEY_LEFT:
                current_box_index = max(0, current_box_index - 1)
            elif key == curses.KEY_RIGHT:
                current_box_index = min(4, current_box_index + 1)
            elif key == ord('\n'):
                # TODO: Make array of initial colors and reset to that instead of 0
                func(current_box_index)
            elif key == ord('q'):
                return -1
            
    def askGuess(self):
        # Get user input
        question = "What was your guess? "
        answer = ""
        while True:
            self.stdscr.clear()
            self.print_all_boxes()
            self.stdscr.addstr(3, 0, question + answer)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key == ord('\n'):
                return answer
            elif key == curses.KEY_BACKSPACE or key == 127 or key == ord('\b'):
                answer = answer[:-1]
            elif key >= 32 and key <= 126:  # ASCII printable characters range
                answer += chr(key)
            time.sleep(0.1)
    
    def help(self):
        # Print help menu to screen
        while True:
            self.stdscr.clear()
            # self.print_all_boxes()
            self.stdscr.addstr(3, 0, "Help menu")
            
            key = self.stdscr.getch()
            if key == ord('q'):
                return -1
            else:
                return 0
        

    def main_loop(self):
        while True:
            self.stdscr.clear()
            self.print_all_boxes()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            # Select box
            if key == ord('\n'):
                self.askGuess()
                self.selectBox(self.selectCorrect, msg="Select correct letters")
                self.selectBox(self.selectWrongPos, msg="Select letters in the wrong position")
                # self.selectBox()
            if key == ord('q'):  # Quit on 'q'
                break

if __name__ == "__main__":
    def main(stdscr):
        tc = TerminalController(stdscr)
        tc.main_loop()
    curses.wrapper(main)
