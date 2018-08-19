#Exercício Python 030: Crie um programa que leia um número inteiro e mostre na tela se ele é PAR ou ÍMPAR.
number = int(input('Tell me a number: '))
if number%2 == 0:
    print('The number {} is even' .format(number))
else:
    print('The number {} is odd' .format(number))