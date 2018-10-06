'''Exercício Python 092: Crie um programa que leia nome, ano de nascimento e carteira de trabalho
e cadastre-o (com idade) em um dicionário. Se por acaso a CTPS for diferente de ZERO, o dicionário
receberá também o ano de contratação e o salário. Calcule e acrescente, além da idade,
com quantos anos a pessoa vai se aposentar.'''

from datetime import datetime

people = {}
while True:
    people['name'] = str(input('Name: '))
    birth_year = int(input('birth year: '))
    people['years'] = datetime.now().year - birth_year
    people['work_permit'] = str(input('work permit: '))
    if people['work_permit'] == '0':
        break
    people['year_contract'] = int(input('Year contract: '))
    people['salary'] = int(input('Salary: '))
    break
print('-'*50)
for i, v in people.items():
    print(f' - {i} have value {v}.')