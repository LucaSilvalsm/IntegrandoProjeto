# Model/Carrinho_produto.py
class CarrinhoProdutoDTO:
    def __init__(self, produto_id, nome_produto, quantidade, observacao, preco_total, imagem_produto):
        self.produto_id = produto_id
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.observacao = observacao
        self.preco_total = preco_total
        self.imagem_produto = imagem_produto

    @classmethod
    def from_carrinho_produto(cls, carrinho, produto):
        return cls(
            produto_id=carrinho.produto_id,
            nome_produto=produto.nome_produto,
            quantidade=carrinho.quantidade,
            observacao=carrinho.observacao,
            preco_total=str(carrinho.preco_total),  # Converte para string para garantir serialização correta
            imagem_produto=produto.imagem  # Supondo que 'imagem' seja o campo correto para imagem do produto
        )

    def serialize(self):
        return {
            'produto_id': self.produto_id,
            'nome_produto': self.nome_produto,
            'quantidade': self.quantidade,
            'observacao': self.observacao,
            'preco_total': self.preco_total,
            'imagem_produto': self.imagem_produto
        }
