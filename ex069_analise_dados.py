'''Exercício Python 069: Crie um programa que leia a idade e o sexo de várias pessoas. A cada
pessoa cadastrada, o programa deverá perguntar se o usuário quer ou não continuar. No final, mostre:
A) quantas pessoas tem mais de 18 anos.
B) quantos homens foram cadastrados.
C) quantas mulheres tem menos de 20 anos.'''

peoplesMore18 = 0
mens = 0
womensLess18 = 0
while True:
    print('-' * 50)
    print('REGISTER A PERSON')
    print('-' * 50)
    go = ' '
    sex = ' '
    year = int(input('Year: '))
    while sex not in 'MF':
        sex = str(input('Sex[M/F]: ')).strip().upper()
    if year >= 18:
        peoplesMore18 += 1
    if sex == 'M':
        mens += 1
    if sex == 'F' and year < 20:
        womensLess18 += 1
    while go not in 'YN':
        go = str(input('Do you want to continue?[y/n] ')).strip().upper()
    if go == 'N':
        break
print('\nTotal peoples with more 18 years old: {}'.format(peoplesMore18))
print('Total mens registered: {}'.format(mens))
print('Total womens registered with less 20 years old: {}'.format(womensLess18))
