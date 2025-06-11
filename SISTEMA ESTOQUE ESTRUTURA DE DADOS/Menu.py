import json
from Produto import *
from Engradado import Engradado
from Pilha import Pilha
from Fila_de_Pedidos import FilaPedidos
from Pedido import Pedido

produtos_cadastrados = carregar_produtos('produtos.json')


# Simulação de Estoque (Matriz 5x8 de Pilhas)
estoque = [[Pilha() for _ in range(5)] for _ in range(8)]
fila_pedidos = FilaPedidos()

def adicionar_produto():
    codigo = input("Código: ")
    lote = input("Lote: ")
    nome = input("Nome: ")
    peso = float(input("Peso: "))
    data_validade = input("Data de validade (YYYY-MM-DD): ")
    data_fabricacao = input("Data de fabricação (YYYY-MM-DD): ")
    preco_compra = float(input("Preço de compra: "))
    preco_venda = float(input("Preço de venda: "))
    fornecedor = input("Fornecedor: ")
    fabricante = input("Fabricante: ")
    categoria = input("Categoria: ")

    produto = Produto(
        codigo, lote, nome, peso, data_validade, data_fabricacao,
        preco_compra, preco_venda, fornecedor, fabricante, categoria
    )
    produtos_cadastrados.append(produto)
    salvar_produtos(produtos_cadastrados, 'produtos.json')



    engradado = Engradado(produto.codigo, quantidade=int(input("Quantidade no engradado: ")))

    # Inserção simplificada: sempre na primeira pilha livre
    for linha in estoque:
        for pilha in linha:
            if len(pilha.engradados) < 5:
                if pilha.adicionar(engradado):
                    print("Engradado adicionado ao estoque.")
                    
                    return
    print("Estoque cheio. Não foi possível adicionar.")
    

def remover_produto():
    codigo = input("Código do produto para remover: ")
    quantidade = int(input("Quantidade a remover: "))

    for linha in estoque:
        for pilha in linha:
            if not pilha.esta_vazia():
                topo = pilha.topo()
                if topo and topo.produto_codigo == codigo:
                    while quantidade > 0 and not pilha.esta_vazia():
                        pilha.remover()
                        quantidade -= 1
                    if quantidade == 0:
                        print("Produto removido com sucesso.")
                        return
    print("Não foi possível remover a quantidade desejada.")

def visualizar_estoque():
    for i, linha in enumerate(estoque):
        for j, pilha in enumerate(linha):
            print(f"Posição [{i}][{j}] - {len(pilha.engradados)} engradados")

def registrar_pedido():
    codigo_produto = input("Código do produto: ")
    quantidade = int(input("Quantidade: "))
    data_solicitacao = input("Data da solicitação (YYYY-MM-DD): ")
    solicitante = input("Nome do solicitante: ")

    pedido = Pedido(codigo_produto, quantidade, data_solicitacao, solicitante)
    fila_pedidos.adicionar_pedido(pedido)
    print("Pedido registrado com sucesso.")

def processar_pedidos():
    while fila_pedidos.fila:
        fila_pedidos.processar_pedido(EstoqueSimulado())

class EstoqueSimulado:
    """Classe de Estoque simulada para processar pedidos"""
    def remover_engradado(self, codigo, quantidade):
        removidos = 0
        for linha in estoque:
            for pilha in linha:
                if not pilha.esta_vazia():
                    topo = pilha.topo()
                    if topo and topo.produto_codigo == codigo:
                        while quantidade > 0 and not pilha.esta_vazia():
                            pilha.remover()
                            quantidade -= 1
                            removidos += 1
                        if quantidade == 0:
                            return removidos
        return None

def gerar_relatorios():
    print("Relatório de estoque:")
    visualizar_estoque()
    # Aqui pode implementar recursivamente relatórios de vencimento, falta, etc.

def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Adicionar Produto ao Estoque")
        print("2. Remover Produto do Estoque")
        print("3. Visualizar Estoque")
        print("4. Registrar Pedido")
        print("5. Processar Pedidos")
        print("6. Gerar Relatórios")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_produto()
        elif opcao == '2':
            remover_produto()
        elif opcao == '3':
            visualizar_estoque()
        elif opcao == '4':
            registrar_pedido()
        elif opcao == '5':
            processar_pedidos()
        elif opcao == '6':
            gerar_relatorios()
        elif opcao == '7':
            salvar_produtos(produtos_cadastrados, 'produtos.json')
            print("Produtos salvos com sucesso!")
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()