'''Exercício Python 043: Desenvolva uma lógica que leia o peso e a altura de uma pessoa,
 calcule seu Índice de Massa Corporal (IMC) e mostre seu status, de acordo com a tabela abaixo:
- IMC abaixo de 18,5: Abaixo do Peso
- Entre 18,5 e 25: Peso Ideal
- 25 até 30: Sobrepeso
- 30 até 40: Obesidade
- Acima de 40: Obesidade Mórbida'''

weight = float(input('Type with your weight (kg):'))
height = float(input('Type with your height(m): '))
imc = weight/(height**2)
print('The IMC is: {:.1f}'.format(imc))

if(imc < 18.5):
    print('Under weight')
elif 18.5 <= imc <= 25:
    print('OK')
elif 25 < imc >= 30:
    print('Overweight')
elif 30 < imc <= 40:
    print('Obesity')
else:
    print('morbid obesity')
