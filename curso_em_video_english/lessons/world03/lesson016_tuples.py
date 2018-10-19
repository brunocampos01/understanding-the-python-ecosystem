"""Em Python, existem 3 tipos de Variáveis Compostas:
- Tuplas
- Listas
- Dicionários
lanche = ('Hambúrguer', 'Suco', 'Pizza', 'Pudim')
Índices:      [0]        [1]      [2]      [3]
NOTA 1: As Tuplas são IMUTÁVEIS!"""

lanche = ('haburger', 'batata doce', 'pizza', 'pudim')

print(lanche[0:])
print(lanche[1:])
print(lanche[-1])
#lanche[1] = 'Refrigerante' -> Impossible command, since tuples are immutable

#count elements
print(len(lanche))

#organiza por ordem
print(sorted(lanche))

if False:
    #exibindo todos os dados e posicoes
    for comida in lanche:
        print('Eu vou comer {}.'.format(comida))

    for cont in range(0, len(lanche)):
        print('Comi {} na seguinte ordem: {}'.format(lanche[cont], cont))
        print(lanche[cont])

    for indice, quecomida in enumerate(lanche):  # Para cada posição "pos" e elemento "quecomida" em "lanche"...
        print(f'{quecomida} na posição {indice}')

if True:
    #concatenacao de tuplas
    a = (2, 5, 4)
    b = (5, 8, 1, 2)
    c = a + b
    d = b + a
    print('c = {}'.foramt(c))
    print('d = {}'.format(d))
    print('O tamanho da tupla eh: {}'.format(len(c)))
    print('O numero 5 aparece {} vezes na tupla.' .format(c.count(5)))
    print('A posicao do numero 1 eh {}'.format(c.index(1)))
if False:
    #deletar tupla
    del (c)
    print(c)

# Tuplas aceitam vários tipos de dados, não necessariamente do mesmo tipo.
if False:
    pessoa = ('Gustavo', 39, 'M', 99.88)  # Tupla "pessoa" com dados str, int, str e float, respectivamente
    print(pessoa)  # Exibe ('Gustavo', 39, 'M', 99.88)

if False:
    del(pessoa)
# del(pessoa[0]) -> Comando impossível, pois não se pode deletar um único elemento da tupla
