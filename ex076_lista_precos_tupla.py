'''Exercício Python 076: Crie um programa que tenha uma tupla única com nomes de produtos
e seus respectivos preços, na sequência.
No final, mostre uma listagem de preços, organizando os dados em forma tabular.'''
priceList = ('pencil', 1.75, 'eraser', 2.00, 'pen', 1.00, 'notebook', 12.50)
print('-' * 50)
print('\t\t\t\tPRICE LIST')
print('-' * 50)
for position in range(0, len(priceList)):
    if position % 2 == 0:
        print('{:.<30}' .format(priceList[position]), end=' ')
    else:
        print('R$ {:>7.2f}'.format(priceList[position]))
print('-' * 50)
