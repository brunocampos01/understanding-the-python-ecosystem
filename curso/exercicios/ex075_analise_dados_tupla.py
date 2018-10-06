'''Exercício Python 075: Desenvolva um programa que leia quatro valores pelo teclado e guarde-os em uma tupla. No final, mostre:
A) Quantas vezes apareceu o valor 9.
B) Em que posição foi digitado o primeiro valor 3.
C) Quais foram os números pares.'''

numbers = ((int(input('Type a number: '))), (int(input('Type a number: '))),
          (int(input('Type a number: '))), (int(input('Type a number: '))))
print(numbers)
print('The number 9 appeared {} times in tuple.'.format(numbers.count(9)))
if 3 in numbers:
    print('The number 3 appeared in position {} in of tuple.'.format(numbers.index(3) + 1))
print('The numbers pair are: ')
for n in numbers:
    if n % 2 == 0:
        print(n, end=' ')