#Exercício Python 052: Faça um programa que leia um número inteiro e diga se ele é ou não um número primo.
number = int(input('Type a number: '))
countDividers = 0
for count in range(1, number + 1):
    if number % count == 0:
        countDividers = countDividers + 1
        print('Its divisible for: {}'.format(count))
if count <= 2:
    print('The number {} is cousin'.format(number))
else:
    print('The number is not cousin.')
    print('There are {} dividers.'.format(countDividers))
