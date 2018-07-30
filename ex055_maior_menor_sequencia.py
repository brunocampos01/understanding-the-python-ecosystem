#Exercício Python 055: Faça um programa que leia o peso de cinco pessoas. No final, mostre qual foi o maior e o menor peso lidos.
bigger = 0
smaller = 0
for count in range(1, 6):
    value = int(input('number {}: '.format(count)))
    if count == 1:
        bigger = value
        smaller = value
    else:
        if value > bigger:
            bigger = value
        if value < smaller:
            smaller = value
print('The bigger number is: {} '.format(bigger))
print('The smaller number is: {} '.format(smaller))