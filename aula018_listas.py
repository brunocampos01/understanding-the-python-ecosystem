listaIntera = list()
galera = list()

listaIntera.append('gustavo')
listaIntera.append(40)
#eh preciso [:] para criar uma copia senao os dados sempre ficam ligados
galera.append(listaIntera[:])

listaIntera[0] = 'maria'
listaIntera[1] = 12
galera.append(listaIntera[:])
print(galera)


galeral = [['maria'], ['selva'], ['zorao'], ['cabelho']]
for p in galeral:
    print(p)
