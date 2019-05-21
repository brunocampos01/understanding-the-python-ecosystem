"""
import <NOME DO MÓDULO> | Importa tudo contido no módulo

from <NOME DO MÓDULO> import <NOME DA FUNÇÃO>
| Importa uma função específica do módulo

from <NOME DO MÓDULO> import <NOME DA FUNÇÃO 1>, <NOME DA FUNÇÃO 2>
 | Importa duas ou mais funções específicas do módulo
"""
from math import sqrt, floor, ceil


num = int(input('Digite um número: '))
raiz = sqrt(num)

print('A raiz de {} é igual a {}.'.format(num, raiz))
print('A raiz de {} arredondada para baixo é igual a {}.'
      .format(num, floor(raiz)))
print('A raiz de {} arredondada para cima é igual a {}.'
      .format(num, ceil(raiz)))

##############################################################
import secrets  # Importa o Módulo random SECRETS com todas as suas funções


num1 = secrets.randbelow(6)  # Atribui à variável "num1" um valor aleatório float entre 0 e 1
num2 = secrets.randbelow(6)  # Atribui à variável "num2" um valor aleatório int entre 1 e 10
print(num1, num2)  # Exibe os valores gerados

##############################################################
import emoji


print(emoji.emojize('Olá, Mundo :earth_americas:!', use_aliases=True))
