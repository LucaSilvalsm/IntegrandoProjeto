from Model import Produto
from dao.ProdutoDAO import ProdutoDAO

class ProdutoController:
    def __init__(self):
        self.dao = ProdutoDAO()
        
    def incluir(self, produto):
        if not isinstance(produto, Produto):
            raise TypeError("Não é um objeto Produto")
        return self.dao.incluir(produto)
    
    def get_produto_by_id(self, produto_id):
        return self.dao.get_produto_by_id(produto_id)
    
    def alterar(self, produto_id, novo_produto):
        return self.dao.alterar(produto_id, novo_produto)
    
    def excluir(self, produto_id):
        return self.dao.excluir(produto_id)
    
    def obter(self, produto_id):
        return self.dao.obter(produto_id)
    
    def todas_categorias(self):
        return self.dao.todas_categorias()
    
    def obter_todos(self):
        return self.dao.obter_todos()
    
    def tipo_produto(self, tipo_produto):
        return self.dao.tipo_produto(tipo_produto)
