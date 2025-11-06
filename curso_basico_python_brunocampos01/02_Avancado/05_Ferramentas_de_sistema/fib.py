import argparse
import sys


def fibonacci(input_number):
    previous, next = 0, 1
    for number in range(input_number):
        previous, next = next, previous + next
        
    return previous


def execute(parser):
    """
    Executa a sequência de finobacci com o argumento passado,
    além de vários outros argumentos opcionais e o -h que é o help
    """
    
    # Adiciona o argumento number da sequência de fibonacci
    parser.add_argument(
        "number",
        help="Número da sequência de Fibonacci que se deseja obter",
        type=int
    )
    
    # Adiciona o argumento opcional para escrever em arquivos
    parser.add_argument(
        "-o",
        "--output",
        help="Mandar a saída do programa para um arquivo separado",
        action="store"
    )
    
    # Cria um grupo de argumentos mutuamente exclusivo
    group = parser.add_mutually_exclusive_group()
    
    # Adicionamos um modo de saída do tipo verbose ou quiet ao grupo
    # logo o usuário é obrigado a escolhar um mode específico de saída
    group.add_argument(
        "-v",
        "--verbose",
        help="Imprime a saída no modo verbose",
        action="store_true"
    )
    group.add_argument(
        "-q",
        "--quiet",
        help="Imprime a saída no modo quiet",
        action="store_true"
    )
    
    # Pegamos os argumentos colocados na linha de comando
    args = parser.parse_args()
    
    # Obtemos o resultado
    result = fibonacci(args.number)
    
    # Armazenar o resultado no arquivo inserido pelo usuário
    if args.output != None:
        file = open(args.output, 'a')
        sys.stdout = file
    
    # Imprimir na tela o resultado
    if args.verbose:
        print("O", args.number, "valor da sequência de fibonacci é", result)
    elif args.quiet:
        print(result)
    else:
        print("Fibonacci(" + str(args.number) + ") =", result)

    
def main():
    # Primeiros vamos criar o objeto que irá lidar com o argumento
    parser = argparse.ArgumentParser(description="Exemplo de Argparse")
    
    # Argumentos que serão passados como parâmetros
    execute(parser)

if __name__ == '__main__':
    main()