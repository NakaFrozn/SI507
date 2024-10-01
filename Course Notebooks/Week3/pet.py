import copy
import random

class Pet:

    def __init__(self, nm, words=["hi", "bye"]):
        self.name = nm
        self.words = copy.copy(words)

    def speak(self):
        my_words = ''
        for w in self.words:
            my_words += w + " "
        return "I can say " + my_words

    def teach(self, new_word):
        self.words.append(new_word)

pets = [
    Pet("Fido"),
    Pet("Rufus", ["breakfast","lunch"]),
    Pet("Sally", [])
]

words = [
    "hall", "child", "depth", "meal", "phone", "tale",
    "tea", "town", "growth", "height", "guest", "thing",
]

def teach_random(pet, num_words):
    num_words = min(num_words, len(words))
    for i in range(num_words):
        j = random.randint(0, len(words) - 1)
        pet.teach(words[j])

if __name__ == "__main__":
  print(pets[1].speak())
  print("In pet.py, my name is", __name__)
