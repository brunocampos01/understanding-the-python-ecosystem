'''Exercício Python 080: Crie um programa onde o usuário possa digitar cinco valores numéricos
e cadastre-os em uma lista, já na posição correta de inserção (sem usar o sort()).
 No final, mostre a lista ordenada na tela.'''
list = []
count = 0
while True:
    count += 1
    n = int(input('Enter with value: '))
    if n not in list:
        if count == 1 or n > list[-1]:
            list.append(n)
            print(' Added at the bottom of the list  ')
        else:
            indice = 0
            while indice < len(list):
                if n <= list[indice]:
                    list.insert(indice, n)
                    print('Added in position {} of list.'.format(indice))
                    break
                indice += 1
    else:
        print('Duplicate')
    leave = str(input('Do you want leave? [y/n] ')).upper()
    if leave in 'Y':
        break
print(list)