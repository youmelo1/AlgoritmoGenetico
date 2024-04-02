import random
import math
from matplotlib import pyplot as plt
import numpy as np

berlim = {
1: (565.0, 575.0),
2: (25.0, 185.0),
3: (345.0, 750.0),
4: (945.0, 685.0),
5: (845.0, 655.0),
6: (880.0, 660.0),
7: (25.0, 230.0),
8: (525.0, 1000.0),
9: (580.0, 1175.0),
10: (650.0, 1130.0),
11: (1605.0, 620.0),
12: (1220.0, 580.0),
13: (1465.0, 200.0),
14: (1530.0, 5.0),
15: (845.0, 680.0),
16: (725.0, 370.0),
17: (145.0, 665.0),
18: (415.0, 635.0),
19: (510.0, 875.0),
20: (560.0, 365.0),
21: (300.0, 465.0),
22: (520.0, 585.0),
23: (480.0, 415.0),
24: (835.0, 625.0),
25: (975.0, 580.0),
26: (1215.0, 245.0),
27: (1320.0, 315.0),
28: (1250.0, 400.0),
29: (660.0, 180.0),
30: (410.0, 250.0),
31: (420.0, 555.0),
32: (575.0, 665.0),
33: (1150.0, 1160.0),
34: (700.0, 580.0),
35: (685.0, 595.0),
36: (685.0, 610.0),
37: (770.0, 610.0),
38: (795.0, 645.0),
39: (720.0, 635.0),
40: (760.0, 650.0),
41: (475.0, 960.0),
42: (95.0, 260.0),
43: (875.0, 920.0),
44: (700.0, 500.0),
45: (555.0, 815.0),
46: (830.0, 485.0),
47: (1170.0, 65.0),
48: (830.0, 610.0),
49: (605.0, 625.0),
50: (595.0, 360.0),
51: (1340.0, 725.0),
52: (1740.0, 245.0)
}


def criarRotas(cidades, tamanhoPopulacao):
    listaRotas = []

    for i in range(tamanhoPopulacao):
        
        idsCidade = random.sample(list(cidades), k=len(cidades))

        
        rota = [cidades[i] for i in idsCidade]

        
        listaRotas.append(rota)

    return listaRotas


def distanciaEuclidiana(cidadeIda, cidadeChegada):
    #calcula distancia euclidiana = √((x2-x1)^2 + (y2-y1)^2)
    x1,y1 = cidadeIda
    x2,y2 = cidadeChegada
    return math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    
def distanciaDaRota(rota):
    distancia = 0

    #soma a distancia euclidiana da rota
    for i in range(len(rota)):

        #se i for o destino final, para o loop
        if i+1==len(rota):
            break
        distancia += distanciaEuclidiana(rota[i], rota[i+1])
    
    #como precisamos voltar ao ponto incial, é preciso fazer a distancia euclidiana entre
    #a cidade final e a cidade inicial
    distancia += distanciaEuclidiana(rota[len(rota)-1], rota[0])

    return distancia


def fitness(rota):
    #calcula o fitness da rota

    distancia = distanciaDaRota(rota)

    fitness = 1/distancia

    return fitness


def selecaoRoleta(rotas, quantidadeElite):
    selecionados = []

    rotas.sort(reverse = True, key=fitness)

    for i in range(quantidadeElite):
        selecionados.append(rotas[i])

    somaFitness = sum([fitness(rota) for rota in rotas])
    probabilidades = [fitness(rota)/somaFitness for rota in rotas]

    for i in range(len(rotas)-quantidadeElite):
        indexEscolhido = np.random.choice(len(rotas), p=probabilidades)
        selecionados.append(rotas[indexEscolhido])

    return selecionados


def selecaoTorneio(rotas,quantidadeElite):
    selecionados = []

    rotas.sort(reverse = True, key=fitness)

    for i in range(quantidadeElite):
        selecionados.append(rotas[i])

    for i in range(len(rotas)-quantidadeElite):
        #tamanhoTorneio = random.randint(1, len(rotas)-1)
        torneio = random.sample(rotas, 10)
        vencedor = max(torneio, key=fitness)
        selecionados.append(vencedor)
    
    return selecionados

def cruzamentoPontoUnico(pai1, pai2):
    filho = []
    influenciaPai1 = []
    influenciaPai2 = []
    
    ponto = int(random.random() * len(pai1))
    
    for i in range(ponto, len(pai1)):
        influenciaPai1.append(pai1[i])
        
    
    influenciaPai2 = [gene for gene in pai2 if gene not in influenciaPai1]

    filho = influenciaPai1 + influenciaPai2
    return filho

