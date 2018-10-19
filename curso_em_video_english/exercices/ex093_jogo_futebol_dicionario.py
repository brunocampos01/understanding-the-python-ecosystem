#ex 93 + 95
'''Exercício Python 093: Crie um programa que gerencie o aproveitamento de um jogador de futebol.
 O programa vai ler o nome do jogador e quantas partidas ele jogou.
 Depois vai ler a quantidade de gols feitos em cada partida. No final, tudo isso será guardado em um dicionário,
  incluindo o total de gols feitos durante o campeonato.'''

player = dict()
matches = list()
name = str(input('Player soccer: '))
player['name'] = name
total = int(input(f'How much games {name} played ? '))
total_goals = 0

for playes in range(0, total):
    matches.append(int(input(f'How much goals {name} did in playes {playes + 1} ? ')))
# insert list matches in dict
player['matches'] = matches[:]
print('#'*50)
for i, v in player.items():
    print(f' The field {i} has value {v}')
# equal for
total_goals = sum(matches)
print('#'*50)
print(f'The player {name} played {total} and did {total_goals} goals !')
