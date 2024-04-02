import random
import numpy as np
import matplotlib.pyplot as plt

listaFitness = []

def problema(x, y, z):
    return (7*2*x*4)**1/2 + 9*y**-27 + 31*z-1

def fitness(x, y, z):
    

    ans = problema(x, y, z)

    

    if ans == 0:
        return 99999
    else:
        listaFitness.append(abs(1/ans))
        return abs(1/ans)




    

#gerar solucoes
solucoes = []
for s in range(1000):
    solucoes.append( (random.uniform(0,10000),
                      random.uniform(0, 10000),
                      random.uniform(0, 10000)) )

geracoes = 0

for geracoes in range(100000):

    solucoesRankeadas = []
    for s in solucoes:
        solucoesRankeadas.append( (fitness(s[0], s[1], s[2]), s) )
    
    solucoesRankeadas.sort()
    solucoesRankeadas.reverse()

    print(f"=== Geracao {geracoes} melhores solucoes ===")
    print(solucoesRankeadas[0])


    if problema(solucoesRankeadas[0][1][0],solucoesRankeadas[0][1][1],solucoesRankeadas[0][1][2]) <0.0001 and problema(solucoesRankeadas[0][1][0],solucoesRankeadas[0][1][1],solucoesRankeadas[0][1][2])>=0 :
        break

    melhoresSolucoes = solucoesRankeadas[:100]

    elemento_x = []
    elemento_y = []
    elemento_z = []

    for s in melhoresSolucoes:
        elemento_x.append(s[1][0])
        elemento_y.append(s[1][1])
        elemento_z.append(s[1][2])

    novaGeracao = []
    for _ in range(1000):
        eX = random.choice(elemento_x) * random.uniform(0.99, 1.01)
        eY = random.choice(elemento_y) * random.uniform(0.99, 1.01)
        eZ = random.choice(elemento_z) * random.uniform(0.99, 1.01)

        novaGeracao.append( (eX, eY, eZ) )
        solucoes = novaGeracao