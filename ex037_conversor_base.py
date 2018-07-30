#Exercício Python 037: Escreva um programa em Python que leia um número inteiro qualquer
#  e peça para o usuário escolher qual será a base de conversão:
# 1 para binário, 2 para octal e 3 para hexadecimal.
number = int(input('Enter the number integer: '))
choose = int(input('''Choose a base to conversion:
[1] converter to binary
[2] converter to octal
[3] converter to hexadecimal
Your choose: '''))

if choose == 1:
    binary = str(bin(number))
    print('{} converted to binary is {}' .format(number, binary[2:]))
elif choose == 2:
    octal = str(oct(number))
    print('{} converted to octal is {}' .format(number, octal[2:]))
elif choose == 3:
    hexadecimal = str(hex(number))
    print('{} converted to hexadecimal {}' .format(number, hexadecimal[2:]))
else:
    print("XXX wrong choice XXX")
