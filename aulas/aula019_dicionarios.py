pessoas = {'nomes': 'gustavo', 'sexo': 'm', 'idade': 12}
print(pessoas['nomes'])

#imprime os nomes dos indices
if False:
    print(pessoas.keys())
#imprime os valores dos indices
if False:
    print(pessoas.values())
#imprime tudo
if False:
    print(pessoas.items())

#imprimi dicionario com laco
if False:
    for key, value in pessoas.items():
        print(f'{key} = {value}')

#add novo indice
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
