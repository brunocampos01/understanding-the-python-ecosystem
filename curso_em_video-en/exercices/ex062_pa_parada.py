#Exercício Python 062: Melhore o DESAFIO 061, perguntando para o usuário se ele quer mostrar mais alguns termos.
# O programa encerrará quando ele disser que quer mostrar 0 termos.
print('\narithmetic progress generator\n')
first = int(input('Type fisrt term: '))
ratio = int(input('Type a rate: '))
element = first
count = 1
total = 0
moreElement = 10

while moreElement != 0:
    total = total + moreElement
    while count <= total:
        print('{}'.format(element), end=' -> ')
        element += ratio
        count += 1
    print('PAUSE')
    moreElement = int(input('More elements? type 0 to exit '))
print('Arithmetic progress with {} elements.'.format(total))
