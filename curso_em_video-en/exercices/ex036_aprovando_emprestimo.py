#Exercício Python 036: Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa.
# Pergunte o valor da casa, o salário do comprador e em quantos anos ele vai pagar.
# A prestação mensal não pode exceder 30% do salário ou então o empréstimo será negado.

cores = {'limpa' : '\033[m',
        'azul' : '\033[34m',
        'amarelo' : '\033[33m',
         'vermelho' : '\033[031m'}

valueHouse = int(input('Enter te value of house: R$ '))
salary = int(input('Enter your salary monthly: R$ '))
years = int(input('How old do you to pay the house? '))
monthlyPursuit = (valueHouse/years)/12
print('To a house of R$ {} in {} years the monthly installment will be R$ {:.2f}.' .format(valueHouse, years, monthlyPursuit))
if monthlyPursuit > 0.3*salary:
    print('{}LOAN DENIED'.format(cores['vermelho']))
else:
    print('loan granted')

