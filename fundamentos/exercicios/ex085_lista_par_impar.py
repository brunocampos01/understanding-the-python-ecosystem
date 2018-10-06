'''Exercício Python 085: Crie um programa onde o usuário possa digitar sete valores numéricos
e cadastre-os em uma lista única que mantenha separados os valores pares e ímpares.
No final, mostre os valores pares e ímpares em ordem crescente.'''
pair = []
odd = []
values = [[pair], [odd]]
for c in range(0, 7):
    value = int(input('Type the value: '))
    values.append(value)
    if value % 2 == 0:
        pair.append(value)
    else:
        odd.append(value)
pair.sort()
odd.sort()
print('='*50)
print(values)
print('Pairs = {}'.format(pair))
print('Odd = {}'.format(odd))
