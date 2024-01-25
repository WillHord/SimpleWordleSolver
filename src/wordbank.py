from typing import Dict, Set, List
from collections import Counter

from trie import Trie

class WordBank():
    def __init__(self) -> None:
        self.trie = Trie()
        self.counter = Counter()
        
    def addWord(self, word: str) -> None:
        self.trie.insert(word)
        
    def readWords(self, path: str) -> None:
        with open(path, 'r') as f:
            for line in f:
                self.addWord(line.strip())
                self.counter.update(set(line.strip()))
                
    def getPossibleWords(self, word: str, included: Dict[str, List[int]], excluded: Set[str]) -> List[str]:
        return self.trie.atPositions(word, included, excluded)
    
    def getMostCommon(self):
        return self.counter.most_common(1)[0][0]
    
    def getBestGuess(self):
        pass

if __name__ == "__main__":
    wb = WordBank()
    wb.readWords("wordle-words.txt")
    
    # wb.trie.printRoot()
    print(wb.getMostCommon())
    print(wb.counter)
    
    # print(wb.getPossibleWords("_o_ar", {"r":[0,2],"o":[3], "a":[]}, set([i for i in "thwgebl"])))