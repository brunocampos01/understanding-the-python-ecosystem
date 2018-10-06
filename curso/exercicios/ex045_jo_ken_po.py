#Exercício Python 045: Crie um programa que faça o computador jogar Jokenpô com você.
from random import randint
from time import sleep
print('''Your chooce:
[0] STONE
[1] PAPER
[2] scissors ''')
itens = ('stone', 'paper','scissors')
chooce = int(input('Which is your move? '))
choocePc = randint(0, 2)

print('JO')
sleep(1)
print('KEN')
sleep(1)
print('PO!!!')
sleep(1)

print('{}\nPC throwed: {}'.format('-='*20, itens[choocePc]))
print('Player throwed: {}\n{}'.format(itens[chooce], '-='*20))

if chooce == choocePc:
    print('tie')
elif chooce == 0 and choocePc == 1:
    print('Paper GAIN stone')
elif chooce == 0 and choocePc == 2:
    print('stone GAIN scissors')
elif chooce == 1 and choocePc == 0:
    print('paper GAIN stone')
elif chooce == 1 and choocePc == 2:
    print('Scissors GAIN paper')
elif chooce ==2 and choocePc == 0:
    print('stone GAIN scissors')
elif chooce == 2 and choocePc == 1:
    print('scissors GAIN paper')
else:
    print('Invalid !')