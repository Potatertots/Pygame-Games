import pygame
from os import path

pygame.init()


#load sound files
snd_dir = path.dirname(__file__)

ans_sound = pygame.mixer.Sound(path.join(snd_dir, 'answer.wav'))
ex_sound = pygame.mixer.Sound(path.join(snd_dir, 'exit.wav'))
error = pygame.mixer.Sound(path.join(snd_dir, 'error.wav'))

operator = 'hi' #tells program how to proceed, 'hi' is filler


#defining functions
def add(num1, num2):
    ''' add two numbers'''
    return (num1 + num2)

def sub(num1, num2):
    '''subtract num2 from num1'''
    return (num1 - num2)

def div(num1, num2):
    '''divide num1 by num2'''
    if num2 == 0:
        error.play()
        return "error - enter a non-zero divisor"
    return (num1/num2)

def mult(num1, num2):
    '''multiply num1 and num2'''
    return (num1 * num2)

def exp(num1, num2):
    '''num1 to the power of num2'''
    multer = num1
    if num2 == 0:
        return 1
    elif num2 == 1:
        return num1
    for i in range(num2 -1):
        num1 = num1*multer
    return num1

def fact(n):
    '''n factorial'''
    if n == 0:
        return 1
    ans = n
    for i in range(1,n):
        ans = ans*(n-i)
    return int(ans)

def choose(n,r):
    '''choose function in math'''
    return int(fact(n)/(fact(r) * fact(n-r)))

def answer(to_print):
    ans_sound.play()
    print("Your answer is " + str(to_print))


while operator != "exit":
    print('Welcome to the TI 150.')
    operator = input("Please enter operator ( +, -, *, /, **, choose, exit ): ")
    operator = (operator.lower()).strip()
    if operator == 'exit':
        ex_sound.play()
        break
    try:
        a = int(input("please enter your first number "))
        b = int(input("please enter your second number "))
        if operator == "+":
            ans = add(a,b)
            answer(ans)
        elif operator == "-":
            ans = sub(a,b)
            answer(ans)
        elif operator == "*":
            ans = mult(a,b)
            answer(ans)
        elif operator == "/":
            ans = div(a,b)
            answer(ans)
        elif operator == "**":
            ans = exp(a,b)
            answer(ans)
        elif operator == "choose":
            ans = choose(a,b)
            answer(ans)
        else:
            error.play()
            print("please enter one of the given functions")
    except: #error handling
        error.play()
        print("please enter a number - no letters or special characters")
        print()

    
