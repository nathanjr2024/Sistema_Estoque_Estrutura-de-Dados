from collections import deque
from Pilha import Pilha

class FilaPedidos:
    
    def __init__(self):
        self.fila = deque()
        
    def adicionar_pedido(self, pedido):
        self.fila.append(pedido)
        
    def processar_pedido(self, estoque):
        if self.fila:
            pedido = self.fila.popleft()
            retirados = estoque.remover_engradado(pedido.codigo_produto, pedido.quantidade)
            if retirados is not None:
                print(f"Pedido de {pedido.solicitante} atendido!")
                return True
            
            else:
                print(f"produto insuficiente para atender pedido de {pedido.solicitante}.")
                
                return False
        return None