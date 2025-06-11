from Pilha import pilha
from Pedido import Pedido

class Estoque:
    def init(self):
        self.matriz = [[pilha() for _ in range(5)] for _ in range(8)]
        
    def adicionar_engradado(self, engradado):
        for i, linha in enumerate(self.matriz):
            for j, pilha in enumerate(linha):
                if pilha.adicionar(engradado):
                    print(f"Engradado adicionado na posição [{i}][{j}]")
                    return True
        return False
    
    
    
    def remover_engradado(self, produto_codigo, quantidade):
        retirados = []  # Lista de tuplas (engradado, pilha_original)

        for linha in self.matriz:
            for pilha in linha:
                while pilha.topo() and pilha.topo().produto_codigo == produto_codigo and quantidade > 0:
                    retirado = pilha.remover()
                    if retirado:
                        retirados.append((retirado, pilha))
                        quantidade -= retirado.quantidade

        if quantidade <= 0:
            # Sucesso: retorna só os engradados, não as pilhas
            return [item[0] for item in retirados]
        else:
            # Falha: devolve os engradados às pilhas de origem (rollback) checagem de retirada de um engradado
            for engradado, pilha in reversed(retirados):
                pilha.adicionar(engradado)
            return None
        
        
        
    def visualizar(self):
        for i, linha in enumerate(self.matriz):
            print(f"Linha {i}:")
            for j, pilha in enumerate(linha):
                topo = pilha.topo()
                if topo:
                    print(f"  Coluna {j}: {topo.produto_codigo} x {len(pilha.engradados)}")
                else:
                    print(f"  Coluna {j}: Vazia")
                    
                    

    def contar_por_produto(self, produto_codigo):
        total = 0
        for linha in self.matriz:
            for pilha in linha:
                for eng in pilha.engradados:
                    if eng.produto_codigo == produto_codigo:
                        total += eng.quantidade
        return total