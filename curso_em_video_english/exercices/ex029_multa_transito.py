#Exercício Python 029: Escreva um programa que leia a velocidade de um carro.
# Se ele ultrapassar 80Km/h, mostre uma mensagem dizendo que ele foi multado.
# A multa vai custar R$7,00 por cada Km acima do limite.
speed = int(input('Which speed of the car? '))
if speed>80:
    trafficTicket = (speed-80)*7
    print('FINED! You exceeded the limit permitted of speed the 80Km/h')
    print('You must pay traffic ticket of: {}' .format(trafficTicket))
else:
    print('OK')
print('Have a nice day :)' )


