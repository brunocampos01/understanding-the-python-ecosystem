"""
Exercice Python 030:

Crie um programa que leia um número inteiro e mostre na tela se ele é PAR ou ÍMPAR.
"""

#Exercício Python 051: Desenvolva um programa que leia o primeiro termo e a
# razão de uma PA. No final, mostre os 10 primeiros termos dessa progressão.
print('='*40)
print('\t10 TERMS OF ARITHMETIC PROGRESSION')
print('='*40)

first = int(input('Type the first term: '))
ratio = int(input('ratio: '))
tenth = first + (10 - 1) * ratio

for count in range(first, tenth + ratio, ratio):
    print('{}'.format(count), end=' -> ')
print('END')
