import threading
import time
import random

NUM_THREADS = 3
T = 2
DURACAO = 8
locks = [threading.Lock() for _ in range(2)]

ultima_atividade = time.time()
atividade_lock = threading.Lock()
alertas = 0

def watchdog(situacao):
    global ultima_atividade, alertas
    start_time = time.time()
    while time.time() - start_time < DURACAO:
        time.sleep(T)
        with atividade_lock:
            delta = time.time() - ultima_atividade
        if delta > T:
            alertas += 1
            print(f"[WATCHDOG - {situacao}] Possível deadlock detectado! Sem progresso por {delta:.2f}s")

def thread_risco_deadlock(id_thread):
    global ultima_atividade
    start_time = time.time()
    while time.time() - start_time < DURACAO:

        first, second = (0, 1) if id_thread % 2 == 0 else (1, 0)
        print(f"Thread {id_thread} tentando lock {first}")
        with locks[first]:
            with atividade_lock:
                ultima_atividade = time.time()
            time.sleep(random.uniform(0.1, 0.5))
            print(f"Thread {id_thread} tentando lock {second}")
            with locks[second]:
                with atividade_lock:
                    ultima_atividade = time.time()
                print(f"Thread {id_thread} conseguiu ambos os locks")
                time.sleep(random.uniform(0.1, 0.3))

def thread_sem_deadlock(id_thread):
    global ultima_atividade
    start_time = time.time()
    while time.time() - start_time < DURACAO:

        for i in range(len(locks)):
            print(f"Thread {id_thread} tentando lock {i}")
            with locks[i]:
                with atividade_lock:
                    ultima_atividade = time.time()
                time.sleep(random.uniform(0.1, 0.3))
        print(f"Thread {id_thread} conseguiu todos os locks")
        time.sleep(random.uniform(0.1, 0.3))

def rodar_cenario(nome_cenario, func_thread):
    global ultima_atividade, alertas
    ultima_atividade = time.time()
    alertas = 0
    
    print(f"\n--- INICIANDO CENÁRIO: {nome_cenario} ---\n")
    
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=func_thread, args=(i,), daemon=True)
        threads.append(t)
        t.start()
    
    wd = threading.Thread(target=watchdog, args=(nome_cenario,), daemon=True)
    wd.start()
    
    time.sleep(DURACAO)
    
    print(f"\n--- FIM DO CENÁRIO: {nome_cenario} ---")
    print(f"[{nome_cenario}] Alertas do watchdog: {alertas}\n")
    return alertas

alertas_deadlock = rodar_cenario("Risco de Deadlock", thread_risco_deadlock)
alertas_ordenado = rodar_cenario("Ordem Total de Locks", thread_sem_deadlock)

print("=== COMPARAÇÃO FINAL ===")
print(f"Alertas do watchdog - Risco de Deadlock: {alertas_deadlock}")
print(f"Alertas do watchdog - Ordem Total de Locks: {alertas_ordenado}")

