#Exercício Python 026: Faça um programa que leia uma frase pelo teclado e mostre
# quantas vezes aparece a letra "A", em que posição ela aparece a primeira vez e em
# que posição ela aparece a última vez.
phrase = input('Enter with phrase: ')
phrase = phrase.strip()
countLetterA = phrase.count('a')
print('The letter "a" appeared: {} times in the phrase' .format(countLetterA))
print('The first letter "a" appeared in the position {}' .format(phrase.find('a')))
print('The last letter "a" appered in position {}' .format(phrase.rfind('a')))