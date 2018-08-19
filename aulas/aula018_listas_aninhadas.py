if False:
    pessoal = list()
    dados = ['Pedro', 25]
    pessoal.append(dados[:])  # Adiciona todos os itens de "dados" a "pessoal", criando uma lista dentro da outra (composta)
    print(pessoal)

if False:
    pessoas = [['Pedro', 25], ['Maria', 19], ['João', 32]]  # Cria uma lista composta "pessoas" com 3 listas dentro
    print(pessoas[0][0])
    print(pessoas[1][1])
    print(pessoas[1])

if True:
    galera = [['João', 19], ['Ana', 33], ['Joaquim', 13], ['Maria', 45]]
    print(galera)
    print(galera[0])
    print(galera[0][0])
    print(galera[2][1])

    for pessoa in galera: # Para cada "pessoa" na lista composta "galera"...
        print(pessoa)

    for pessoa in galera:
        print('pessoa[0]: {}'.format(pessoa[0]))

    for pessoa in galera:
        print('pessoa[1]: {}'.format(pessoa[1]))

    for pessoa in galera:
        print(f'{pessoa[0]} tem {pessoa[1]} anos de idade.')

    for indice, valor in enumerate(galera):
        print(f'O indice {indice} tem a lista: {valor}')