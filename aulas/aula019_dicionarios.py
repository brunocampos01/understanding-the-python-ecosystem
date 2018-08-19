'''
Tuplas: () - Parênteses
Listas: [] - Colchetes
Dicionários: {} - Chaves
Exemplo 1 de Dicionário Vazio:
dados = dict()
Exemplo 2 de Dicionário Vazio:
dados = {}'''

pessoas = {'nomes': 'gustavo', 'sexo': 'm', 'idade': 12}
if False:
    print(pessoas['nomes'])
    print(pessoas.keys()) #imprime os nomes dos indices
    print(pessoas.values()) #imprime os valores dos indices
    print(pessoas.items()) # tudo

    for k in pessoas.keys():  # Para cada chave "k" nas chaves (keys) do dicionário "pessoas"...
        print('indice: {}'.format(k))

    for v in pessoas.values():
        print('valor: {}'.format(v))

    for k, v in pessoas.items():
        print(f'{k} = {v}')

#add indice
if False:
    pessoas['peso'] = 98
    print(pessoas.values())

#dicionarios dentro de lista
if False:
    brasil = []
    estado1 = {'UF': 'Rio de Janeiro', 'sigla': 'RJ'}
    estado2 = {'UF': 'Sao Paulo', 'sigla':'SP'}
    brasil.append(estado1)
    brasil.append(estado2)
    print(brasil)

#copiar elementos internos
#usar um dicionario temporario
if False:
    estado = dict()
    brasil = list()
    for c in range(0, 3):
        estado['uf'] = str(input('UF: '))
        estado['sigla'] = str(input('Sigle: '))
        brasil.append(estado.copy())
    for c in brasil:
        for key, value in c.items():
            print(f'The space {key} has {value}.')
