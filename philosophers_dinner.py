import threading
import time

class Filosofo():
    def __init__(self, ID):
        self.ID = ID
        self.state = 'pensando'
        self.refeicoes = 0
        
    def set_state(self, state):
        self.state = state
    
    def inc_refeicoes(self):
        self.refeicoes += 1
    
    def get_state(self):
        return self.state
    
    def get_refeicoes(self):
        return self.refeicoes
    
mutex = threading.Lock()

def jantar(i, filosofo:Filosofo):
    while filosofo.get_refeicoes() < 5:
        filosofo.set_state('faminto')
        
        mutex.acquire()
        filosofo.set_state('comendo')
        filosofo.inc_refeicoes()
        print(f'Filosofo {i} comeu')
        mutex.release()
        
        filosofo.set_state('pensando')
        
        
        time.sleep(5)

filosofos = [Filosofo(id) for id in range(1,6)]

for i, filosofo in enumerate(filosofos):
    threading.Thread(target=jantar, args=(i, filosofo)).start()