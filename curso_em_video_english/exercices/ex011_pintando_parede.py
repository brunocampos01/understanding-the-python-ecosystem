#Exercício Python 011: Faça um programa que leia a largura e a altura de uma parede em metros,
# calcule a sua área e a quantidade de tinta necessária para pintá-la,
# sabendo que cada litro de tinta pinta uma área de 2 metros quadrados.
width = float(input('enter the width: '))
height = float(input('enter the height: '))
area = width*height
ink = area/2
print('For paint the wall {}m2 X {}m2, you need of {}l ink.' .format(width, height, ink))