'''Exercício Python 070: Crie um programa que leia o nome e o preço de vários produtos. O programa deverá perguntar se o usuário vai continuar ou não. No final, mostre:
A) qual é o total gasto na compra.
B) quantos produtos custam mais de R$1000.
C) qual é o nome do produto mais barato. '''
print('-'*50)
print('CHEAPS SHOPS')
print('-'*50)

valueTotal = 0
above1000 = 0
productMoreCheap = ' '
cheaperPrice = 0
count = 0
while True:
    productName = str(input('Name product: ')).strip()
    productPrice = int(input('Price: R$ '))
    count += 1
    valueTotal += productPrice
    if count == 1:
        productMoreCheap = productName
        cheaperPrice = productPrice
    if cheaperPrice > productPrice:
        cheaperPrice = productPrice
        productMoreCheap = productName
    if productPrice > 1000:
        above1000 =+ 1
    go = ' '
    while go not in 'YN':
        go = str(input('Do you want to continue?[Y/N] ')).strip().upper()
    if go == 'N':
        break
print('--- END ---')
print('Pruchese balance: {}'.format(valueTotal))
print('There are {} product above value R$ 1000'.format(above1000))
print('The product more cheaps is {} and cost R$ {}'.format(productMoreCheap, cheaperPrice))
