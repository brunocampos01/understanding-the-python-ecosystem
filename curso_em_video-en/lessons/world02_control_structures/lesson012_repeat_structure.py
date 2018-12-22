"""Repetition structure with Logic Test
NOTE:
Use the for when the loop has a predefined number of repetitions. Otherwise, use the while."""

if False:
    #for
    for c in range(1, 11):
        print(c)
    print('end')

    # while
    c = 1
    while c < 11:
        print(c)
        c += 1
    print('end')

if False:
    n = 1
    while n != 0:  # Flag/Condição de Parada
        n = int(input('Digite um valor: '))
    print('FIM 2')

if False:
    r = 'S'
    while r == 'S':
        n = int(input('Digite um valor: '))
        r = str(input('Quer continuar [S/N]? ')).upper()
    print('FIM 3')

#Infinite Repetition Structure
if False:
    # loop infinito
    n = s = 0
    while True:
        n = int(input('Digite um número: '))
        if n == 999:
            break
        s += n
    print('A soma vale {}.'.format(s))
    print('FIM 4')
