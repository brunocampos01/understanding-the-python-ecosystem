#Exercício Python 047: Crie um programa que mostre na tela todos os números pares que estão no intervalo entre 1 e 50.

for cont in range(2, 51, 2):
    print(cont, end=' ')

print('\n')

for cont in range(1, 51):
    if(cont % 2 == 0):
        print(cont, end=' ')