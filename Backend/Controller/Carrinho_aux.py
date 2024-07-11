from Model.Carrinho import Carrinho
from dao.CarrinhoDAO import CarrinhoDAO

class CarrinhoController:
    def __init__(self):
        self.dao = CarrinhoDAO()
        
    def create(self, carrinho):
        return self.dao.create(carrinho)
    
    def obter_id(self, carrinho_id):
        return self.dao.obter_id(carrinho_id)
    
    def delete(self, carrinho_id):
        return self.dao.delete(carrinho_id)
    
    def obter_itens_carrinho(self, usuario_id):
        return self.dao.obter_itens_carrinho(usuario_id)
    
    def get_by_user(self, usuario_id):
        return self.dao.get_by_user(usuario_id)
