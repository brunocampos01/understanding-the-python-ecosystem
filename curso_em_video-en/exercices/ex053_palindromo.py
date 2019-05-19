"""
Exercise Python 053:

Crie um programa que leia uma frase qualquer
e diga se ela é um palíndromo, desconsiderando os espaços.
"""
inversePhrase = ''
words = phrase.split()
print(words)
joinWords = ''.join(words)
print(joinWords)
numberLetter = len(joinWords)
print('The number letters this phrase is: {}'.format(numberLetter))

# Begins with the last letter and decreases until the first
for numberLetter in range(numberLetter - 1, -1, -1):
    inversePhrase = inversePhrase + joinWords[numberLetter]

if inversePhrase == joinWords:
    print('Its palindrome')
else:
    print(inversePhrase)

# Other way
inversePhrase = joinWords[::-1]
print(inversePhrase)
