# slicing string
if False:
    frase = 'Curso em Vídeo Python'

    print(frase)  # Exibe a frase inteira
    print(frase[9])  # Exibe o caractere de índice [9] na frase, no caso, a letra "V"
    print(frase[9:13])  # Exibe desde o caractere de índice [9] até o [13], porém excluindo este último, ficando "Víde"
    print(frase[9:14])  # Exibe desde o caractere de índice [9] até o [14], porém excluindo este último, ficando "Vídeo"
    print(frase[9:21])  # Apesar de o índice [21] não existir na frase, como o último é excluído, fica "Vídeo Python"
    print(frase[9:21:2])  # Exibe do índice [9] ao [21], pulando de 2 em 2, ficando "VdoPto"
    print(frase[:5])  # Exibe do índice inicial (0, no caso) até o [5] (lembrando: excluindo este), ficando "Curso"
    print(frase[15:])  # Exibe do índice [15] até o final (21, no caso), ficando "Python"
    print(frase[9::3])  # Exibe do índice [9] até o final (21, no caso), pulando de 3 em 3, ficando "VePh"
    print(frase[::2])  # Exibe do índice inicial [0] até o final (21, no caso), pulando de 2 em 2, ficando "Croe íe yhn"

# Strings Analysis
if False:
    frase = 'Curso em Vídeo Python'

    print(len(frase))  # Exibe a quantidade de caracteres de uma string (no caso, 21)
    print(frase.count('o'))
    """ Exibe a quantidade de vezes que o caractere entre parênteses (no caso, "o" minúsculo)
    aparece na string (no caso, 3) """
    print(frase.count('o', 0, 13))
    """ Idem ao caso acima, porém aqui foi incluído um fatiamento do índice [0] ao [13]-1, exibindo "1" """
    print(frase.count('o', 0, 14))  # Idem ao caso acima, porém aqui o índice final ficou sendo [14]-1, exibindo "2"
    print(frase.find('deo'))  # Exibe o índice inicial (11, no caso) do que está entre parênteses
    print(frase.find('Android'))  # Quando se procura na string algo que não está presente, o valor exibido é "-1"
    print('Curso' in frase)  # Verifica se o que está entre aspas está presente na string, e se sim, exibe "True"

# string transformation
if False:
    frase = 'Curso em Vídeo Python'
    frase2 = '   Aprenda Python  '

    print(frase.replace('Python', 'Android'))  # Exibe a string com um termo existente substituído por outro
    print(frase.upper())  # Exibe a string toda em letras maiúsculas
    print(frase.lower())  # Exibe a string toda em letras minúsculas
    print(
        frase.capitalize())  # Exibe a string capitalizada (com apenas o primeiro caractere da frase em letra maiúscula)
    print(frase.title())  # Exibe a string estilo título (com o primeiro caractere de cada palavra em letra maiúscula)
    print(frase)  # A string original não foi alterada permanentemente por nenhum dos comandos utilizados acima

    print('')  # Linha em branco para separar os comandos direcionados a cada string

    print(frase2.strip())  # Remove todos os espaços excedentes da string
    print(frase2.rstrip())  # Remove os espaços excedentes apenas do lado direito da string (inclusão do "r" no comando)
    print(
        frase2.lstrip())  # Remove os espaços excedentes apenas do lado esquerdo da string (inclusão do "l" no comando)
    print(
        frase2)  # Novamente, a string original não foi alterada permanentemente por nenhum dos comandos utilizados acima

    print('')  # Linha em branco

    frase = frase.replace('Python', 'Android')  # Desta forma sim, a string original é substituída permanentemente
    print(frase)  # Exibe a string original já com as modificações feitas acima

# String Split and Join
if False:
    frase = 'Curso em Vídeo Python'
    frase_separada = frase.split()  # Separa cada palavra da string em uma lista; os índices são refeitos
    print(frase_separada)  # Exibe a lista de palavras separadas

    """
    ÍNDICES REFEITOS
    [C] [u] [r] [s] [o]   [e] [m]   [V] [í] [d] [e] [o]   [P] [y] [t] [h] [o] [n]
    [0] [1] [2] [3] [4]   [0] [1]   [0] [1] [2] [3] [4]   [0] [1] [2] [3] [4] [5]
    [        0        ]   [  1  ]   [        2        ]   [          3          ]
    """

    frase_junta_hifen = '-'.join(
        frase_separada)  # Junta as palavras separadas na lista com o caractere "-" como divisor
    print(frase_junta_hifen)  # Exibe a string junta novamente, desta vez com "-" no lugar dos espaços

    frase_junta_espaco = ' '.join(frase_separada)  # Junta as palavras separadas na lista usando um espaço como divisor
    print(frase_junta_espaco)  # Exibe a string junta novamente, com o espaço sendo o divisor, como na origin

# Long Text Print
if False:
    print('''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Cras aliquam sapien non augue pharetra finibus. Integer ac justo quam.
    Pellentesque at eros vel tortor pharetra mollis sit amet convallis sem.
    Cras vel lobortis metus. Donec metus magna, fermentum eget dolor at, egestas dapibus sem.
    Etiam varius, enim ut tincidunt tristique, dui risus tristique quam, id iaculis ipsum sem nec elit.
    Nunc iaculis sit amet diam id lobortis. Nam egestas congue lectus vitae maximus.''')

# manipulation list
if False:
    frase = 'Curso em Vídeo Python'
    frase_dividida = frase.split()  # Atribui à variável "frase_dividida" a lista de palavras contidas em "frase"
    print(frase_dividida[0])  # Exibe a primeira palavra na lista criada acima
    print(frase_dividida[2])  # Exibe a terceira palavra na lista
    print(frase_dividida[3][0])  # Exibe a primeira letra da quarta palavra na lista
    print(frase_dividida[3][0:3])  # Exibe da primeira até a terceira letra da quarta palavra na lista
    print(
        frase_dividida[0][::2])  # Exibe da primeira até a última letra da primeira palavra na lista, pulando de 2 em 2
