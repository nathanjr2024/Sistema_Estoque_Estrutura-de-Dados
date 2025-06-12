import json
from datetime import datetime, timedelta
from Modelos import Produto, Engradado, Estoque, Fila, Pedido

class SistemaEstoque:
    def __init__(self, nome_arquivo_produtos='produtos.json', nome_arquivo_estoque='estoque_estado.json'):
        self.estoque = Estoque()
        self.fila_pedidos = Fila()
        self.historico_pedidos_atendidos = []
        self.nome_arquivo_produtos = nome_arquivo_produtos
        self.nome_arquivo_estoque = nome_arquivo_estoque
        self.produtos_cadastrados = self._carregar_produtos()
        self._carregar_estado_estoque()
        
    def cadastrar_novo_produto(self, dados_produto):
        """Registra um novo produto no sistema e salva no arquivo JSON.
        Verifica se o produto já existe pelo código antes de cadastrar."""
        
        codigo = dados_produto['codigo']
        if any(p.codigo == codigo for p in self.produtos_cadastrados):
            print(f"Erro: Produto com código '{codigo}' já cadastrado.")
            return False
        
        try: 
            novo_produto = Produto(**dados_produto)
            self.produtos_cadastrados.append(novo_produto)
            self._salvar_produtos()
            print(f"Produto '{novo_produto.nome}' cadastrado com sucesso.")
            return True
        except (TypeError, ValueError) as e:
            print(f"Erro ao cadastrar produto: Dados inválidos: {e}")
            return False
        


    def _salvar_produtos(self):
        lista_dict = [p.para_dicionario() for p in self.produtos_cadastrados]
        with open(self.nome_arquivo_produtos, 'w', encoding='utf-8') as f:
            json.dump(lista_dict, f, ensure_ascii=False, indent=4)

    def _carregar_produtos(self):
        lista_produtos = []
        try:
            with open(self.nome_arquivo_produtos, 'r', encoding='utf-8') as f:
                lista_dict = json.load(f)
                for d in lista_dict:
                    lista_produtos.append(Produto(**d))
        except FileNotFoundError:
            print(f"Arquivo '{self.nome_arquivo_produtos}' não encontrado. Começando com lista de produtos vazia.")
        return lista_produtos

    def _salvar_estado_estoque(self):
        print("Salvando estado do estoque...")
        dados_estoque = [[pilha.para_dicionario() for pilha in linha] for linha in self.estoque.matriz]
        with open(self.nome_arquivo_estoque, 'w', encoding='utf-8') as f:
            json.dump(dados_estoque, f, ensure_ascii=False, indent=4)
        print("Estado do estoque salvo com sucesso.")

    def _carregar_estado_estoque(self):
        try:
            with open(self.nome_arquivo_estoque, 'r', encoding='utf-8') as f:
                dados_estoque = json.load(f)
            for i, linha_dados in enumerate(dados_estoque):
                for j, pilha_dados in enumerate(linha_dados):
                    for engradado_dado in pilha_dados:
                        produto_obj = next((p for p in self.produtos_cadastrados if p.codigo == engradado_dado['codigo_produto']), None)
                        if produto_obj:
                            
                            
                            engradado = Engradado(
                                produto=produto_obj,
                                quantidade=engradado_dado['quantidade'],
                                capacidade_maxima=engradado_dado['capacidade_maxima']
                            )
                            
                            
                            self.estoque.matriz[i][j].empilhar(engradado)
        except (FileNotFoundError, json.JSONDecodeError):
             print(f"Arquivo de estado do estoque não encontrado ou inválido. Iniciando com estoque vazio.")


    def adicionar_produto_estoque(self, codigo_produto, quantidade_engrados, linha, coluna):
    # 1. Busca o objeto completo do produto
        produto_base = next((p for p in self.produtos_cadastrados if p.codigo == codigo_produto), None)
        if not produto_base:
            print("Erro: Produto com este código não cadastrado.")
            return
            
        
        # 2. Captura a quantidade padrão usando o nome CORRETO e PADRONIZADO
        try:
            # Usa o nome 'quantidade_por_produto'
            qtd_padrao = produto_base.quantidade_por_produto 
        except AttributeError:
            # A mensagem de erro também foi atualizada para refletir o nome correto
            print("\nERRO: O objeto 'Produto' não tem o atributo 'quantidade_por_produto'.")
            print("Por favor, verifique a classe Produto em 'modelos.py' e se os produtos foram cadastrados corretamente.")
            return

        pilha_destino = self.estoque.matriz[linha][coluna]
        adicionados = 0
        
        for _ in range(quantidade_engrados):
            if not pilha_destino.esta_cheia():
                if pilha_destino.esta_vazia() or pilha_destino.ver_topo().produto.codigo == codigo_produto:
                    
                    # 3. Cria o novo engradado usando a quantidade padrão correta
                    novo_engradado = Engradado(
                        produto=produto_base, 
                        quantidade=qtd_padrao,
                        capacidade_maxima=qtd_padrao
                    )
                    pilha_destino.empilhar(novo_engradado)
                    adicionados += 1
                else:
                    print(f"Erro: A pilha em L{linha}C{coluna} já contém outro produto.")
                    break
            else:
                print(f"Aviso: Pilha em L{linha}C{coluna} ficou cheia. {adicionados} de {quantidade_engrados} engradados adicionados.")
                break
                
        if adicionados > 0:
            print(f"Operação concluída. {adicionados} engradados de '{produto_base.nome}' adicionados.")


    def registrar_pedido(self, solicitante, itens_pedido):
        novo_pedido = Pedido(solicitante, itens_pedido)
        self.fila_pedidos.enfileirar(novo_pedido)
        print(f"Pedido de '{solicitante}' registrado e adicionado à fila.")

    def processar_proximo_pedido(self):
        if self.fila_pedidos.esta_vazia():
            print("Não há pedidos na fila para processar.")
            return

        pedido_atual = self.fila_pedidos.desenfileirar()
        print(f"\nProcessando pedido de '{pedido_atual.solicitante}'...")
        
        pode_atender = True
        for item in pedido_atual.itens:
            codigo = item['codigo_produto']
            qtd_necessaria = item['quantidade']
            posicoes = self.estoque.buscar_produto(codigo)
            
            total_disponivel = 0
            if posicoes:
                topo = self.estoque.matriz[posicoes[0][0]][posicoes[0][1]].ver_topo()
                if topo:
                    qtd_por_engradado = topo.quantidade
                    for i, j in posicoes:
                        total_disponivel += len(self.estoque.matriz[i][j]) * qtd_por_engradado
            
            if total_disponivel < qtd_necessaria:
                print(f"--> Estoque INSUFICIENTE para o produto '{codigo}'. Disponível: {total_disponivel}, Necessário: {qtd_necessaria}.")
                pode_atender = False
                break 

        if pode_atender:
            print("--> Estoque suficiente. Realizando a baixa dos produtos.")
            for item in pedido_atual.itens:
                qtd_a_remover_total = item['quantidade']
                posicoes = self.estoque.buscar_produto(item['codigo_produto'])
                
                topo = self.estoque.matriz[posicoes[0][0]][posicoes[0][1]].ver_topo()
                qtd_por_engradado = topo.quantidade
                engradados_a_remover = (qtd_a_remover_total + qtd_por_engradado - 1) // qtd_por_engradado

                for i, j in posicoes:
                    if engradados_a_remover == 0: break
                    pilha = self.estoque.matriz[i][j]
                    
                    while engradados_a_remover > 0 and not pilha.esta_vazia():
                        pilha.desempilhar()
                        engradados_a_remover -= 1
                        print(f"Removido 1 engradado do produto '{item['codigo_produto']}' da posição L{i}C{j}.")

            pedido_atual.atendido = True
            self.historico_pedidos_atendidos.append(pedido_atual)
            print(f"\nPedido de '{pedido_atual.solicitante}' ATENDIDO com sucesso!")
        else:
            print(f"\nPedido de '{pedido_atual.solicitante}' NÃO PODE SER ATENDIDO por falta de estoque. O pedido foi descartado.")
    
    def gerar_relatorio_vencimento(self, dias_limite=30):
        print(f"\n--- Relatório de Produtos Próximos ao Vencimento ({dias_limite} dias) ---")
        produtos_vencendo = []
        data_limite = datetime.now() + timedelta(days=dias_limite)
        self._verificar_vencimento_recursivo(0, 0, data_limite, produtos_vencendo)
        
        if not produtos_vencendo:
            print("Nenhum produto próximo do vencimento.")
        else:
            for p, l, c in produtos_vencendo:
                print(f"- {p.nome} (Lote: {p.lote}) vence em {p.data_validade.strftime('%d/%m/%Y')} na posição L{l}C{c}")
        print("-" * 55)

    def _verificar_vencimento_recursivo(self, linha, coluna, data_limite, resultados):
        if linha >= self.estoque.linhas:
            return

        pilha = self.estoque.matriz[linha][coluna]
        if not pilha.esta_vazia():
            produto_topo = pilha.ver_topo().produto
            if produto_topo.data_validade <= data_limite:
                if (produto_topo, linha, coluna) not in resultados:
                    resultados.append((produto_topo, linha, coluna))

        proxima_coluna = (coluna + 1) % self.estoque.colunas
        proxima_linha = linha + (1 if proxima_coluna == 0 else 0)
        self._verificar_vencimento_recursivo(proxima_linha, proxima_coluna, data_limite, resultados)

    def gerar_relatorio_historico(self):
        print("\n--- Histórico de Pedidos Atendidos ---")
        if not self.historico_pedidos_atendidos:
            print("Nenhum pedido foi atendido ainda.")
        else:
            self._exibir_historico_recursivo(self.historico_pedidos_atendidos)
        print("-" * 35)

    def _exibir_historico_recursivo(self, lista_pedidos):
        if not lista_pedidos:
            return
        print(f"- {lista_pedidos[0]}")
        self._exibir_historico_recursivo(lista_pedidos[1:])