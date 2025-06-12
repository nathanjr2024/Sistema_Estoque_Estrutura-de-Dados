from datetime import datetime
from collections import deque

class Produto:
    # Garanta que o __init__ esteja assim:
    def __init__(self, codigo, lote, nome, peso, data_validade, data_fabricacao, preco_compra, preco_venda, fornecedor, fabricante, categoria, quantidade_por_produto):
        self.codigo = codigo
        self.lote = lote
        self.nome = nome
        self.peso = peso
        self.data_validade = datetime.strptime(data_validade, "%Y-%m-%d")
        self.data_fabricacao = datetime.strptime(data_fabricacao, "%Y-%m-%d")
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria
        self.quantidade_por_produto = quantidade_por_produto 

    
    def para_dicionario(self):
        return {
            'codigo': self.codigo, 'lote': self.lote, 'nome': self.nome, 'peso': self.peso,
            'data_validade': self.data_validade.strftime("%Y-%m-%d"),
            'data_fabricacao': self.data_fabricacao.strftime("%Y-%m-%d"),
            'preco_compra': self.preco_compra, 'preco_venda': self.preco_venda,
            'fornecedor': self.fornecedor, 'fabricante': self.fabricante, 'categoria': self.categoria,
            'quantidade_por_produto': self.quantidade_por_produto 
        }
        
    def __repr__(self):
        return f"Produto(cod={self.codigo}, nome='{self.nome}')"
        
    def __repr__(self):
        return f"Produto(cod={self.codigo}, nome='{self.nome}')"

class Engradado:
    def __init__(self, produto, quantidade, capacidade_maxima):
        if not isinstance(produto, Produto):
            raise TypeError("O engradado só pode conter um objeto do tipo Produto.")
        self.produto = produto
        self.quantidade = quantidade
        self.capacidade_maxima = capacidade_maxima

    def para_dicionario(self):
        return {
            'codigo_produto': self.produto.codigo,
            'quantidade': self.quantidade,
            'capacidade_maxima': self.capacidade_maxima
        }

    def __repr__(self):
        return f"Engradado[{self.produto.nome} ({self.quantidade}/{self.capacidade_maxima})]"

class Pilha:
    CAPACIDADE_MAXIMA = 5

    def __init__(self):
        self._engradados = []

    def para_dicionario(self):
        return [engradado.para_dicionario() for engradado in self._engradados]
        
    def empilhar(self, engradado):
        if self.esta_cheia():
            print("Erro: A pilha de engradados está cheia.")
            return False
        if not self.esta_vazia() and engradado.produto.codigo != self.ver_topo().produto.codigo:
            print(f"Erro: Esta pilha contém '{self.ver_topo().produto.nome}' e não pode receber '{engradado.produto.nome}'.")
            return False
        self._engradados.append(engradado)
        return True

    def desempilhar(self):
        return self._engradados.pop() if not self.esta_vazia() else None

    def ver_topo(self):
        return self._engradados[-1] if not self.esta_vazia() else None

    def esta_vazia(self):
        return len(self._engradados) == 0

    def esta_cheia(self):
        return len(self._engradados) >= self.CAPACIDADE_MAXIMA
        
    def __len__(self):
        return len(self._engradados)
        
    def __repr__(self):
        return f"Pilha com {len(self._engradados)} engradados."

class Fila:
    def __init__(self):
        self._itens = deque()
    def enfileirar(self, item): self._itens.append(item)
    def desenfileirar(self): return self._itens.popleft() if not self.esta_vazia() else None
    def esta_vazia(self): return len(self._itens) == 0
    def __len__(self): return len(self._itens)

class Estoque:
    def __init__(self, linhas=8, colunas=5):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = [[Pilha() for _ in range(colunas)] for _ in range(linhas)]

    def visualizar_estoque(self):
        print("=" * 85)
        print(" " * 30 + "VISUALIZAÇÃO DO ESTOQUE")
        print("=" * 85)
        for i in range(self.linhas):
            for j in range(self.colunas):
                pilha = self.matriz[i][j]
                topo = pilha.ver_topo()
                if topo:
                    print(f"| L{i}C{j}: [{len(pilha)}/5] {topo.produto.nome[:7]:<7}", end=" ")
                else:
                    print(f"| L{i}C{j}: [ 0/5] {'Vazio':<7}", end=" ")
            print("|")
        print("=" * 85)

    def buscar_produto(self, codigo_produto):
        posicoes = []
        for i in range(self.linhas):
            for j in range(self.colunas):
                pilha = self.matriz[i][j]
                if not pilha.esta_vazia() and pilha.ver_topo().produto.codigo == codigo_produto:
                    posicoes.append((i, j))
        return posicoes

class Pedido:
    def __init__(self, solicitante, itens_pedido):
        self.solicitante = solicitante
        self.data_solicitacao = datetime.now()
        self.itens = itens_pedido
        self.atendido = False
    def __repr__(self):
        status = "Atendido" if self.atendido else "Pendente"
        return f"Pedido de '{self.solicitante}' em {self.data_solicitacao.strftime('%d/%m/%Y')} - Status: {status}"