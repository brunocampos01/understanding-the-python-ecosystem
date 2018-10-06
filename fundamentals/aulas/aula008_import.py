"""
import <NOME DO MÓDULO> | Importa tudo contido no módulo
from <NOME DO MÓDULO> import <NOME DA FUNÇÃO> | Importa uma função específica do módulo
from <NOME DO MÓDULO> import <NOME DA FUNÇÃO 1>, <NOME DA FUNÇÃO 2> | Importa duas ou mais funções específicas do módulo
Exemplos:
import math
from math import sqrt
from math import sqrt, ceil
Algumas Funções do Módulo math:
ceil - Arredonda o valor para cima
floor - Arredonda o valor para baixo
trunc
pow
sqrt
factorial
Ctrl + Espaço após digitar "from <NOME DO MÓDULO> import" ou somente "import" no PyCharm, lista todas as funções
ou módulos possíveis para importar
Ao tentar importar Módulos/Bibliotecas que não estão diretamente integrada ao Python, no PyCharm, ao fazer
isso, uma lampadinha vermelha será exibida logo ao lado. Clicando sobre ela, é possível escolher a opção
para instalar tal Módulo/Biblioteca se ela existir no banco de dados do PyPI (Python Package Index).
Para ver quais Módulos/Bibliotecas extras estão instalados, no PyCharm (Windows 10), ir em:
File > Settings... > Project: NomeDoProjeto > Project Interpreter
Também é possível adicionar ou remover Módulos/Bibliotecas rapidamente,
clicando nos botões de "+" e de "-", respectivamente
Relação de Módulos/Bibliotecas Integradas Disponíveis: https://docs.python.org/3/library/index.html
Módulos/Bibliotecas Extras: https://pypi.python.org/pypi
"""
from math import sqrt, floor, ceil
num = int(input('Digite um número: '))
raiz = sqrt(num)
print('A raiz de {} é igual a {}.'.format(num, raiz))
print('A raiz de {} arredondada para baixo é igual a {}.'.format(num, floor(raiz)))
print('A raiz de {} arredondada para cima é igual a {}.'.format(num, ceil(raiz)))

import random  # Importa o Módulo random com todas as suas funções
num1 = random.random()  # Atribui à variável "num1" um valor aleatório float entre 0 e 1
num2 = random.randint(1, 10)  # Atribui à variável "num2" um valor aleatório int entre 1 e 10
print(num1, num2)  # Exibe os valores gerados

import emoji
print(emoji.emojize('Olá, Mundo :earth_americas:!', use_aliases=True))