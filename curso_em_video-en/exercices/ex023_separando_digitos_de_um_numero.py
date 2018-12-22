#Exercício Python 023: Faça um programa que leia um número de 0 a 9999 e mostre na tela cada um dos dígitos separados.
from math import trunc

number = int(input('enter a number: '))
thousand = trunc(number/1000)
hundred = trunc(number/100)%10
ten = trunc(number/10)%10
unity = trunc(number/1)%10

print('thousand = {}' .format(thousand))
print('hundred = {}' .format(hundred))
print('ten = {}' .format(ten))
print('unity = {}' .format(unity))

#utiliza menos processamento
thousand = number//1000 % 10
hundred = number//100%10
ten = number//10%10
unity = number//1%10