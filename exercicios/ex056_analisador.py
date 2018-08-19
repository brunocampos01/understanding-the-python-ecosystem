'''Exercício Python 056: Desenvolva um programa que leia o nome, idade e sexo de 4 pessoas.
No final do programa, mostre: a média de idade do grupo, qual é o nome do homem mais velho e
quantas mulheres têm menos de 20 anos.'''

avgYear = 0
yearMenOld = 0
nameMenOld = ''
womens20 = 0

for count in range(1, 5):
    print('-- {}º People --'.format(count))
    name = str(input('Type a name: ')).strip()
    year = int(input('Type year:'))
    avgYear = avgYear + year
    sex = str(input('Type the sex(m/f): ')).strip()

    if count == 1 and sex in 'Mm':
        menOld = year
        nameMenOld = name
    if sex in 'Mm' and year > yearMenOld:
        yearMenOld = year
        name = nameMenOld
    if sex in 'Ff' and year < 20:
        womens20 = womens20 + 1

avgYear = avgYear/4
print('The average of the group is {}'.format(avgYear))
print('The man more old have {} years and call {}'.format(yearMenOld, nameMenOld))
print('Altogether {} womens with less than 20 years.'.format(womens20))