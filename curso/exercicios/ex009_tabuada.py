#Exercício Python 009: Faça um programa que leia um número Inteiro qualquer e mostre na tela a sua tabuada.
numberTable = int(input('Enter the number to know the table: '))
print('-'*10)
print('{} X {:2} = {}' .format(numberTable, 1, numberTable*1))
print('{} X {:2} = {}' .format(numberTable, 9, numberTable*9))
print('-'*10)