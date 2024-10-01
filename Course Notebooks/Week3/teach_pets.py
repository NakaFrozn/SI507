import pet

p1 = pet.pets[0]
p2 = pet.Pet("Polly", ["cracker", "scurvy dog"])

print(p1.speak())
print(p2.speak())

pet.teach_random(p1, 2)
pet.teach_random(p2, 4)

print(p1.speak())
print(p2.speak())

print("in teach_pets.py, my  name is ", __name__) #teach_pets.py
