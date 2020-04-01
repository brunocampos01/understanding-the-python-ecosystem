"""
Exercise Python 078:

Faça um programa que leia 5 valores numéricos e guarde-os em uma listaa.
No final, mostre qual foi o maior e o menor valor digitado
e as suas respectivas posições na listaa.
 """

lista = []
highest = 0
smallest = 0

for c in range(0, 5):
    lista.append(input('Enter a number for the location {}: '.format(c)))

    if c == 0:
        highest = smallest = lista[c]
    elif highest < lista[c]:
        highest = lista[c]
    elif smallest > lista[c]:
        smallest = lista[c]

print(lista)
print('The highest value enterd was {} in position: '.format(highest))

for i, v in enumerate(lista):
    if v == highest:
        print('...{}'.format(i), end='')

print()
print('The smallest value entered was {} in position: '.format(smallest))

for i, v in enumerate(lista):
    if v == smallest:
        print('...{} '.format(i), end='')
