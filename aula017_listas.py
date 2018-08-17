#tupla = (2, 5, 9, 1)
#tuplas sao imutaveis
#num[2] = 5

lista = [2, 5, 9, 1]
print(lista)
lista.sort()
print('Ordenacao da lista: {}'.format(lista))
print('Quantidade de elementos da lista: {}'.format(len(lista)))
lista.insert(6, 3)
print('Adicionado elemento 6 no meio da lista: {}'.format(lista))
lista.append(900)
print('Adicionado elemento 900 na ultima posicao da lista: {}'.format(lista))
lista.remove(2)
print('Removido elemento 2 da lista: {}'.format(lista))
lista.pop()
print('Removido ultimo elemento da lista: {}\n '.format(lista))

for position, valor in enumerate(lista):
    print('Na posicao {} encontrei o valor {}.'.format(position, valor))