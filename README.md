# SimpleWordleSolver

SimpleWordleSolver is an easy way to cheat in Wordle

## Getting Started

### Prerequisites

Python 3

### Installing

To install this program run the following commands:

```
git clone git@github.com:WillHord/SimpleWordleSolver.git

pip install english_words
```

Once you have made the program you can then run it using the command

```
python main.py
```

The program will give you a word to test, then it will ask if the word was correct. There are a few options you can respond:
```
y: The word was correct and the game is over
n: The word was incorrect
h: Help (Shows commands)
r: Reroll word from possible words
q: Quit program
```

If the word was not correct it will ask you which letters were correct, please input them as a single string. It will then ask if they were in the correct position answer 'y' if they are in the correct spot. This process will repeat until you quit the program or input that the word was correct.


## Built With

* [Python](https://www.python.org/) - Language Used

## Authors

* **Will Hord** - [Willhord](https://github.com/WillHord)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
