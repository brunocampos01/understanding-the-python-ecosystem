'''Le nome + media 2 alunos. No final exibe conteudo estruturado na tela'''

classroom = []
students = {}

#add elements in dict
for count in range(0, 2):
    students['name'] = str(input('Name: '))
    students['media'] = int(input('AVG: '))
    classroom.append(students.copy())

#print dict
for index in classroom: #list
    for key, value in index.items(): #dict
        print(f'{key} = {value}')

print(classroom)