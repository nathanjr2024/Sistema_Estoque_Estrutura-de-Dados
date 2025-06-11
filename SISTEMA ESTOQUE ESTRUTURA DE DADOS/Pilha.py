from Engradado import Engradado

class Pilha:
    def __init__(self):
        self.engradados = []

    def adicionar(self , engradado):
        if len(self.engradados) < 5:
            if not self.engradados or self.engradados[-1].produto_codigo == engradado.produto_codigo:
                self.engradados.append(engradado)
                return True
            return False
    
    def remover(self):
        if self.engradados:
            return self.engradados.pop()
        return None

    def topo(self):
        if self.engradados:
            return self.engradados[-1]
        
    def esta_vazia(self):
        return len(self.engradados) == 0