#Exercício Python 004:
# Faça um programa que leia algo pelo teclado e mostre na tela o seu tipo primitivo
# e todas as informações possíveis sobre ele.

a =input('Digite algo: ')
print('the type this value is ', type(a))
print('so tem espacos?', a.isspace())
print('eh numero?', a.isnumeric())
print('eh alfanumero?', a.isalnum())
print('esta em maiusculas?', a.isupper())
print('eta em minusculas? {}'.format(a.islower()))
print('eta em minusculas?', a.islower())
