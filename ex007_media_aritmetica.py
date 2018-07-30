#Exercício Python 007: Desenvolva um programa que leia as duas notas de um aluno, calcule e mostre a sua médias
note1 = float(input('enter the note 1: '))
note2 = float(input('enter the note 2: '))
result = ((note1 + note2) / 2)
print('The average is: {:.1f}' .format(result))