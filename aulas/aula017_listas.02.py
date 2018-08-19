"""É possível começar uma lista vazia "valores" assim:
valores = []
Ou
valores = list()"""

valores = []
valores = list()

valores = list(range(4, 11))  # Cria uma lista "valores" com os números de 4 até 10 (o último número, 11, é ignorado)
print(valores)

if False:
    for v in valores:  # Para cada item "v" na lista "valores"...
        print(f'{v}...', end=' ')

    for c, v in enumerate(valores):  # Para cada índice "c" e item "v" na lista "valores"...
        print(f'Na posição {c} encontrei o valor {v}!')
    print('Cheguei ao final da lista.')