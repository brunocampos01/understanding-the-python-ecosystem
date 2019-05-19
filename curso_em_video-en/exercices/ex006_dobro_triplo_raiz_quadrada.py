# Exercício Python 006:
# Crie um algoritmo que leia um número e mostre o seu dobro, triplo e raiz quadrada.


number = int(input('Enter a number: '))
double = number * 2
triple = number * 3
square = number ** (1 / 2)
print('Your number is: {0} \ndouble: {1}\ntriple: {2}\nsquare:{3}'.format(number, double, triple, square))
