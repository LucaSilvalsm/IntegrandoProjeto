class Produto:
    def __init__(self, id=None, nome_produto="", tipo_produto="", tamanho="", ingrediente="", preco=0.0, descricao="", imagem=""):
        self.id = id
        self.nome_produto = nome_produto
        self.tipo_produto = tipo_produto
        self.tamanho = tamanho
        self.ingrediente = ingrediente
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem

    def serialize(self):
        return {
            "id": self.id,
            "nome_produto": self.nome_produto,
            "tipo_produto": self.tipo_produto,
            "tamanho": self.tamanho,
            "ingrediente": self.ingrediente,
            "preco": self.preco,
            "descricao": self.descricao,
            "imagem": f"/static/img/produtos/{self.imagem}"  # Adiciona o caminho completo da imagem
        }
