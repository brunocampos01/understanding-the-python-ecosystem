'''Exercício Python 082: Crie um programa que vai ler vários números e colocar em uma lista.
Depois disso, crie duas listas extras que vão conter apenas os valores pares e os valores ímpares digitados,
respectivamente. Ao final, mostre o conteúdo das três listas geradas.'''

list = []
listPair = []
listOdd = []
while True:
    element = int(input('Type a number: '))
    list.append(element)
    leave = str(input('Do you want leave?[Y/N] ')).upper()
    if leave in 'Y':
        break
print('List: {}'.format(list))
for i in list:
    if i%2==0:
        listPair.append(i)
    else:
        listOdd.append(i)
print('='*50)
print('The list {} contains pairs.'.format(listPair))
print('The list {} contains odd.'.format(listOdd))