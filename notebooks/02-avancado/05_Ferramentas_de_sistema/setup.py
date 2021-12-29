import sys

def args():
    print(sys.argv)
    
def install():
    print("Instalando tudo!")
    
def text(text):
    print(text)
    
def sum(x, y):
    return x + y
    
def pipe():
    n = sys.stdin.read()
    print("O sentido da vida é", n)
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--install':
            install()
        elif sys.argv[1] == '--args':
            args()
        elif sys.argv[1] == '--pipe':
            pipe()
        elif sys.argv[1] == '--text':
            text(sys.argv[2])
        elif sys.argv[1] == '--sum':
            sum(sys.argv[2], sys.argv[3])