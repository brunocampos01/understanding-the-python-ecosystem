'''Exercício Python 072: Crie um programa que tenha uma tupla totalmente preenchida com
 uma contagem por extenso, de zero até vinte.
 Seu programa deverá ler um número pelo teclado (entre 0 e 20) e mostrá-lo por extenso.'''
numbers = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
           'nine', 'ten', 'eleven', 'twelve', 'thirteen','fourteen', 'fifteen', 'sixteen',
           'seventeen', 'eightteen', 'nineteen', 'twenty')


'''number = int(input('Enter a number between 0 and 20: '))
while number < 0 or number > 20:
    print('Try again.')
    number = int(input('Enter a number between 0 and 20: '))
print('You type the number {}'.format(numbers[number]))'''

# less
while True:
    number = int(input('Enter a number between 0 and 20: '))
    if 0 <= number <= 20:
        break
    print('Try again.')
print('You type the number {}'.format(numbers[number]))
