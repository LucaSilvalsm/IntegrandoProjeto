class Carrinho:
    def __init__(self, usuario_id, produto_id, nome_produto, quantidade, observacao, preco_total, imagem_produto=None):
        self.usuario_id = usuario_id
        self.produto_id = produto_id
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.observacao = observacao
        self.preco_total = preco_total
        self.imagem_produto = imagem_produto

    def serialize(self):
        return {
            'usuario_id': self.usuario_id,
            'produto_id': self.produto_id,
            'nome_produto': self.nome_produto,
            'quantidade': self.quantidade,
            'observacao': self.observacao,
            'preco_total': str(self.preco_total),
            'imagem_produto': self.imagem_produto
        }
