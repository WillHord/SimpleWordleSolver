import pytest
from collections import Counter
import os

from src.wordbank import WordBank
from src.trie import Trie


test_path = os.path.join(os.path.dirname(__file__), "dummy.txt")


@pytest.fixture
def wordbank_instance():
    # Generate dummy file for testing
    testing_words = ["hello", "world", "apple", "banana", "cherry"]
    with open(test_path, 'w') as f:
        for word in testing_words:
            f.write(word + "\n")
    wordbank = WordBank()
    yield wordbank
    # Cleanup
    # If dummy file was created, delete it
    if os.path.exists(test_path):
        os.remove(test_path)


def test_init_wordbank():
    # Test initialization
    wordbank = WordBank()
    assert isinstance(wordbank.trie, Trie)
    assert isinstance(wordbank.counter, Counter)
    assert wordbank.included == {}
    assert wordbank.excluded == set()
    assert wordbank.word == "_____"


def test_add_word(wordbank_instance):
    # Test adding a word
    wordbank_instance.addWord("test")
    assert wordbank_instance.trie.included("test")
    assert not wordbank_instance.trie.included("testing")


def test_read_words(wordbank_instance):
    # Test reading words from a file
    wordbank_instance.readWords(str(test_path))
    assert wordbank_instance.trie.included("hello")
    assert wordbank_instance.trie.included("world")
    assert wordbank_instance.trie.included("apple")
    assert wordbank_instance.trie.included("banana")
    assert wordbank_instance.trie.included("cherry")
    assert not wordbank_instance.trie.included("testing")


def test_get_possible_words(wordbank_instance):
    # Test getting possible words
    wordbank_instance.readWords(str(test_path))
    wordbank_instance.word = "a___e"
    wordbank_instance.included = {'a': [0], 'e': [4]}
    wordbank_instance.excluded = {'b'}
    possible_words = wordbank_instance.getPossibleWords(
        wordbank_instance.word, wordbank_instance.included, wordbank_instance.excluded)
    assert possible_words == ['apple']
    possible_words = wordbank_instance.getPossibleWords("_____", {}, set())
    assert possible_words == ['hello', 'world', 'apple']
    possible_words = wordbank_instance.getPossibleWords("______", {}, set())
    assert possible_words == ['banana', 'cherry']


def test_rank_words(wordbank_instance):
    # Test ranking words
    words = ["hello", "world"]
    count = Counter("helloworld")
    ranked = wordbank_instance.rankWords(words, count.most_common(26))
    assert ranked == {22: ['hello'], 19: ['world']}


def test_get_best_guess(wordbank_instance):
    # Test getting the best guess
    # Test best guess with word ___l_
    wordbank_instance.readWords(str(test_path))
    wordbank_instance.word = "___l_"
    wordbank_instance.included = {}
    wordbank_instance.excluded = set()
    best_guess = wordbank_instance.getBestGuess()
    assert best_guess == ['hello', 'world', 'apple']

    # Test no possible words
    wordbank_instance.word = "_____"
    wordbank_instance.included = {}
    wordbank_instance.excluded = set("abcdefghijklmnopqrstuvwxyz")
    best_guess = wordbank_instance.getBestGuess()
    assert best_guess == ["No possible words"]


def test_add_guess(wordbank_instance):
    # Test adding a guess
    wordbank_instance.addGuess("apple", [0, 2], [4])
    assert wordbank_instance.word == "a_p__"
    assert wordbank_instance.included == {'a': [], 'p': [], 'e': [4]}
    assert wordbank_instance.excluded == {'l', 'p'}
