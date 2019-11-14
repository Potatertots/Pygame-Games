import random

battlegrid = [[False] * 7 for i in range(7)] #the grid on which ships will be placed

popper = [[i for i in range(7)] for i in range(7)] #pull coordinates from this
#list to make sure that ships aren't placed on top of each other


def shipplacer(shiplist, reflist):
    '''places one ship at random on the grid'''
    
    size = random.randrange(2,3)
    orientation = random.choice(['h','v']) #random size and orientation

    #randomly determining top/right coordinate of ship
    randy = random.randrange(6)
    randx = random.choice(reflist[randy])
    #reflist[randy].pop(randx)
    shiplist[randy][randx] = True

    #putting on the rest of the ship
    for i in range(1,size):
        if orientation == 'h':
            randx += 1
            #reflist[randy].pop(randx)
            shiplist[randy][randx] = True
        else:
            randy +=1
            #reflist[randy].pop(randx)
            shiplist[randy][randx] = True


def index_2d(data, search):
    ''' .index() function but for 2d lists grr'''
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    return False

    
for i in range(3): #place 3 ships on the battlegrid
    shipplacer(battlegrid,popper)

for i in range(7):
    print(battlegrid[i])

#game variables/lists
guessnum = 0
shipspres = [] #successful guesses
shipsabs = [] #unsuccessful guesses

while True: #game loop

    #status update
    print("Ships have been hit here: " + str(shipspres))
    print("failed guesses: " + str(shipsabs))
    print("number of guesses: " + str(guessnum))

    #user guesses
    xguess = int(input("Guess an x coordinate: "))
    yguess = int(input("Guess a y coordinate: "))

    #check guesses
    if battlegrid[yguess][xguess] == True:
        battlegrid[yguess][xguess] = False
        print("congratulations! you hit a ship!")
        shipspres.append([xguess,yguess])
    else:
        print("no ship here :(")
        shipsabs.append([xguess,yguess])

    #check if they've won 
    if index_2d(battlegrid,True) == False:
        print("Congratulations, you won in " + str(guessnum) + " tries!")
        again = input("Would you like to play again? y or n ") #play again?
        if (again.lower()).strip() == 'y':
            popper = [[i for i in range(7)] for i in range(7)]
            for i in range(3):
                shipplacer(battlegrid,popper)
            guessnum = 0
            shipspres = []
            shipsabs = []
        else:
            print("cya nerds")
            break

    guessnum += 1


    
    
