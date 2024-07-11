from Model import db
from flask import url_for

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(200), nullable=False)
    tipo_produto = db.Column(db.String(200))
    tamanho = db.Column(db.String(200))
    ingrediente = db.Column(db.String(200))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(250))

    def __init__(self, nome_produto, tipo_produto, tamanho, ingrediente, preco, descricao=None, imagem=None):
        self.nome_produto = nome_produto
        self.tipo_produto = tipo_produto
        self.tamanho = tamanho
        self.ingrediente = ingrediente
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem

    def serialize(self):
        return {
            "ID": self.id,
            "Produto": self.nome_produto,
            "Tipo": self.tipo_produto,
            "Tamanho": self.tamanho,
            "Ingrediente": self.ingrediente,
            "Descrição": self.descricao,
            "Preço": (self.preco),  # Converter Numeric para string para evitar problemas de serialização
            "Imagem": url_for('static', filename=f'img/produtos/{self.imagem}', _external=True) if self.imagem else None
        }
