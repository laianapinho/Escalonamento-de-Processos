from tarefa import Tarefa
from fcfs import executar_fcfs
from sjf import executar_sjf
from rr import executar_rr
from srtf import executar_srtf
from priop import executar_priop
from prioc import executar_prioc

def ler_tarefas_de_arquivo(nome_arquivo):
    tarefas = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip() == "":
                continue  # pula a linha vazia
            dados = linha.strip().split()
            nome = dados[0]
            tempoIngresso = int(dados[1])
            duracao = int(dados[2])
            prioridade = int(dados[3])
            tipo = int(dados[4])
            tarefas.append(Tarefa(nome, tempoIngresso, duracao, prioridade, tipo))
    return tarefas

# Leitura das tarefas do arquivo
arquivo = input("Digite o nome do arquivo: ")
tarefas = ler_tarefas_de_arquivo(arquivo)

# CPU-bound
tarefas_cpu_bound = [tarefa for tarefa in tarefas if tarefa.tipo == 1]
if tarefas_cpu_bound:
    a = int(input("\nCPU-bound: Qual algoritmo deseja executar?\n1 - FCFS\n2 - SJF\nEscolha: "))
    if a == 1:
        print("\n== Executando FCFS para CPU-bound ==")
        executar_fcfs(tarefas_cpu_bound)
    elif a == 2:
        print("\n== Executando SJF para CPU-bound ==")
        executar_sjf(tarefas_cpu_bound)
    else:
        print("Opção inválida para CPU-bound.")
else:
    print("\nNenhuma tarefa do tipo CPU-bound encontrada.")

# I/O-bound
tarefas_io_bound = [tarefa for tarefa in tarefas if tarefa.tipo == 2]
if tarefas_io_bound:
    b = int(input("\nI/O-bound: Qual algoritmo deseja executar?\n3 - SRTF\n4 - Prioridade Cooperativa\nEscolha: "))
    if b == 3:
        print("\n== Executando SRTF para I/O-bound ==")
        executar_srtf(tarefas_io_bound)
    elif b == 4:
        print("\n== Executando Prioridade Cooperativa para I/O-bound ==")
        executar_prioc(tarefas_io_bound)
    else:
        print("Opção inválida para I/O-bound.")
else:
    print("\nNenhuma tarefa do tipo I/O-bound encontrada.")

# Ambos
tarefas_ambos_bound = [tarefa for tarefa in tarefas if tarefa.tipo == 3]
if tarefas_ambos_bound:
    c = int(input("\nAMBOS-bound: Qual algoritmo deseja executar?\n5 - Round Robin\n6 - Prioridade Preemptiva\nEscolha: "))
    if c == 5:
        print("\n== Executando RR para AMBOS-bound ==")
        executar_rr(tarefas_ambos_bound)
    elif c == 6:
        print("\n== Executando Priop para AMBOS-bound ==")
        executar_priop(tarefas_ambos_bound)
    else:
        print("Opção inválida para AMBOS-bound.")
else:
    print("\nNenhuma tarefa do tipo AMBOS-bound encontrada.")
