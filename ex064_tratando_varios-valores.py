'''Exercício Python 064: Crie um programa que leia vários números inteiros pelo teclado.
O programa só vai parar quando o usuário digitar o valor 999, que é a condição de parada. No final,
 mostre quantos números foram digitados e qual foi a soma entre eles (desconsiderando o flag).'''
number = 0
count = 0
sum = 0
while number != 999:
    number = int(input('Type a number [999 to stop] :'))
    if number != 999:
        count += 1
        sum += number
print('You typed {} number and sum is: {}'.format(count, sum))

'''
if n == 999
    break'''
