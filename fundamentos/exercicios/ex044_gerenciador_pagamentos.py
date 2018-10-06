''' Exercício Python 044: Elabore um programa que calcule o valor a ser pago por um produto,
considerando o seu preço normal e condição de pagamento:
- à vista dinheiro/cheque: 10% de desconto
- à vista no cartão: 5% de desconto
- em até 2x no cartão: preço formal
- 3x ou mais no cartão: 20% de juros'''
cores = {'limpa': '\033[m',
        'azul': '\033[34m',
        'amarelo': '\033[33m',
        'vermelho': '\033[31m'}

print('\n{}{} LOJAS CARAMBOLAS {}{}'.format(cores['azul'], '='*20, '='*20, cores['limpa']))
value = int(input('\nValue of buys R$: '))
print('''PAYMENT METHODS
[1] in cash
[2] once on the card
[3] twice in the card
[4] 3x in the card''')
choose = int(input('Choose option: '))
if choose == 1:
    value = value*0.9
elif choose == 2:
    value = value*0.95
elif choose == 3:
    value = value
elif choose == 4:
    plots = int(input('How many Plots: '))
    value = value*1.2
    print('Your purcheses will be parceled out in {} of R$ {} with interest.'.format(plots, value/plots))
else:
    print('{}Option Invalid of payment methods!'.format(cores['vermelho']))
print('Your purchases cost R$ {}'.format(value))