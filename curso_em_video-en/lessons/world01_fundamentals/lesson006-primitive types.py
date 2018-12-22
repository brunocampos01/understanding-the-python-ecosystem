#implicit types
if False:
    counter = 100 # integer
    miles = 500.0 # float point
    name = "Rocky Balboa" # string
    print (counter)
    print (miles)
    print (name)

#mix types
if False:
    n1 = float(input('enter value: '))
    n2 = int(input('enter other value: '))
    s = n1 + n2
    print('the sum is {}, and {} = {}' .format(n1, n2, s))

#prints
if False:
    n1 = int(input('enter value: '))
    n2 = int(input('enter other value: '))
    s = n1 + n2
    print('the sum between {} and {} is {}'.format(n1, n2, s))  # method 1
    print(f'the sum between {n1} and {n2} is {s}')  # method f strings

#checkers types
if False:
    n = input('type something: ')
    print(n.isnumeric())  # Checks if what was entered is or can become a numeric value; returns True if yes
    print(n.isalpha())  # Checks if what is typed is a letter or contains only letters; returns True if yes
    print(n.isalnum())  # Checks if what is typed contains only letters and numbers; returns True if yes
    print(n.isupper())  # Checks if what was typed contains only uppercase letters; returns True if yes
    print(n.isdecimal())
