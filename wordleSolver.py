from english_words import english_words_lower_alpha_set
import random as rand
import re

def main() -> None:
    notUsed, correctPos, wrongPos, used = set(), {}, {}, set()
    possibles = [i for i in english_words_lower_alpha_set if len(i) == 5]
    #word = rand.sample(possibles,1)[0]
    word = "adieu"
    print("First Guess:", word)
    while(True):
        userinput = input("Was that the word? (y,n,r,h) ").lower()
        if userinput == 'h':
            print("y: yes\nn: no\nr: reroll new word\nh: help\nq: quit")
            pass
        elif userinput == 'y':
            print("Word found!")
            break
        elif userinput == 'r':
            possibles.remove(word)
            word = rand.sample(possibles, 1)[0]
            print("New word:",word)
            continue
        elif userinput == 'q':
            print("Exiting...")
            return
        else:
            tempUsed = set(input("Please enter all letters that are used in the word: ").lower())
            used = used.union(tempUsed)
            for i in tempUsed:
                occurences = [m.start() for m in re.finditer(i, word)]
                if len(occurences) == 1:
                    res = input(f"Was '{i}' in the correct spot?(y/n) ").lower()
                    if res == 'y':
                        correctPos[i] = occurences[0]
                    else:
                        wrongPos[occurences[0]] = i
                else:
                    for j in occurences:
                        res = input(f"Was '{i}' at index {j+1} correct?(y/n) ").lower()
                        if res == 'y':
                            correctPos[i] = j
                        else:
                            wrongPos[j] = i

            notUsed = notUsed.union(set([i for i in word if i not in used]))

            possibles = [i for i in possibles if all([j not in i for j in notUsed])
                            and all([j in i for j in used])
                            and all([i[k] == j for j,k in correctPos.items()])
                            and all([i[j] != k for j,k in wrongPos.items()])
                         ]
            try:
                word = rand.sample(possibles, 1)[0]
                print("New word:",word)
            except Exception as e:
                print(e)
                print("Possibles:", possibles)
                exit()

if __name__ == "__main__":
    main()
