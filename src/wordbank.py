from typing import Dict, Set, List
from collections import Counter
import os

class WordBank:
    def __init__(self) -> None:
        self.trie = Trie()
        self.counter = Counter()
        self.included = {}
        self.excluded = set()
        self.word = "_____"
        
    def addWord(self, word: str) -> None:
        self.trie.insert(word)
        
    def readWords(self, path: str) -> None:
        with open(path, 'r') as f:
            for line in f:
                self.addWord(line.strip())
                self.counter.update(set(line.strip()))
                
    def getPossibleWords(self, word: str, included: Dict[str, List[int]], excluded: Set[str]) -> List[str]:
        return self.trie.atPositions(word, included, excluded)
    
    def rankWords(self, words: List[str], count: List[tuple]) -> Dict[int, List[str]]:
        letter_rank = {}
        pos = 0
        for val in range(len(count) - 1, -1, -1):
            letter_rank[count[pos][0]] = val + 1
            pos += 1
        ranking = {}
        for word in words:
            rank = 0
            _word = set(word)
            for letter in _word:
                rank += letter_rank[letter]
            if rank not in ranking:
                ranking[rank] = []
            ranking[rank].append(word)
        return ranking
    
    def getBestGuess(self) -> List[str]:
        # Given the possible words, return the best guesses
        # best guesses include the most most common letters possible from counter
        possibleWords = self.getPossibleWords(self.word, self.included, self.excluded)
        if not possibleWords:
            return ["No possible words"]
        rankings = self.rankWords(possibleWords, self.counter.most_common(26))
        bestGuesses = []
        for rank in sorted(rankings.keys(), reverse=True):
            bestGuesses.extend(rankings[rank])
            if len(bestGuesses) >= 10:
                break
        return bestGuesses
    
    def addGuess(self, guess: str, correct: List[int], wrongPos: List[int]) -> None:
        for i in correct:
            if guess[i] not in self.included:
                self.included[guess[i]] = []
            self.word = self.word[:i] + guess[i] + self.word[i+1:]
        for i in wrongPos:
            if guess[i] not in self.included:
                self.included[guess[i]] = []
            self.included[guess[i]].append(i)
        for i in range(len(guess)):
            if i not in correct and i not in wrongPos:
                self.excluded.add(guess[i])
                
    def get_word(self, word: str) -> str:
        return # Wrod from trie
    
if __name__ == "__main__":
    from trie import Trie
    
    wb = WordBank()
    path = os.path.join(os.path.dirname(__file__), "wordle-words.txt")
    wb.readWords(path)
    
    # print(wb.getPossibleWords("__o_e", {'o':[3, 1], 'e':[]}, set([i for i in "thrwbmbsclnevk"])))
    
    # Word: _o_ar
    # Included: {'r':[0,2],'o':[3], 'a':[]}
    # Excluded: set([i for i in "thwgebl"])
    wb.excluded = set([i for i in "thwgebl"])
    wb.included = {'r':[0,2],'o':[3], 'a':[]}
    wb.word = "_o_ar"
    print(wb.getBestGuess())
    
else:
    from src.trie import Trie