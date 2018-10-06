'''Exercício Python 022: Crie um programa que leia o nome completo de uma pessoa e mostre:
– O nome com todas as letras maiúsculas e minúsculas;
– Quantas letras ao todo sem considerar espaços;
– Quantas letras tem o primeiro nome.'''

name = input('Enter your name complety: ')
list = name.split()
print('Analyzing...')
print('Your name in upper is: {}' .format(name.upper()))
print('Your name in lower is: {}' .format(name.lower()))
print('Your name has {} letters' .format(len(name)))
print('Your first name is {}' .format(list[0]))
print('Your fisrt name has {} letters' .format(len(list[0])))
print('Your fisrt name has {} letters' .format(name.find(' ')))