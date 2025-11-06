# Algoritmo Genético para o Problema de Flowshop

Este projeto implementa um Algoritmo Genético (GA) em Python para resolver o problema de agendamento *Flowshop* de Permutação (PFSP) com o objetivo de minimizar o *makespan*.

O algoritmo foi testado nas instâncias de benchmark de Taillard (ex: "car1", "car8"), encontrando os valores ótimos conhecidos.

## Estrutura do Projeto

* `main.py`: executa o GA.
* `genetic_algorithm.py`: Contém a lógica do "motor" do GA (Seleção, Crossover OX, Mutação).
* `flowshop.py`: Contém a lógica de definição do problema.
* `requirements.txt`: Dependências do projeto.

## Como Executar

1.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute o `main.py`:
    ```bash
    python main.py
    ```