def cruzamentoUniforme(pai1, pai2):
    filho  = []
    for i in range(len(pai1)):
        rand =  int(random.uniform(0,2))
        if rand == 0:
            if pai1[i] not in filho:
                filho.append(pai1[i])
            else:
                for item  in pai1:
                    if item not in filho:
                        filho.append(item)
                        break
        else:
            if pai2[i] not in filho:
                filho.append(pai2[i])
            else:
                for item  in pai2:
                    if item not in filho:
                        filho.append(item)
                        break    
                


    return filho


def cruzarPop(selecionados, quantidadeElite, metodoCruzamento):
    listaCriancas = []
    amostra = random.sample(selecionados, len(selecionados))

    for i in range(0, quantidadeElite):
        listaCriancas.append(selecionados[i])


    ponteiroEsquerdo = 0
    ponteiroDireito = len(selecionados)-1

    for i in range(0, len(selecionados)-quantidadeElite):
        crianca = metodoCruzamento(amostra[ponteiroEsquerdo], amostra[ponteiroDireito])
        ponteiroEsquerdo += 1
        ponteiroDireito -= 1
        listaCriancas.append(crianca)


    return listaCriancas

def mutacaoInsercao(rota, taxaMutacao):  
    if random.uniform(0,1) >= taxaMutacao:
        return rota
     
    index1, index2 = random.sample(range(len(rota)), 2)
    removed_element = rota.pop(index1)
    if index2 > index1:
        rota.insert(index2 - 1, removed_element)
    else:
        rota.insert(index2, removed_element)

    return rota

def mutacaoTroca(rota, taxaMutacao):
    if random.uniform(0,1) >= taxaMutacao:
        return rota     
        
    gene1 = random.randint(0,len(rota)-1)
    gene2 = random.randint(0,len(rota)-1)

    rota[gene1], rota[gene2] = rota[gene2], rota[gene1]

    return rota

def aplicarMutacao(populacao, taxaMutacao, metodoMutacao):
    listaRotas = []
    
    for i in range(0, len(populacao)):
        rota = metodoMutacao(populacao[i], taxaMutacao)
        listaRotas.append(rota)
    return listaRotas

def gerarProximaGeracao(geraaoAtual, quantidadeElite, taxaMutacao, metodoSelecao, metodoCruzamento, metodoMutacao):
    selecionados = metodoSelecao(geraaoAtual, quantidadeElite)
    filhos = cruzarPop(selecionados, quantidadeElite, metodoCruzamento)
    proximaGeracao = aplicarMutacao(filhos, taxaMutacao, metodoMutacao)
    return proximaGeracao


def indiceDicionario(dicionario, valor):
    for chave, val in dicionario.items():
        if val == valor:
            return chave


def algoritmoGenetico(populacao, tamanhoPopulacao, quantidadeElite, taxaMutacao, metodoSelecao, metodoCruzamento, metodoMutacao, distancia):
    pop = criarRotas(populacao, tamanhoPopulacao)
    print('Distancia inicial:', distanciaDaRota(pop[0]))
    progresso = []
    progresso.append(distanciaDaRota(pop[0]))
    geracoes = 0

    while distancia<distanciaDaRota(pop[0]):
        pop = gerarProximaGeracao(pop, quantidadeElite, taxaMutacao, metodoSelecao, metodoCruzamento, metodoMutacao)
        progresso.append(distanciaDaRota(pop[0]))
        geracoes+=1

    pop.sort(reverse = True, key=fitness)
    print('Distancia final:', distanciaDaRota(pop[0]))
    print('Gerações criadas: ',geracoes)

    melhorRota = []
    for i in range(len(pop[0])):
        melhorRota.append(indiceDicionario(populacao, pop[0][i]))
    melhorRota.append(melhorRota[0])

    print('Melhor rota: ',melhorRota)
    plt.plot(progresso)
    plt.ylabel('Distância')
    plt.xlabel('Geração')
    plt.show()

    return geracoes

algoritmoGenetico(berlim, 400, 40, 0.01, selecaoTorneio, cruzamentoPontoUnico, mutacaoInsercao, distancia= 10000)


def torneioVSselecao():
    geracoesTorneio = 0
    
    geracoesRoleta = 0
    

    i = 0
    j = 0

    while i<10:
        geracoesTorneio += algoritmoGenetico(berlim, 200, 20, 0.01, selecaoTorneio, cruzamentoPontoUnico, mutacaoInsercao, 9000)
        i+=1 
    while j<10:
        geracoesRoleta += algoritmoGenetico(berlim, 200, 20, 0.01, selecaoRoleta, cruzamentoPontoUnico, mutacaoInsercao, 9000)
        j+=1


    print('Média de gerações do torneio: ', geracoesTorneio/i)
    
    print('-----------------------------------------------------')
    print('Média de gerações da roleta: ', geracoesRoleta/i)
    
