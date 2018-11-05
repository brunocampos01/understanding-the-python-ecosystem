"""
NOTE 1: Every method has "()" (opens and closes parentheses) at the end.
For example, in "car. Follow ()", "car" is the object and "follow ()" is the method.
NOTE 2: All exercises and challenges to date have used Sequential Structures.
From now on, the Conditional Structures will be presented.
NOTE 3: Side spacing before the commands within a Conditional Framework is called Indentation.
An indentation can be created by pressing the "Tab" key (2 keys below the "Esc").
NOTE 4: In a simple conditional structure of "if" and "minus", the "if" command block is
executed if the condition is true (True), while the "snag" command block is
executed if the condition is false (False).

Simple Conditional Example:
if <CONDIÇÃO>:
    <COMANDOS>

Compound Conditional Example:
if <CONDIÇÃO>:
    <COMANDOS A>
else:
    <COMANDOS B>
Simplified Conditional Example:
print('Frase a exibir se a condição se cumprir' if <CONDIÇÃO> else 'Frase a exibir se a condição não se cumprir')

Example of Nested Conditional Structure:
if <CONDIÇÃO 1>:
    <COMANDOS A>
elif <CONDIÇÃO 2>:
    <COMANDOS B>
elif <CONDIÇÃO 3>:
    <COMANDOS C>
else:
    <COMANDOS D>"""
tempo = int(input('Quantos anos tem seu carro? '))  # Atribui à variável "tempo" o valor de um número inteiro
if tempo <= 3:  # Se a variável "tempo" receber um valor igual ou menor do que 3...
    print('Carro novo!')  # Exibe "Carro novo!"
else:  # Senão...
    print('Carro velho!')  # Exibe "Carro velho!"
print('--- FIM ---')  # Exibe "--- FIM ---" independemente do resultado da condição acima
