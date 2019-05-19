"""
Exercice Python 012:

O mesmo professor do desafio 019 quer sortear a ordem de apresentação
de trabalhos dos alunos.
Faça um programa que leia o nome dos quatro alunos e mostre a ordem sorteada.
"""
from random import shuffle

studentOne = input('First student: ')
studentTwo = input('Second student: ')
studentThree = input('Third student: ')
stundentFour = input('Fourth student: ')

list_student = [studentOne, studentTwo, studentThree, stundentFour]
listShuffled = shuffle(list_student)
print('The order presentation is: ')
print(list_student)
