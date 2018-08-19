#Exercício Python 008: Escreva um programa que leia um valor em metros e o exiba convertido em centímetros e milímetros.
value = int(input('enter the value in meters to converter in cm and ml: '))
cm = value*100
ml = value*1000
print('The value {} in cm is: {} and ml is: {}' .format(value, cm, ml))
