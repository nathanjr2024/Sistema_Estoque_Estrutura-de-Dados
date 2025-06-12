import os
from Sistema import SistemaEstoque
from Modelos import Produto



def menu_principal():
    print("\n===== Sistema de Gerenciamento de Estoque =====")
    print("1. Adicionar Engradados ao Estoque")
    print("2. Registrar Novo Pedido na Fila")
    print("3. Processar Próximo Pedido da Fila")
    print("4. Visualizar Estoque Completo")
    print("5. Gerar Relatórios")
    print("6. Cadastrar Novo Produto") 
    print("0. Salvar e Sair")
    return input("Escolha uma opção: ")


def cadastrar_novo_produto_ui(sistema: SistemaEstoque):
    """Interface para coletar dados de um novo produto e solicitar o cadastro."""
    print("\n--- Cadastro de Novo Produto ---")
    try:
        dados_produto = {
            'codigo': input("Código único do produto: "),
            'lote': input("Lote: "),
            'nome': input("Nome do produto: "),
            'peso': float(input("Peso (em kg/unidade): ")),
            'data_validade': input("Data de validade (AAAA-MM-DD): "),
            'data_fabricacao': input("Data de fabricação (AAAA-MM-DD): "),
            'preco_compra': float(input("Preço de compra (R$): ")),
            'preco_venda': float(input("Preço de venda (R$): ")),
            'fornecedor': input("Fornecedor: "),
            'fabricante': input("Fabricante: "),
            'categoria': input("Categoria: "),
            'quantidade_por_produto': int(input("Quantidade do produto por engradado: "))
        }
        # Chama o método do sistema para cadastrar
        sistema.cadastrar_novo_produto(dados_produto)

    except ValueError:
        print("\nERRO: Para peso e preços, utilize apenas números (use '.' para centavos).")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o cadastro: {e}")
    

def iniciar_programa():
    sistema = SistemaEstoque()
    
    if not sistema.produtos_cadastrados:
        print("Cadastrando produtos de exemplo...")
    try:
        
        sistema._salvar_produtos()
        print("Produtos de exemplo cadastrados e salvos.")
    except Exception as e:
        print(f"Erro ao criar produtos de exemplo: {e}")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        opcao = menu_principal()

        try:
            if opcao == '1':
                sistema.estoque.visualizar_estoque()
                cod = input("Digite o código do produto: ")
                qtd = int(input("Digite a quantidade de engradados (serão adicionados até 5 por pilha):\n "))
                l = int(input("Digite a linha para adicionar (0-7): "))
                c = int(input("Digite a coluna para adicionar (0-4): "))
                if 0 <= l <= 7 and 0 <= c <= 4:
                    sistema.adicionar_produto_estoque(cod, qtd, l, c)
                else:
                    print("\nERRO: Posição inválida! A linha deve ser de 0 a 7 e a coluna de 0 a 4.")
                
            elif opcao == '2':
                solicitante = input("Nome do solicitante: ")
                itens = []
                while True:
                    cod = input("Código do produto (ou 'fim' para terminar): ")
                    if cod.lower() == 'fim': break
                    qtd = int(input("Quantidade desejada do produto: "))
                    itens.append({'codigo_produto': cod, 'quantidade': qtd})
                if itens: sistema.registrar_pedido(solicitante, itens)

            elif opcao == '3':
                sistema.processar_proximo_pedido()

            elif opcao == '4':
                sistema.estoque.visualizar_estoque()

            elif opcao == '5':
                sistema.gerar_relatorio_vencimento()
                sistema.gerar_relatorio_historico()
                
            elif opcao == '6':
                cadastrar_novo_produto_ui(sistema)

            elif opcao == '0':
                sistema._salvar_estado_estoque()
                print("Saindo do sistema...")
                
            
            else:
                print("Opção inválida!")
        
        except ValueError:
            print("\nERRO: Entrada inválida. Por favor, digite um número quando solicitado.")
        except Exception as e:
            print(f"\nOcorreu um erro inesperado: {e}")
            
        input("\nPressione Enter para continuar...")