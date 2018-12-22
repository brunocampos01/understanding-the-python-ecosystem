#Exercício Python 005: Faça um programa que leia um número Inteiro e mostre na tela o seu sucessor e seu antecessor.
number = int(input('enter number int: '))
predecessor = number - 1
successor = number + 1
print('o numero {} tem como predecessor {} e {} como sucessor' .format(number, predecessor, successor))

