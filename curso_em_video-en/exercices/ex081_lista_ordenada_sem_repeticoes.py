"""
Exercise Python 080:

Crie um programa onde o usuário possa digitar cinco valores numéricos
e cadastre-os em uma listaa, já na posição correta de inserção (sem usar o sort()).
No final, mostre a listaa ordenada na tela.
 """
lista = []
count = 0
while True:
    count += 1
    n = int(input('Enter with value: '))

    if n not in lista:
        if count == 1 or n > lista[-1]:
            lista.append(n)
            print(' Added at the bottom of the lista  ')
        else:
            indice = 0
            while indice < len(lista):

                if n <= lista[indice]:
                    lista.insert(indice, n)
                    print('Added in position {} of lista.'.format(indice))
                    break
                indice += 1
    else:
        print('Duplicate')
    leave = str(input('Do you want leave? [y/n] ')).upper()

    if leave in 'Y':
        break
print(lista)
