'''Exercício Python 074: Crie um programa que vai gerar cinco números aleatórios e colocar em uma tupla. Depois disso,
mostre a listagem de números gerados e também indique o menor e o maior valor que estão na tupla.'''

from random import randint
numbers = (randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10), randint(1, 10))
highest = 0
lower = 0
for c in numbers:
    print('{} '.format(c), end='\n')
    if c == numbers[0]:
        lower = c
    elif c < lower:
        lower = c
    if c > highest:
        highest = c
print('Lower = {}'.format(lower))
print('Highest = {}'.format(highest))
#or
print(max(numbers))
print(min(numbers))