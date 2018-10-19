'''Exercício Python 059: Crie um programa que leia dois valores e mostre um menu na tela:
[ 1 ] somar
[ 2 ] multiplicar
[ 3 ] maior
[ 4 ] novos números
[ 5 ] sair do programa
Seu programa deverá realizar a operação solicitada em cada caso.'''

number1 = int(input('Type a number: '))
number2 = int(input('Type a number: '))
chooce = 0
while chooce != 6:
    print('-='*50)
    chooce = int(input(''' \t[1] sum
    [2] multiply
    [3] divide
    [4] subtract
    [5] new number
    [6] exit
    Which choose? '''))
    if chooce == 1:
        sum = number1 + number2
        print('Sum = {}'.format(sum))
    if chooce == 2:
        multiply = number1 * number2
        print('Mutiply = {}'.format(multiply))
    if chooce == 3:
        divide = number1/number2
        print('Divide = {}'.format(divide))
    if chooce == 4:
        subtract = number1 = number2
        print('Subtract = {}'.format(subtract))
    if chooce == 5:
        number1 = int(input('Type a number: '))
        number2 = int(input('Type a number: '))
print("End")
