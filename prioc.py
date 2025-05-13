from tarefa import Tarefa 
from collections import deque  

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
            tipo = int(dados[4])  
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

    while tarefas_restantes or fila_prontos or processo_em_execucao:
        # Adiciona tarefas que chegaram ao tempo atual
        for tarefa in list(tarefas_restantes):
            if tarefa.tempoIngresso <= tempoAtual:
                fila_prontos.append(tarefa)
                tarefas_restantes.remove(tarefa)

        # Se não há processo em execução, escolhe o de maior prioridade (menor número)
        if not processo_em_execucao and fila_prontos:
            mais_prioritaria = min(fila_prontos, key=lambda tarefa: tarefa.prioridade)  # 🟢 CORREÇÃO AQUI
            fila_prontos.remove(mais_prioritaria)
            processo_em_execucao = mais_prioritaria

            if processo_em_execucao.nome not in tempo_inicio_execucao:
                tempo_inicio_execucao[processo_em_execucao.nome] = tempoAtual
                ordem_execucao.append((processo_em_execucao.nome, tempoAtual))

            # Executa o processo completamente (não preemptivo)
            tempoAtual += processo_em_execucao.duracao
            tempo_fim_execucao[processo_em_execucao.nome] = tempoAtual
            processo_em_execucao = None

        elif not fila_prontos and tarefas_restantes:
            # Avança o tempo se nada está pronto
            tempoAtual += 1

    # Cálculo dos tempos
    for tarefa in tarefas:
        nome = tarefa.nome
        tempo_espera[nome] = tempo_inicio_execucao[nome] - tarefa.tempoIngresso
        somaTempoEspera += tempo_espera[nome]
        tempo_execucao = tempo_fim_execucao[nome] - tarefa.tempoIngresso
        somaTempoExecucao += tempo_execucao

    tempomedioexecucao = somaTempoExecucao / total_tarefas
    tempomedioespera = somaTempoEspera / total_tarefas

    # Resultados
    print("\nOrdem de execução:")
    for nome, tempo in ordem_execucao:
        print(f"{nome} executado no tempo {tempo}")

    print("Tempo Médio de Execução:", tempomedioexecucao)
    print("Tempo Médio de Espera:", tempomedioespera)
