# resources/CarrinhoProduto.py
from flask import request, jsonify
from flask_restful import Resource
from Model.Carrinho_produto import CarrinhoProdutoDTO
from Controller.Carrinho_aux import CarrinhoController
from Controller.Produto_aux import ProdutoController
from Model.Carrinho import Carrinho

class CarrinhoProdutoResource(Resource):
    def __init__(self):
        self.carrinho_controller = CarrinhoController()
        self.produto_controller = ProdutoController()

    def post(self):
        data = request.json  # Supondo que os dados venham como JSON do frontend
        
        # Busca o produto pelo ID enviado do frontend
        produto_id = data.get('produto_id')
        produto = self.produto_controller.get_produto_by_id(produto_id)
        
        if not produto:
            return {'message': 'Produto não encontrado'}, 404
        
        # Cria um CarrinhoProdutoDTO com os dados recebidos do frontend e do produto encontrado
        carrinho_produto_dto = CarrinhoProdutoDTO(
            produto_id=produto_id,
            nome_produto=produto.nome_produto,
            quantidade=data.get('quantidade'),
            observacao=data.get('observacao'),
            preco_total=data.get('preco_total'),
            imagem_produto=produto.imagem
        )
        
        # Cria o objeto Carrinho no banco de dados usando o DTO
        novo_carrinho = Carrinho(
            usuario_id=1,  # Supondo que você tenha o ID do usuário de alguma forma
            produto_id=carrinho_produto_dto.produto_id,
            nome_produto=carrinho_produto_dto.nome_produto,
            quantidade=carrinho_produto_dto.quantidade,
            observacao=carrinho_produto_dto.observacao,
            preco_total=carrinho_produto_dto.preco_total,
            imagem_produto=carrinho_produto_dto.imagem_produto
        )
        
        try:
            self.carrinho_controller.create(novo_carrinho)
            return {'message': 'Item adicionado ao carrinho com sucesso'}, 201
        except Exception as e:
            return {'message': str(e)}, 500
