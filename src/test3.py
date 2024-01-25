import curses
import time

class TerminalController:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()

    def setup(self):
        curses.start_color()
        # Use terminal's default colors
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
        letters = ["_", "_", "_", "_", "_"]
        for i, letter in enumerate(letters):
            self.print_box(letter, 0, i * box_width, 5)  # 5 is the y-coordinate

    def _selectBox(self, index):
        arrow = "↑"
        spaces = " " * ((index * 5) + 2)
        return "\n" + spaces + arrow + "\n"
    
    def selectBox(self):
        current_box_index = 0
        while True:
            self.stdscr.clear()
            # self.stdscr.addstr(self.getBoxTemplate())
            self.print_all_boxes()
            self.stdscr.addstr(self._selectBox(current_box_index))
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.stdscr.addstr(0, 0, str(key))
            if key == curses.KEY_LEFT:
                current_box_index = max(0, current_box_index - 1)
            elif key == curses.KEY_RIGHT:
                current_box_index = min(4, current_box_index + 1)
            elif key == ord('\n'):
                return current_box_index
            elif key == ord('q'):
                return -1
        

    def main_loop(self):
        while True:
            self.stdscr.clear()
            self.print_all_boxes()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            # Select box
            if key == ord('\n'):
                self.selectBox()
            if key == ord('q'):  # Quit on 'q'
                break

if __name__ == "__main__":
    def main(stdscr):
        tc = TerminalController(stdscr)
        tc.main_loop()
    curses.wrapper(main)
