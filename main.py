import numpy as np
import matplotlib.pyplot as plt
import requests
import random as rm

import flowshop as fl
import algoritimo_genetico as ga

TAMANHO_POP = 200         # Indivíduos por geração
N_GERACOES = 1000         # Número de ciclos de evolução
TAXA_CROSSOVER = 0.85     # cruzamento
TAXA_MUTACAO = 0.2
TAMANHO_TORNEIO = 5     
INSTANCIA_NOME = "car8" 


print("--- Carregando Problema ---")
try:
    url = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop1.txt"
    response = requests.get(url)
    response.raise_for_status()
    flowshop_instances = fl.parse_all_flowshop_instances_from_text(response.text)
except requests.exceptions.RequestException as e:
    print(f"Falha ao baixar instâncias: {e}")
    exit()

inst = flowshop_instances[INSTANCIA_NOME]
n_tarefas = inst["n_jobs"]
n_maquinas = inst["n_machines"]

tempos_processamento = np.array(inst["processing_times"]).T

print(f"Resolvendo Instância: '{INSTANCIA_NOME}' ({n_tarefas} Tarefas, {n_maquinas} Máquinas)")

# matriz de reutilização
matriz_cache_makespan = np.zeros((n_maquinas, n_tarefas), dtype=int)

populacao = ga.criar_populacao_inicial(TAMANHO_POP, n_tarefas)

melhor_individuo_global = None
melhor_makespan_global = float('inf') #valor nulo
historico_melhor_makespan = []


# Evolução
for geracao in range(N_GERACOES):

    fitness_da_geracao = []
    makespans_da_geracao = []
    for individuo in populacao:
        fitness, makespan = ga.calcular_fitness(
            individuo,
            tempos_processamento,
            matriz_cache_makespan
        )
        fitness_da_geracao.append(fitness)
        makespans_da_geracao.append(makespan)

    # geração atual melhor que global
    melhor_makespan_geracao = min(makespans_da_geracao)
    if melhor_makespan_geracao < melhor_makespan_global:
        melhor_makespan_global = melhor_makespan_geracao
        indice_melhor_geracao = np.argmin(makespans_da_geracao)
        melhor_individuo_global = populacao[indice_melhor_geracao].copy()
        
    # melhor makespan
    historico_melhor_makespan.append(melhor_makespan_global)

    nova_populacao = []

    # guardar melhor solução
    nova_populacao.append(melhor_individuo_global.copy())

    # nova população
    while len(nova_populacao) < TAMANHO_POP:

        pai1 = ga.selecao_por_torneio(populacao, fitness_da_geracao, TAMANHO_TORNEIO)
        pai2 = ga.selecao_por_torneio(populacao, fitness_da_geracao, TAMANHO_TORNEIO)
        
        # crossover
        if rm.random() < TAXA_CROSSOVER:
            filho = ga.crossover_ox(pai1, pai2)
        else:
            filho = pai1.copy()
        
        # mutação
        filho_mutado = ga.mutacao(filho.copy(), TAXA_MUTACAO)
        
        nova_populacao.append(filho_mutado)

    populacao = nova_populacao


# grafico
print("\n--- Resultados Finais ---")
print(f"Melhor Solução (Permutação): {melhor_individuo_global}")
print(f"Melhor Makespan Encontrado: {melhor_makespan_global}")

fl.calcular_makespan(
    tempos_processamento, 
    melhor_individuo_global, 
    matriz_cache_makespan
)
dados_gantt_final = fl.matriz_para_gantt_permutacao_zero(
    matriz_cache_makespan,
    tempos_processamento,
    melhor_individuo_global
)
fl.gantt_matplotlib(dados_gantt_final)
plt.show()