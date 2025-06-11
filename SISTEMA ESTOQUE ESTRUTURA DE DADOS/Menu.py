# Arquivo: Menu.py
import json
from Produto import Produto, carregar_produtos, salvar_produtos
from Engradado import Engradado
from Estoque import Estoque  # Importa a classe Estoque
from Fila_de_Pedidos import FilaPedidos
from Pedido import Pedido

# --- Inicialização do Sistema ---
# Carrega os produtos existentes do arquivo JSON
produtos_cadastrados = carregar_produtos('produtos.json') #
# Cria uma instância única do Estoque e da Fila de Pedidos
estoque = Estoque()
fila_pedidos = FilaPedidos()

# --- Funções do Menu Refatoradas ---

def cadastrar_novo_produto():
    """Função dedicada a cadastrar um novo tipo de produto no sistema."""
    print("\n--- Cadastro de Novo Produto ---")
    codigo = input("Código: ")
    
    # Verifica se o código do produto já existe
    if any(p.codigo == codigo for p in produtos_cadastrados):
        print("Erro: Já existe um produto com este código.")
        return

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

    novo_produto = Produto(
        codigo, lote, nome, peso, data_validade, data_fabricacao,
        preco_compra, preco_venda, fornecedor, fabricante, categoria
    )
    produtos_cadastrados.append(novo_produto)
    salvar_produtos(produtos_cadastrados, 'produtos.json') #
    print(f"\nProduto '{nome}' cadastrado com sucesso!")

def adicionar_engradado_estoque():
    """Adiciona um engradado de um produto já cadastrado ao estoque."""
    print("\n--- Adicionar Engradado ao Estoque ---")
    codigo_produto = input("Código do produto: ")

    # Verifica se o produto existe
    if not any(p.codigo == codigo_produto for p in produtos_cadastrados):
        print("Erro: Nenhum produto encontrado com este código. Cadastre o produto primeiro.")
        return
        
    try:
        quantidade = int(input("Quantidade de itens no engradado: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return

    engradado = Engradado(codigo_produto, quantidade)

    if estoque.adicionar_engradado(engradado): #
        print("\nEngradado adicionado ao estoque com sucesso.")
    else:
        print("\nErro: Estoque cheio ou nenhuma pilha compatível encontrada.")

def remover_unidades_estoque():
    """Remove uma quantidade específica de um produto do estoque manualmente."""
    print("\n--- Remover Unidades do Estoque ---")
    codigo = input("Código do produto para remover: ")
    
    try:
        quantidade = int(input("Quantidade a remover: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return

    # Utiliza o método da classe Estoque que possui lógica de rollback
    engradados_removidos = estoque.remover_engradado(codigo, quantidade) #

    if engradados_removidos is not None:
        print(f"\nRemoção concluída com sucesso.")
    else:
        print("\nNão foi possível remover a quantidade desejada (estoque insuficiente ou produto não encontrado).")

def visualizar_estoque():
    """Exibe o estado atual do estoque."""
    print("\n--- Visualização do Estoque ---")
    estoque.visualizar() #

def registrar_pedido():
    """Registra um novo pedido de cliente na fila."""
    print("\n--- Registrar Novo Pedido ---")
    codigo_produto = input("Código do produto: ")
    
    # Verifica se o produto existe
    if not any(p.codigo == codigo_produto for p in produtos_cadastrados):
        print("Erro: Nenhum produto encontrado com este código.")
        return

    try:
        quantidade = int(input("Quantidade desejada: "))
        if quantidade <= 0:
            print("A quantidade deve ser um número positivo.")
            return
    except ValueError:
        print("Erro: Quantidade inválida.")
        return
        
    data_solicitacao = input("Data da solicitação (YYYY-MM-DD): ")
    solicitante = input("Nome do solicitante: ")

    try:
        pedido = Pedido(codigo_produto, quantidade, data_solicitacao, solicitante) #
        fila_pedidos.adicionar_pedido(pedido) #
        print("\nPedido registrado com sucesso.")
    except ValueError as e:
        print(f"Erro ao registrar o pedido: {e}. Verifique o formato da data.")


def processar_pedidos():
    """Processa o próximo pedido da fila."""
    print("\n--- Processando Pedido ---")
    if not fila_pedidos.fila:
        print("Não há pedidos na fila para processar.")
        return
    
    # A fila_pedidos.processar_pedido agora usa a instância real de Estoque
    fila_pedidos.processar_pedido(estoque) #

def gerar_relatorios():
    """Gera e exibe relatórios sobre o estoque."""
    print("\n--- Relatório de Estoque por Produto ---")
    if not produtos_cadastrados:
        print("Nenhum produto cadastrado.")
        return
        
    for produto in produtos_cadastrados:
        total_unidades = estoque.contar_por_produto(produto.codigo) #
        print(f"Produto: {produto.nome} (Cód: {produto.codigo}) - Total em Estoque: {total_unidades} unidades")

def menu():
    """Função principal que exibe o menu e gerencia as opções."""
    while True:
        print("\n=========== MENU DO SISTEMA DE ESTOQUE ===========")
        print("1. Cadastrar Novo Produto")
        print("2. Adicionar Engradado ao Estoque")
        print("3. Remover Unidades do Estoque")
        print("4. Visualizar Estoque")
        print("5. Registrar Pedido de Cliente")
        print("6. Processar Próximo Pedido da Fila")
        print("7. Gerar Relatório de Estoque")
        print("8. Salvar Alterações nos Produtos")
        print("0. Sair")
        print("==================================================")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_novo_produto()
        elif opcao == '2':
            adicionar_engradado_estoque()
        elif opcao == '3':
            remover_unidades_estoque()
        elif opcao == '4':
            visualizar_estoque()
        elif opcao == '5':
            registrar_pedido()
        elif opcao == '6':
            processar_pedidos()
        elif opcao == '7':
            gerar_relatorios()
        elif opcao == '8':
            salvar_produtos(produtos_cadastrados, 'produtos.json') #
            print("\nAlterações nos dados dos produtos salvas com sucesso!")
        elif opcao == '0':
            salvar_produtos(produtos_cadastrados, 'produtos.json')
            print("\nAlterações salvas. Saindo do sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()