from  random import randint
from time import sleep
from operator import itemgetter

game = {'player1': randint(1, 6),
        'player2': randint(1, 6),
        'player3': randint(1, 6),
        'player4': randint(1, 6)}
ranking = {}

print('#'*50)
print('Values: ')
for i, v in game.items():
    print(f'{i} took the number {v}')
    sleep(0.5)

ranking = sorted(game.items(), key=itemgetter(1), reverse=True)

print('#'*50)
print('Ranking')
for i in ranking:
    print(i)