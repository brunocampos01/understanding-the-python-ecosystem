#Exercício Python 010: Crie um programa que leia quanto dinheiro uma pessoa
# tem na carteira e mostre quantos dólares ela pode comprar.
money = float(input('How much money does you have? R$ '))
moneyInDolar = money/3.85
print('With R$ {} you can buy US$ {:.3f}' .format(money, moneyInDolar))