'''Exercício Python 083: Crie um programa onde o usuário digite uma expressão qualquer que use parênteses.
Seu aplicativo deverá analisar se a expressão passada está com os parênteses abertos e fechados na ordem correta.'''

listOpen = []
listClose = []
print('Program to validate parentheses')
print('-'*50)
expression = str(input('Type a expression: ')).lower()

for value in expression:
    if value in "(":
        listOpen.append(value)
    elif value in ")":
        listClose.append(value)

if len(listOpen) == len(listClose):
    print('His expression is valid.')
else:
    print('Expression is not valid.')

'''
other form:
using stack
when find ( append in stack
when find ) pop in stack
'''