import random as rm
import flowshop as fl

def criar_populacao_inicial( tamanho_pop, n_tarefa):
    tarefas_inical = list(range(n_tarefa))
    populacao = []
    for _ in range(tamanho_pop):
        tarefasNovas = tarefas_inical.copy()
        rm.shuffle(tarefasNovas)
        populacao.append(tarefasNovas)
    return populacao


def  calcular_fitness(individuo, tempos, matriz_cache):
    
    makespan = fl.calcular_makespan(tempos, individuo, matriz_cache)
    fitness = 1.0 / (makespan + 1e-9)
    return (fitness,makespan)

def selecao_por_torneio(populacao, fitness, tamanho_torneio):
        melhor_fitness = -1
        melhor_individuo = None
        tamanho_populacao = len(populacao)

        for _ in range(tamanho_torneio):
            indice_competidor = rm.randint(0, tamanho_populacao - 1)
            fitness_competidor = fitness[indice_competidor]

            if fitness_competidor > melhor_fitness:

                melhor_fitness = fitness_competidor
                melhor_individuo = populacao[indice_competidor]

        return melhor_individuo


def crossover_ox(pai1, pai2):
    num_tarefas = len(pai1)
    
    corte2 = rm.randint(1, num_tarefas - 1)
    corte1 = rm.randint(0, corte2)

    bloco = pai1[corte1:corte2 + 1]

    filho = [None] * num_tarefas
    filho[corte1:corte2 + 1] = bloco
    
    restantes = []
    for q in pai2:
        if q not in bloco:
            restantes.append(q)

    idx_restantes = 0
    idx_filho = (corte2 + 1) % num_tarefas 

    for _ in range(len(restantes)):
        while filho[idx_filho] is not None:
            idx_filho = (idx_filho + 1) % num_tarefas

        filho[idx_filho] = restantes[idx_restantes]

        idx_restantes += 1
        idx_filho = (idx_filho + 1) % num_tarefas

    return filho 
   
def mutacao(individuo,taxaMutacao=1):
    if rm.random() < taxaMutacao:
        sorteio1,sorteio2 = rm.sample(range(len(individuo)), 2)
        individuo[sorteio1], individuo[sorteio2] = individuo[sorteio2], individuo[sorteio1]
    
    return individuo

