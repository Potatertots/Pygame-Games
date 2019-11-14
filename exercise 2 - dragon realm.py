import random
import time

def displayIntro():
    print('You are in a land full of dragons. In front of you,')
    print('you see two caves. In one cave, the dragon is friendly')
    print('and will share his treasure with you. The other dragon')
    print('is greedy and hungry, and will eat you on sight.')
    print()

def chooseCave():
    cave = ''
    while cave != '1' and cave != '2':
        print('Which cave will you go into? (1 or 2)')
        cave = input()

    return cave

def checkCave(chosenCave):
    print('You approach the cave...')
    time.sleep(2)
    print('It is dark and spooky...')
    time.sleep(2)
    print('A large dragon jumps out in front of you! He opens his jaws and...')
    print()
    time.sleep(2)

    friendlyCave = random.randint(1, 2)

    if chosenCave == str(friendlyCave):
         print('Invites you into his cave!')
         return("safe")
    else:        
        print('Gobbles you down in one bite!')
        return "dead"

def friendly():
    print("The dragon congratulates you on being the first hero to find him in years.")
    print("He apologizes that his lair is so messy - he wasn't expecting guests!")
    print(" ")
    time.sleep(1)
    print("Unfortunately, suddent fluctutations in the stock market put him into a bad mood.")
    print("He demands you tell him a joke, or face certain DEATH. Do you say:")
    print(" ")
    time.sleep(1)
    print("1. I can count on one hand the number of times I've been to Chernobyl ... six!")
    time.sleep(1)
    print("2. What do you call a cow with three legs? Lean beef!")
    time.sleep(1)
    print("3. YOUR MOM IS THE JOKE.")
    print("(Enter 1, 2, or 3)")
    print(" ")
    joke = input()
    if joke == "1":
        print("The dragons gives you his treasure!")
    else:
        print("The dragon summarily yeets you.")

playAgain = 'yes'
while playAgain == 'yes' or playAgain == 'y':

    displayIntro()

    caveNumber = chooseCave()

    isSafe = checkCave(caveNumber)

    if isSafe == "safe":
        friendly()

    print('Do you want to play again? (yes or no)')
    playAgain = input()

