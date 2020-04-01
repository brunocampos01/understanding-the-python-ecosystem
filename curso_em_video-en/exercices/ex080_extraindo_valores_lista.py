"""
Exercise Python 081:

 Crie um programa que vai ler vários números e colocar em uma lista. Depois disso, mostre:
A) Quantos números foram digitados.
B) A lista de valores, ordenada de forma decrescente.
C) Se o valor 5 foi digitado e está ou não na lista.
"""
lista = []
count = 0
while True:
    lista.append(int(input('Type a number: ')))
    leave = str(input('Do you want continue?[Y/N] ')).upper()

    if leave in 'N':
        break

print('You typed {} elements.'.format(len(lista)))
print('Values in inverse order is: {}'.format(lista.sort(reverse=True)))
print('Ordem typed: {}'.format(lista))

if 5 in lista:
    print('The value 5 belongs to lista')
