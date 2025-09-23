import threading
import time
import random
import os
from threading import Event, Lock

class CorridaCavalos:
    def __init__(self, num_cavalos=5, distancia_meta=50):
        self.num_cavalos = num_cavalos
        self.distancia_meta = distancia_meta
        self.cavalos = {}
        self.posicoes = {}
        self.vencedor = None
        self.corrida_finalizada = False
        
        # Sincronização
        self.largada = Event()  # Para largada sincronizada
        self.lock_placar = Lock()  # Exclusão mútua para atualização do placar
        self.lock_vencedor = Lock()  # Exclusão mútua para registro do vencedor
        
        # Controle de exibição
        self.lock_display = Lock()
        
        # Inicializar cavalos
        for i in range(num_cavalos):
            nome_cavalo = f"Cavalo {i+1}"
            self.cavalos[nome_cavalo] = 0
            self.posicoes[nome_cavalo] = 0
    
    def cavalo_correndo(self, nome_cavalo):
        """Função executada por cada thread (cavalo)"""
        # Aguardar largada sincronizada
        self.largada.wait()
        
        while not self.corrida_finalizada:
            # Passo aleatório (1 a 3 posições)
            passo = random.randint(1, 3)
            
            # Atualizar posição com exclusão mútua
            with self.lock_placar:
                if not self.corrida_finalizada:
                    self.posicoes[nome_cavalo] += passo
                    
                    # Verificar se cruzou a linha de chegada
                    if self.posicoes[nome_cavalo] >= self.distancia_meta:
                        self.posicoes[nome_cavalo] = self.distancia_meta
                        
                        # Registrar vencedor de forma determinística
                        with self.lock_vencedor:
                            if self.vencedor is None:
                                self.vencedor = nome_cavalo
                                self.corrida_finalizada = True
            
            # Pausa pequena para visualização
            time.sleep(0.1)
    
    def exibir_placar(self):
        """Exibe o placar atual da corrida"""
        with self.lock_display:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CORRIDA DE CAVALOS")
            print("-" * 40)
            
            # Ordenar cavalos por posição (para resolver empates de forma determinística)
            cavalos_ordenados = sorted(self.posicoes.items(), 
                                     key=lambda x: (-x[1], x[0]))  # Por posição desc, depois por nome
            
            for nome, posicao in cavalos_ordenados:
                # Criar barra de progresso simples
                progresso = int((posicao / self.distancia_meta) * 20)
                barra = "█" * progresso + "░" * (20 - progresso)
                
                print(f"{nome}: [{barra}] {posicao}/{self.distancia_meta}")
            
            print("-" * 40)
            if self.corrida_finalizada and self.vencedor:
                print(f"VENCEDOR: {self.vencedor}!")
    
    def obter_aposta(self):
        """Solicita aposta do usuário"""
        print("BEM-VINDO À CORRIDA DE CAVALOS!")
        print("\nCavalos participantes:")
        for i in range(self.num_cavalos):
            print(f"{i+1}. Cavalo {i+1}")
        
        while True:
            try:
                aposta = input(f"\nEm qual cavalo apostar? (1-{self.num_cavalos}): ")
                numero_cavalo = int(aposta)
                if 1 <= numero_cavalo <= self.num_cavalos:
                    return f"Cavalo {numero_cavalo}"
                else:
                    print(f"Escolha entre 1 e {self.num_cavalos}")
            except ValueError:
                print("Digite um número válido")
    
    def iniciar_corrida(self):
        """Inicia a corrida com largada sincronizada"""
        # Obter aposta do usuário
        aposta_usuario = self.obter_aposta()
        print(f"\nVocê apostou no {aposta_usuario}!")
        
        # Criar e iniciar threads dos cavalos
        threads = []
        for nome_cavalo in self.cavalos.keys():
            thread = threading.Thread(target=self.cavalo_correndo, args=(nome_cavalo,))
            threads.append(thread)
            thread.start()
        
        # Contagem regressiva para largada
        print("\nPreparando largada...")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("LARGADA!\n")
        
        # Sinalizar largada sincronizada
        self.largada.set()
        
        # Loop de exibição do placar
        while not self.corrida_finalizada:
            self.exibir_placar()
            time.sleep(0.2)
        
        # Exibir resultado final
        self.exibir_placar()
        
        # Aguardar todas as threads terminarem
        for thread in threads:
            thread.join()
        
        # Anunciar resultado da aposta
        print(f"\nSUA APOSTA: {aposta_usuario}")
        if aposta_usuario == self.vencedor:
            print("VOCÊ GANHOU!")
        else:
            print(f"Você perdeu. Vencedor: {self.vencedor}")
        
        return self.vencedor, aposta_usuario

def main():
    """Função principal"""
    print("Configuração da Corrida:")
    
    # Configurações da corrida
    try:
        num_cavalos = int(input("Número de cavalos (padrão 5): ") or "5")
        distancia = int(input("Distância da corrida (padrão 50): ") or "50")
    except ValueError:
        print("Usando valores padrão...")
        num_cavalos = 5
        distancia = 50
    
    # Criar e executar corrida
    corrida = CorridaCavalos(num_cavalos, distancia)
    vencedor, aposta = corrida.iniciar_corrida()
    
    # Opção para nova corrida
    print(f"\nRESULTADO FINAL:")
    print(f"Vencedor: {vencedor}")
    print(f"Sua aposta: {aposta}")
    print(f"{'ACERTOU!' if vencedor == aposta else 'ERROU!'}")
    
    nova_corrida = input("\nNova corrida? (s/n): ").lower()
    if nova_corrida == 's':
        main()

if __name__ == "__main__":
    # Configurar random seed para demonstração
    random.seed()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCorrida interrompida!")
    except Exception as e:
        print(f"\nErro: {e}")
