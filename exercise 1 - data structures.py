def removeDup(listy):
    for i in listy:
        while listy.count(i) > 1:
            listy.remove(i)
    return listy



def longerthan(string):
    n = int(input("length:"))
    string = string.split()
    longer = []
    for i in string:
        if len(i) > n:
            longer.append(i)
    return longer

thing = 'Roses are red Violets are blue Computer Science is fun Python is too'

print(longerthan(thing))

