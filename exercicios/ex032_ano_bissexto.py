#Exercício Python 032: Faça um programa que leia um ano qualquer e mostre se ele é bissexto.

from datetime import date
year = int(input('What the year analyse? Input 0 to analyse year current '))
if year == 0:
    year = date.today().year
if year%4 == 0 and year%100 != 0 and year%400 != 0:
    #\033[0;33;44m cores no terminal
    print("{} is lead" .format(year))
else:
    print("{} Dont lead".format(year))