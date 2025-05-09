from tarefa import Tarefa 
from collections import deque  

tarefas = [] 

# Função que lê tarefas de um arquivo e as armazena em uma lista
def ler_tarefas_de_arquivo(nome_arquivo):
    tarefas = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                continue  # Ignora linhas vazias
            dados = linha.strip().split()  
            nome = dados[0]
            tempoIngresso = int(dados[1])
            duracao = int(dados[2])
            prioridade = int(dados[3])
            tipo = int(dados[4])  # Tipo de escalonamento (não usado aqui)
            tarefas.append(Tarefa(nome, tempoIngresso, duracao, prioridade, tipo))
    return tarefas

def executar_prioc(tarefas):
    tempoAtual = 0  
    somaTempoEspera = 0  
    somaTempoExecucao = 0  
    tempo_espera = {tarefa.nome : 0  for tarefa in tarefas}  # Dicionário para tempo de espera de cada tarefa
    tempo_inicio_execucao = {}  # Armazena o tempo de início da execução de cada processo
    tempo_fim_execucao = {}  # Armazena o tempo de término da execução de cada processo
    total_tarefas = len(tarefas)  # Número total de tarefas
    fila_prontos = deque()  # Fila de processos prontos para execução
    tarefas_restantes = tarefas.copy()  # Tarefas que ainda não chegaram
    processo_em_execucao = None  # Processo atualmente executando
    ordem_execucao = []  # Guarda a ordem de execução dos processos

    # Loop principal do escalonador
    while tarefas_restantes or fila_prontos or processo_em_execucao:
        # Verifica se novas tarefas chegaram no tempo atual
        for tarefa in list(tarefas_restantes):
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)  # Vai para fila de prontos
                tarefas_restantes.remove(tarefa)

        # Se não há processo em execução e há processos prontos
        if not processo_em_execucao and fila_prontos:
            # Seleciona o processo com maior prioridade (maior número)
            maior = max(fila_prontos, key=lambda tarefa: tarefa.prioridade)
            fila_prontos.remove(maior)
            processo_em_execucao = maior

            # Registra o tempo em que começou a executar
            if processo_em_execucao.nome not in tempo_inicio_execucao:
                tempo_inicio_execucao[processo_em_execucao.nome] = tempoAtual
                ordem_execucao.append((processo_em_execucao.nome, tempoAtual))

            # Executa todo o processo de uma vez (não preemptivo)
            tempoAtual += processo_em_execucao.duracao
            tempo_fim_execucao[processo_em_execucao.nome] = tempoAtual
            processo_em_execucao = None  # Processo finalizado

        # Caso não tenha nada a executar, avança o tempo
        elif not fila_prontos and tarefas_restantes:
            tempoAtual += 1

    # Após a execução de todas as tarefas, calcula os tempos
    for tarefa in tarefas:
        nome = tarefa.nome
        # Tempo de espera = início da execução - chegada
        tempo_espera[nome] = tempo_inicio_execucao[nome] - tarefa.tempoIngresso
        somaTempoEspera += tempo_espera[nome]
        # Turnaround = término - chegada
        tempo_execucao = tempo_fim_execucao[nome] - tarefa.tempoIngresso
        somaTempoExecucao += tempo_execucao

    # Cálculo dos tempos médios
    tempomedioexecucao = somaTempoExecucao / total_tarefas
    tempomedioespera = somaTempoEspera / total_tarefas

    # Impressão dos resultados
    print("\nOrdem de execução:")
    for nome, tempo in ordem_execucao:
        print(f"{nome} executado no tempo {tempo}")

    print("Tempo Médio de Execução", tempomedioexecucao)
    print("Tempo Médio de Espera", tempomedioespera)
