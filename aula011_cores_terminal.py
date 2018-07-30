#\033[0;33;44m
print('lista de cores no terminal')
cores = {'limpa': '\033[m',
        'azul': '\033[34m',
        'amarelo': '\033[33m',
        'vermelho': '\033[31m'}
print('{} ola, {}muito {}prazer' .format(cores['azul'], cores['limpa'], cores['amarelo']))


frase = 'Curso em Video de Python'
separado = frase.split()
palavra = separado[2]
letra = palavra[3]
print(letra.upper())

from random import randint
num = randint(1, 6)
res = num // 2
print(res)
