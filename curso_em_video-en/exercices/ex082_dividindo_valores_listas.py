"""
Exercise Python 082:

Crie um programa que vai ler vários números e colocar em uma listaa.
Depois disso, crie duas listaas extras que vão conter apenas os valores pares
e os valores ímpares digitados,
respectivamente. Ao final, mostre o conteúdo das três listaas geradas.
"""

lista = []
listaPair = []
listaOdd = []

while True:
    element = int(input('Type a number: '))
    lista.append(element)
    leave = str(input('Do you want leave?[Y/N] ')).upper()

    if leave in 'Y':
        break

print('lista: {}'.format(lista))

for i in lista:
    if i % 2 == 0:
        listaPair.append(i)
    else:
        listaOdd.append(i)

print('=' * 50)
print('The lista {} contains pairs.'.format(listaPair))
print('The lista {} contains odd.'.format(listaOdd))
