fgColors = {
    "default": "\033[39m",
    "black": "\033[30m",
    "darkRed": "\033[31m",
    "darkGreen": "\033[32m",
    'yellow': '\033[43m',
    "darkBlue": "\033[34m",
    "darkMagenta": "\033[35m",
    "darkCyan": "\033[36m",
    "lightGray": "\033[37m",
    "darkGray": "\033[90m",
    "red": "\033[91m",
    "green": "\033[92m",
    "orange": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
}

bgColors = {
    "default": "\033[49m",
    "black": "\033[40m",
    "darkRed": "\033[41m",
    "darkGreen": "\033[42m",
    'yellow': '\033[43m',
    "darkBlue": "\033[44m",
    "darkMagenta": "\033[45m",
    "darkCyan": "\033[46m",
    "lightGray": "\033[47m",
    "darkGray": "\033[100m",
    "red": "\033[101m",
    "green": "\033[102m",
    "orange": "\033[103m",
    "blue": "\033[104m",
    "magenta": "\033[105m",
    "cyan": "\033[106m",
    "white": "\033[107m",
}


class ColoredText:
    def __init__(self):
        pass
    
    def applyBg(self, text: str, color: str) -> str:
        if color not in bgColors:
            raise Exception(f"Invalid color: {color}")
        return bgColors[color] + text + bgColors["default"]
    
    def applyFg(self, text: str, color: str) -> str:
        if color not in fgColors:
            raise Exception(f"Invalid color: {color}")
        return fgColors[color] + text + fgColors["default"]
    
    def applyBgFg(self, text: str, bgColor: str, fgColor: str) -> str:
        if bgColor not in bgColors:
            raise Exception(f"Invalid color: {bgColor}")
        if fgColor not in fgColors:
            raise Exception(f"Invalid color: {fgColor}")
        return self.applyFg(self.applyBg(text, bgColor), fgColor)


def main():
    ct = ColoredText()
    word = "throw".upper()
    
    # output = f"""
    # {ct.applyBg("┌───", 'blue')}┬───┬───┬───┬───┐
    # │ {ct.applyBg(word[0], 'blue')} │ {word[1]} │ {word[2]} │ {word[3]} │ {word[4]} │
    # └─── ┴───┴───┴───┴───┘
    # """
    
    # top = "┌───┐┌───┐┌───┐┌───┐┌───┐"
    # middle = "│{} _ {}││{} _ {}││{} _ {}││{} _ {}││{} _ {}│"
    # bottom = "└───┘└───┘└───┘└───┘└───┘"
    
    output = f"""
    {ct.applyBg("┌───┐", 'blue')}{ct.applyBg("┌───┐", 'green')}{ct.applyBg("┌───┐", 'red')}{ct.applyBg("┌───┐", 'yellow')}{ct.applyBg("┌───┐", 'magenta')}
    {ct.applyBg("│ _ │", 'blue')}{ct.applyBg("│ _ │", 'green')}{ct.applyBg("│ _ │", 'red')}{ct.applyBg("│ _ │", 'yellow')}{ct.applyBg("│ _ │", 'magenta')}
    {ct.applyBg("└───┘", 'blue')}{ct.applyBg("└───┘", 'green')}{ct.applyBg("└───┘", 'red')}{ct.applyBg("└───┘", 'yellow')}{ct.applyBg("└───┘", 'magenta')}
    """
    print(output)
    
    # print("\u2500")
    
#     box = f"""
# ┌───┐
# │ {word[0]} │
# └───┘
#     """

    # # Split the box into lines
    # lines = box.strip().split('\n')
    # # for i in lines:
    # #     print(i)

    # # Concatenate each line with two more boxes
    # three_boxes = '\n'.join([line + '' + line + '' + line for line in lines])

    # # Print the result
    # print(three_boxes)

        
    
    # # print(output)
    # output = f"""
    # {ct.applyBg("┌───┐", 'blue')}┌───┬───┬───┬───┐
    # │ {ct.applyBg(word[0], 'blue')} │ {word[1]} │ {word[2]} │ {word[3]} │ {word[4]} │
    # └───┘ └───┴───┴───┴───┘
    # """
    
    # print(output)

if __name__ == "__main__":
    main()