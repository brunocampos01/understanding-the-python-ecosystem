'''Exercício Python 081: Crie um programa que vai ler vários números e colocar em uma lista. Depois disso, mostre:
A) Quantos números foram digitados.
B) A lista de valores, ordenada de forma decrescente.
C) Se o valor 5 foi digitado e está ou não na lista.'''
list = []
count = 0
while True:
    list.append(int(input('Type a number: ')))
    leave = str(input('Do you want continue?[Y/N] ')).upper()
    if leave in 'N':
        break
print('You typed {} elements.'.format(len(list)))
print('Values in inverse order is: {}'.format(list.sort(reverse=True)))
print('Ordem typed: {}'.format(list))
if 5 in list:
    print('The value 5 belongs to list')
