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
    print('the sum is', n1, 'and ', n2, 'worth', s)  # method 1, exceeded, Python 2
    print('the sum is {} and {} worth {}'.format(n1, n2, s))  # method 2
    print('the sum is {0} and {1} worth {2}'.format(n1, n2, s))  # method 3

#checkers types
if False:
    n = input('type something: ')
    print(n.isnumeric())  # Checks if what was entered is or can become a numeric value; returns True if yes
    print(n.isalpha())  # Checks if what is typed is a letter or contains only letters; returns True if yes
    print(n.isalnum())  # Checks if what is typed contains only letters and numbers; returns True if yes
    print(n.isupper())  # Checks if what was typed contains only uppercase letters; returns True if yes
    print(n.isdecimal())