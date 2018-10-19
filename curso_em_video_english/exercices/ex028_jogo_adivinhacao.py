#Exercício Python 028: Escreva um programa que faça o computador "pensar"
#em um número inteiro entre 0 e 5 e peça para o usuário tentar descobrir qual
#foi o número escolhido pelo computador.
# O programa deverá escrever na tela se o usuário venceu ou perdeu.
from random import randint
from time import sleep
print('#'*100)
print('Try a guess a number between 0 until 5...')
print('#'*100)
numberPC = randint(0,5)
numberUser = int(input('which number I think ? '))
print('\nPROCESS...')
sleep(2)
if numberPC == numberUser:
    print('You win !!!')
print('\nMy number is: {}' .format(numberPC))
print('Your number is {}' .format(numberUser))
print('#'*10,'END','#'*10)