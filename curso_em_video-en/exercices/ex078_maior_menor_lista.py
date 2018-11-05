'''Exercício Python 078: Faça um programa que leia 5 valores numéricos e guarde-os em uma lista.
No final, mostre qual foi o maior e o menor valor digitado e as suas respectivas posições na lista. '''

list = []
highest = 0
smallest = 0
for c in range(0, 5):
    list.append(input('Enter a number for the location {}: '.format(c)))
    if c == 0:
        highest = smallest = list[c]
    elif highest < list[c]:
        highest = list[c]
    elif smallest > list[c]:
        smallest = list[c]
print(list)
print('The highest value enterd was {} in position: '.format(highest))
for i, v in enumerate(list):
    if v == highest:
        print('...{}'.format(i), end='')
print()
print('The smallest value entered was {} in position: ' .format(smallest))
for i, v in enumerate(list):
    if v == smallest:
        print('...{} '.format(i), end='')