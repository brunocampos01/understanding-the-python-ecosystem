'''Exercício Python 088: Faça um programa que ajude um jogador da MEGA SENA a criar palpites.
O programa vai perguntar quantos jogos serão gerados e vai sortear 6 números entre 1 e 60 para cada jogo,
 cadastrando tudo em uma lista composta.'''
from random import randint
print('-'*50)
print('\t\t\t\t MEGA SENA')
print('-'*50)
amount = int(input('How much games raffled? '))
games = []
list = []
tot = 1
print('waint...')
while tot <= amount:
    count = 0
    while True:
        num = randint(1, 60)
        if num not in list:
            list.append(num)
            count += 1
        if count >= 6:
            break
    list.sort()
    games.append(list[:])
    list.clear()
    tot += 1
print('raffleds: {}'.format(amount))
for i, v in enumerate(games):
    print('game {}: {}'.format(i+1, v))
