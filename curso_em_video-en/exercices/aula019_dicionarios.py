'''
Tuplas: () - Parênteses
Listas: [] - Colchetes
Dicionários: {} - Chaves
Exemplo 1 de Dicionário Vazio:
dados = dict()
Exemplo 2 de Dicionário Vazio:
dados = {}'''

#create
pessoas = {}
pessoas = dict()
pessoas = {'nomes': 'gustavo', 'sexo': 'm', 'idade': 12}
print(pessoas)

#create only keys(index)
if False:
    alunos = dict.fromkeys(['aluno', 'nota1', 'nota2'])
    print(alunos)

#prints
if False:
    print(pessoas['nomes'])
    print(pessoas.keys()) #imprime os nomes dos indices
    print(pessoas.values()) #imprime os valores dos indices
    print(pessoas.items()) #tudo

    for k in pessoas.keys():  # Para cada chave "k" nas chaves (keys) do dicionário "pessoas"...
        print('indice: {}'.format(k))

    for v in pessoas.values():
        print('valor: {}'.format(v))

    for k, v in pessoas.items():
        print(f'{k} = {v}')

#Alter VALUES
if False:
    print(pessoas)
    pessoas['sexo'] = 'X' #subtitui
    print(pessoas)
    pessoas.update({'sexo': 'Y'}) #subtitui
    print(pessoas)

#add/pop INDEX
if False:
    pessoas['peso'] = 98 #na pratica, foi criado uma nova lista[]
    print(pessoas)
    pessoas.popitem() #remove ultimo
    print(pessoas)
    pessoas.pop('sexo')
    print(pessoas)
    del pessoas['nomes']
    print(pessoas)

#add VALUES
#insert dict in list
if True:
    brasil = list()
    states = dict()
    for c in range(0, 2):
        estado['uf'] = str(input('UF: '))
        estado['sigle'] = str(input('Sigle: '))
        brasil.append(estado.copy())
    for c in brasil: #percorre lista
        for key, value in c.items(): #percorre o dicionario
            print(f'The space {key} has {value}.')

#dicionarios dentro de lista
if False:
    brasil = []
    estado1 = {'UF': 'Rio de Janeiro', 'sigla': 'RJ'}
    estado2 = {'UF': 'Sao Paulo', 'sigla':'SP'}
    brasil.append(estado1)
    brasil.append(estado2)
    print(brasil)

