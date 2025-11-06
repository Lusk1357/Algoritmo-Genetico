import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import CSS4_COLORS, to_rgb


def parse_all_flowshop_instances_from_text(text):
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    instances = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lower().startswith(" instance"):
            try:
                name = line.split()[1] 
                description = lines[i + 2]
                n_jobs, n_machines = map(int, lines[i + 3].split())
                processing_times = []
                for j in range(n_jobs):
                    parts = lines[i + 4 + j].split()
                    times = [int(parts[k + 1]) for k in range(0, len(parts), 2)]
                    processing_times.append(times)
                instances[name] = {
                    "description": description,
                    "n_jobs": n_jobs,
                    "n_machines": n_machines,
                    "processing_times": processing_times, 
                }
                i += 4 + n_jobs
            except Exception as e:
                i += 1
        else:
            i += 1
    return instances


def calcular_makespan(tempos, permutacao, resultado): 
    n_maquinas, n_tarefas = tempos.shape
    id_tarefa_0 = permutacao[0]
    resultado[0, 0] = tempos[0, id_tarefa_0]

    for i in range(1, n_maquinas):
        resultado[i, 0] = tempos[i, id_tarefa_0] + resultado[i-1, 0]


    for j in range(1, n_tarefas):
        id_tarefa_j = permutacao[j]
        resultado[0, j] = tempos[0, id_tarefa_j] + resultado[0, j-1]
        

    for i in range(1, n_maquinas):
        for j in range(1, n_tarefas):
            id_tarefa_j = permutacao[j]
            
            resultado[i, j] = tempos[i, id_tarefa_j] + max(resultado[i-1, j], resultado[i, j-1])

    makespan_final = resultado[n_maquinas - 1, n_tarefas - 1]

    return makespan_final
    
   
def cor_contraste(cor):
    r, g, b = to_rgb(cor)

    luminancia = 0.299*r + 0.587*g + 0.114*b

    return "black" if luminancia > 0.5 else "white"

def gerar_100_cores():
    cores = list(CSS4_COLORS.keys())
    return cores[:100]  # Pega as 100 primeiras

def matriz_para_gantt_permutacao_zero(tempos_termino, duracoes, numeros_permutacao):
    n_maquinas, n_tarefas = tempos_termino.shape
    dados_gantt = []

    for i in range(n_maquinas):
        atividades = []
        
        for j in range(n_tarefas):
            
            tarefa_real_id = numeros_permutacao[j] 
        
            duracao = duracoes[i, tarefa_real_id]
            
            termino = tempos_termino[i, j]
            
            inicio = termino - duracao
            
            atividades.append((inicio, duracao))

        dados_gantt.append({
            "estagio": f"Máquina {i}",
            "atividades": atividades,
            "numeros": numeros_permutacao 
        })

    return dados_gantt

def gantt_matplotlib(dados, grid=True):
    df = pd.DataFrame(dados)
    cores_base = gerar_100_cores()  
    n = len(df) 
    
    altura_retangulo = 0.6
    fontsize_numero = 9
    
    altura_figura = max(2, n * (altura_retangulo + 0.1))
    fig, ax = plt.subplots(figsize=(12, altura_figura)) 

    for i, row in df.iterrows():
        y_pos = n - 1 - i 
        
        numeros = row.get("numeros", list(range(1, len(row["atividades"]) + 1)))

        for (start, dur), num in zip(row["atividades"], numeros):
            
            cor_caixa = cores_base[(num) % len(cores_base)] 
            
            cor_numero = cor_contraste(cor_caixa)

            ax.broken_barh(
                [(start, dur)], 
                (y_pos - altura_retangulo/2, altura_retangulo), 
                facecolors=cor_caixa,
                edgecolors="black",
                linewidth=1.2
            )

            ax.text(
                start + dur/2, 
                y_pos,         
                str(num),      
                va="center",
                ha="center",
                color=cor_numero,
                fontsize=fontsize_numero,
                weight="bold"
            )

    ax.set_yticks(range(n))
    ax.set_yticklabels(df["estagio"][::-1])
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Máquinas")
    ax.set_title("Diagrama de Gantt - Makespan")

    if grid:
        ax.grid(True, axis="x", linestyle="--", alpha=0.7)
    
    plt.tight_layout()
    plt.show()
