import json
import os
from time import sleep

project_root = os.path.dirname(os.path.abspath(__file__))
process_file_path = os.path.join(project_root, 'processos.json')

def load_process_from_json(file_path):
    
    with open(file_path, 'r') as file:
        processes = json.load(file).get('processes', [])

    processed_data = []
        
    for process in processes:
        
        processed_process = {
            'id': process.get('id'),
            'name': process.get('name'),
            'arrival': process.get('arrival'),
            'execution': process.get('execution')
        }
        processed_data.append(processed_process)
       
    return processed_data


def round_robin_scheduling(processes, quantum = 2, time_unit = 0, print_logs = True):
    time = 0
    queue = processes.copy()
    completed_processes = []

    if print_logs:
        print("Inicializando Round Robin Scheduling")
        print(f"Quantum definido: {quantum} unidades de tempo")
        print(f"Unidade de tempo para simulação: {time_unit} segundos")

    while queue:
        process = queue.pop(0)
        
        if print_logs:
            print(f"Processando: {process['name']} (ID: {process['id']}) - Time: {time}")
        
        if 'start' not in process:
                process['start'] = time
        
        if process['execution'] > quantum:
            time += quantum
            
            sleep(quantum * time_unit)  # Simula o tempo de execução
            
            process['execution'] -= quantum
            queue.append(process)
        else:
            time += process['execution']
            
            sleep(process['execution'] * time_unit)  # Simula o tempo de execução
            
            process['execution'] = 0
            process['completion_time'] = time
            completed_processes.append(process)
            
            if print_logs:
                print(f"Processo {process['name']} (ID: {process['id']}) concluído em tempo {time}")
                    
    return completed_processes

if __name__ == "__main__":
    processes = load_process_from_json(process_file_path)
    print_logs = True  # Defina como False para desativar os logs
    quantum = 2  # Defina o quantum desejado
    time_unit = 0.5  # Define o tempo de simulação para cada unidade de tempo
    
    execution_order = [p['name'] for p in processes]

    print("Ordem de execução dos processos:", execution_order)

    completed_processes = round_robin_scheduling(processes, quantum, time_unit, print_logs)
    
    for process in completed_processes:
        print(f"Processo {process['name']} (ID: {process['id']}) possui tempo de resposta {process['start'] - process['arrival']}") 

    average_response_time = sum(p['start'] - p['arrival'] for p in completed_processes) / len(completed_processes)

    print(f"Tempo médio de resposta dos processos: {average_response_time}")

    print("Ordem dos processos concluídos:", [p['name'] for p in completed_processes])

