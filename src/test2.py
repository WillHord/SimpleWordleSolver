import curses

# ColoredText might not be necessary with curses, as curses has its own color handling
# If you still want to use it, it should be adapted to use curses color pairs

class TerminalController:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup()
        self.current_box_index = 0  # Starting box index

    def setup(self):
        # Initialize curses settings
        curses.curs_set(0)  # Hide cursor
        curses.start_color()  # Start color functionality
        curses.use_default_colors()  # Use terminal's default colors

        curses.cbreak()  # React to keys instantly, without requiring the Enter key
        self.stdscr.keypad(True) 

        # Define color pairs if needed
        # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)  # Example
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # First color pair
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)

    def applyBg(self, text: str, color_pair_id: int) -> str:
        color_attr = curses.color_pair(color_pair_id)
        return f'{curses.attron(color_attr)}{text}{curses.attroff(color_attr)}'

    def _getBox(self, color, letter):        
        return f"{self.applyBg('┌───┐', color)}\n{self.applyBg(f'│ {letter} │', color)}\n{self.applyBg('└───┘', color)}"

    def getBoxTemplate(self):
        testBoxes = [self._getBox(1, '_') for _ in range(5)]
        boxes = [box.split('\n') for box in testBoxes]

        return "\n".join("".join(parts) for parts in zip(*boxes))
    
    def print_box(self, letter, color_pair_id, x, y):
        box_lines = ['┌───┐', f'│ {letter} │', '└───┘']
        self.stdscr.attron(curses.color_pair(color_pair_id))
        for i, line in enumerate(box_lines):
            self.stdscr.addstr(y + i, x, line)
        self.stdscr.attroff(curses.color_pair(color_pair_id))


    def selectBox(self, index):
        arrow = "↑"
        spaces = " " * ((index * 5) + 2)
        return "\n" + spaces + arrow + "\n"

    def askGuess(self):
        # Adapt to use curses window methods
        self.stdscr.addstr("\nWhat is your name? ")
        self.stdscr.refresh()
        return self.stdscr.getstr().decode()

    def print(self):
        self.stdscr.clear()
        self.stdscr.addstr(self.getBoxTemplate())
        self.stdscr.addstr(self.selectBox(self.current_box_index))
        self.stdscr.refresh()

    def main_loop(self):
        # while True:
        #     self.print()
        #     key = self.stdscr.getch()
        #     if key == curses.KEY_RIGHT:
        #         self.current_box_index = min(4, self.current_box_index + 1)
        #     elif key == curses.KEY_LEFT:
        #         self.current_box_index = max(0, self.current_box_index - 1)
        #     elif key == ord('\n'):  # Enter key
        #         self.askGuess()
        #     elif key == ord('q'):  # Quit on 'q'
        #         break

if __name__ == "__main__":
    def main(stdscr):
        tc = TerminalController(stdscr)
        tc.main_loop()

    curses.wrapper(main)
