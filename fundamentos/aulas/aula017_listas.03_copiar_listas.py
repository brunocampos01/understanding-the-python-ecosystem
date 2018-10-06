'''NOTE: When one list is matched to another in Python, when modifying one, the other is also modified together.'''
a = [2, 3, 4, 7]
b = a  # Cria uma lista "b" idêntica à lista "a", tornando-as intrinsecamente ligadas
b[2] = 8
print(f'Lista A: {a}')
print(f'Lista B: {b}')

print('')

"""
Para criar duas listas com itens idênticos, porém que sejam independentes entre si, ao invés de fazer:
a = [2, 3, 4, 7]
b = a
Se faz:
a = [2, 3, 4, 7]
b = a[:]
"""

c = [1, 2, 3, 4]
d = c[:]  # Cria uma lista "d" com os mesmos elementos da lista "c", deixando cada uma independente
d[3] = 5
print(f'Lista C: {c}')
print(f'Lista D: {d}')