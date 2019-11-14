def shift(n, phrase):
    newphrase = []
    for i in phrase:
        i = ord(i)
        if i >= 97 and i <= 122:
            i += (n-97)
            i = i%26 + 97
        elif i >= 65 and i <= 90:
            i += (n-65)
            i = i%26 + 65
        newphrase.append(chr(i))
    return newphrase

while True:
    og = input("Enter a phrase: ")

    key = "a"
    while type(key) != int:
        try:
            key = int(input("enter a shift key: "))
        except:
            key = int(input("enter a NUMBER: "))

    code = shift(key, og)

    print("".join(code))

    goBack = input("Display original? Y or N: ").lower()
    if goBack.startswith("y"):
        print(og)

    cont = input("continue? Y or N: ").lower()
    if cont.startswith("n"):
        break

    print()
    print()

