'''Exercício Python 077: Crie um programa que tenha uma tupla com várias palavras (não usar acentos).
Depois disso, você deve mostrar, para cada palavra, quais são as suas vogais.'''

words = ('course', 'programmer', 'language', 'market', 'python')
for w in words:
    print('\nIn word {} have: '.format(w.upper()), end=' ')
    for letter in w:
        if letter in 'aeiou':
            print('{}'.format(letter), end=' ')
