'''Exercício Python 079: Crie um programa onde o usuário possa digitar vários valores numéricos
 e cadastre-os em uma lista. Caso o número já exista lá dentro, ele não será adicionado.
 No final, serão exibidos todos os valores únicos digitados, em ordem crescente. '''

valuesList = []
while True:
    n = int(input('Enter with value: '))
    if n not in valuesList:
        valuesList.append(n)
    else:
        print('Duplicate')
    leave = str(input('Do you want leave? [y/n] ')).upper()
    if leave in 'Y':
        break
print('-'*30)
valuesList.sort()
print(valuesList)