'''Exercício Python 071: Crie um programa que simule o funcionamento de um caixa eletrônico.
No início, pergunte ao usuário qual será o valor a ser sacado (número inteiro)
e o programa vai informar quantas cédulas de cada valor serão entregues.
OBS: considere que o caixa possui cédulas de R$50, R$20, R$10 e R$1.'''
print('-'*50)
print('\t\t\t\t\tBANK')
print('-'*50)
withdrawal = 0
withdrawal = int(input('How much do you want to take out? R$ '))
fiftyBanknotes = withdrawal // 50
twentyBanknotes = (withdrawal - fiftyBanknotes*50) // 20
tenBanknotes = (withdrawal - fiftyBanknotes*50 - twentyBanknotes*20) // 10
oneBanknotes = withdrawal - fiftyBanknotes*50 - twentyBanknotes*20 - tenBanknotes*10

if fiftyBanknotes > 0:
    print('Total = {:.0f} banknotes of 50,00'.format(fiftyBanknotes))
if twentyBanknotes > 0:
    print('Total = {:.0f} banknotes of 20,00'.format(twentyBanknotes))
if tenBanknotes > 0:
    print('Total = {:.0f} banknotes of 10,00'.format(tenBanknotes))
if oneBanknotes > 0:
    print('Total = {:.0f} banknotes of 1,00'.format(oneBanknotes))
print('*'*50)

