"""
Exemplo de Lista (Variável Composta):

lanche = ['Hambúrguer', 'Suco', 'Pizza', 'Pudim']
Índices:      [0]        [1]      [2]      [3]

NOTA 1: As Listas são MUTÁVEIS
"""
lista = [2, 5, 9, 1]
print(lista)

lanche = ['Hambúrguer', 'Suco', 'Pizza', 'Pudim']
print(lanche)

# replacement
lanche[3] = 'Picolé'
print(lanche)

# sort order
lista.sort()
print('Ordenacao da lista: {}'.format(lista))
lista.sort(reverse=True)
print('Ordenacao inversa da lista: {}'.format(lista))

# lenght
print('Quantidade de elementos da lista: {}'.format(len(lista)))

# insert and append
lista.insert(6, 3)
print('Adicionado elemento 6 no meio da lista: {}'.format(lista))
lista.append(900)
print('Adicionado elemento 900 na ultima posicao da lista: {}'.format(lista))

# remove and pop
lista.remove(2)
print('Removido elemento 2 da lista: {}'.format(lista))
lista.pop()
print('Removido ultimo elemento da lista: {}\n '.format(lista))

if False:
    for indice, valor in enumerate(lista):
        print('Na posicao {} encontrei o valor {}.'.format(indice, valor))
