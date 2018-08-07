
lanche = ('haburger', 'batata doce', 'pizza', 'pudim')
print(lanche[0:])
print(lanche[1:])
print(lanche[-3])

#tuplas sao imutaveis
#lanche[1] = 'refrigerante'

#organiza por ordem
print(sorted(lanche))

#exibindo todos os dados e posicoes
for comida in lanche:
    print('Eu vou comer {}.'.format(comida))

for cont in range(0, len(lanche)):
    print('Comi {} na seguinte ordem: {}'.format(lanche[cont], cont))
    print(lanche[cont])

#concatenacao de tuplas
a = (2, 5, 4)
b = (5, 8, 1, 2)
c = a + b
print(c)
print('O tamanho da tupla eh: {}'.format(len(c)))
print('O numero 5 aparece {} vezes na tupla.' .format(c.count(5)))
print('A posicao do numero 1 eh {}'.format(c.index(1)))

#deletar variaveis
del (c)
print(c)