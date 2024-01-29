# SimpleWordleSolver

An an easy way to cheat in Wordle

## Description
SimpleWordleSolver is a Python-based program designed to help player's cheat in the game [Wordle](https://www.nytimes.com/games/wordle/index.html). It utilizes a Trie data structure and the Curses library to effeciently search for the optimal solution and run completely in the Terminal while still having an appealing interface.

## Getting Started

### Prerequisites

- [Python 3.8](https://www.python.org/) or higher

### Installing

1. Clone the repo
```
git clone git@github.com:WillHord/SimpleWordleSolver.git
```
2. Install required libraries
```
pip install -r requirements.txt
```

### Executing program
Once you have made the program you can then run it using the command

```
python wordleSolver.py
```
The program will start with a welcome screen where you can either type `start` to start solving a wordle puzzle or `help` to view the help menu

```
Commands:
    start (s):          Start a new game
    restart (r):        Restart the current game
    help (h):           Show this help menu
    quit (q, exit):     Quit the game

Gameplay:
    Guess a 5 letter word and then select the letters that are correct or in the wrong position.
    You will then recieve the 10 best guesses for the next round.
    Continue until you find the word or run out of guesses.
```

### Testing
If you want to test and verify the program is working as intended run the command:
```
python -m coverage run -m pytest tests
```

## Built With

* [Python](https://www.python.org/) - Language Used

## Author

* **Will Hord** - [Willhord](https://github.com/WillHord)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
