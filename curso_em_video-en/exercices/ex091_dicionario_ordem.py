"""
Exercice Python 030:

Le nome + media 2 alunos. No final exibe conteudo estruturado na tela
"""

import secrets
from operator import itemgetter
from time import sleep


game = {'player1': secrets.randbelow(6),
        'player2': secrets.randbelow(6),
        'player3': secrets.randbelow(6),
        'player4': secrets.randbelow(6)}
ranking = {}

print('#' * 50)
print('Values: ')
for i, v in game.items():
    print(f'{i} took the number {v}')
    sleep(0.5)

ranking = sorted(game.items(), key=itemgetter(1), reverse=True)

print('#' * 50)
print('Ranking')
for i in ranking:
    print(i)
