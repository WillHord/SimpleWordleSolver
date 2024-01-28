import pytest
from src.trie import Trie

def test_insert():
    trie = Trie()
    trie.insert("apple")
    assert trie.root.children['a'].children['p'].children['p'].children['l'].children['e'].isEnd == True

def test_atPositions():
    trie = Trie()
    trie.insert("apple")
    trie.insert("banana")
    trie.insert("cherry")
    included = {'a': [0], 'e': [4]}
    excluded = {'b'}
    assert trie.atPositions("a___e", included, excluded) == ['apple']

def test_strToIndex():
    trie = Trie()
    assert trie.strToIndex('a') == 0
    assert trie.strToIndex('b') == 1
    assert trie.strToIndex('z') == 25

if __name__ == "__main__":
    pytest.main()