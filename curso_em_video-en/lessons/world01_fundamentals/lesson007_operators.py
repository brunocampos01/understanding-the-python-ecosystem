# Arithmetic Operators
print(5 + 2)  # Adição
print(5 - 2)  # Subtração
print(5 * 2)  # Multiplicação
print(5 / 2)  # Divisão
print(5 ** 2)  # Potência/Exponenciação - Método 1
print(pow(5, 2))  # Potência/Exponenciação - Método 2
print(5 // 2)  # Divisão Inteira
print(5 % 2)  # Resto da Divisão
print(81 ** (1 / 2))  # Raiz Quadrada

"""
Order of Precedence (Which is taken into account first in the Python code):
#1 () - Parênteses
#2 ** - Potência/Exponenciação
#3 *, /, // e % - Multiplicação, Divisão, Divisão Inteira e Resto da Divisão
 (O que aparecer primeiro no código, executa primeiro)
#4 + e - - Adição e Subtração 
(O que aparecer primeiro no código, executa primeiro)
"""
print(5 + 3 * 2)  # Primeiro se resolve a Multiplicação, depois a Adição
print(3 * 5 + 4 ** 2)  # Primeiro se resolve a Exponenciação, depois a Multiplicação, e por fim a Adição
print(3 * (5 + 4) ** 2)  # 1º: Parênteses; 2º: Exponenciação; 3: Multiplicação

# Different Uses of Arithmetic Operators
print('Oi' * 5)  # Exibe a palavra "Oi" 5 vezes
print('=' * 20)  # Exibe o sinal de "=" 20 vezes

# Customizations in the Masks Within the Strings
nome = input('Qual é o seu nome? ')
print('Prazer em te conhecer, {}!'
      .format(nome))  # Exibe normalmente o valor inserido no input da variável "nome"
print('Prazer em te conhecer, {:20}!'
      .format(nome))  # Exibe o valor inserido com 20 caracteres
print('Prazer em te conhecer, {:>20}!'
      .format(nome))  # Exibe o valor inserido com 20 caracteres e alinhado à direita
print('Prazer em te conhecer, {:<20}!'
      .format(nome))  # Exibe o valor inserido com 20 caracteres e alinhado à esquerda
print('Prazer em te conhecer, {:^20}!'
      .format(nome))  # Exibe o valor inserido com 20 caracteres e alinhado no centro
print('Prazer em te conhecer, {:*^20}!'.format(nome))
""" Exibe o valor inserido com 20 caracteres, alinhado no centro
e com o sinal de "*" preenchendo os espaços vazios """

# Customizations in Print Syntax
n1 = int(input('Digite um número: '))
n2 = int(input('Digite outro número: '))
s = n1 + n2
m = n1 * n2
d = n1 / n2
di = n1 // n2
e = n1 ** n2
print('A soma é {}, o produto é {} e a divisão é {}'
      .format(s, m, d))  # Exibe os resultados normalmente
print('A soma é {}, o produto é {} e a divisão é {:.3f}'
      .format(s, m, d))
""" Exibe o resultado da divisão com 3 casas decimais """
print('A soma é {}, o produto é {} e a divisão é {}'
      .format(s, m, d), end=' ')
""" Exibe o resultado sem quebrar a linha, dando um espaço ao invés disso """
print('A soma é {}, o produto é {} e a divisão é {}'
      .format(s, m, d), end=' >>> ')
""" Exibe o resultado sem quebrar a linha, dando um ">>>" ao invés disso """
print('A soma é {}, \no produto é {} \ne a divisão é {}'
      .format(s, m, d))
""" Exibe o resultado com duas quebras de linha no meio do print """
print('Divisão inteira {} e potência {}'
      .format(di, e))
