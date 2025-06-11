from datetime import datetime

class Pedido:
    def __init__(self , codigo_produto , quantidade , data_solicitacao , solicitante ):
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.data_solicitacao = datetime.strptime(data_solicitacao , "%Y-%m-%d")
        self.solicitante = solicitante