'''Exercício Python 084: Faça um programa que leia nome e peso de várias pessoas, guardando tudo em uma lista.
 No final, mostre:
A) Quantas pessoas foram cadastradas.
B) Uma listagem com as pessoas mais pesadas.
C) Uma listagem com as pessoas mais leves.'''

listName = []
listWeight = []
data = [listName, listWeight]
while True:
    name = str(input('Name: '))
    listName.append(name)
    weight = float(input('Weight KG: '))
    listWeight.append(weight)
    leave = str(input('Do you want leave?[Y/N] ')).upper()
    if leave in 'Y':
        break
print('*'*50)
print('datas: {}'.format(data))
print('Total: {}'.format(len(data)))
greater = max(listWeight)
lower = min(listWeight)
print('The greater Weight has {} kg and his name is {}'.format(greater, listName[listWeight.index(greater)]))
print('The lower Weight has {} kg and his name is {}'.format(lower, listName[listWeight.index(lower)]))



