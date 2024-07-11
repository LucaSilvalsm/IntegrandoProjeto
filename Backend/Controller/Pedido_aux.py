from Model.Pedido import Pedido
from dao.PedidoDAO import PedidoDAO

class PedidoController:
    def __init__(self):
        self.dao=PedidoDAO()
        
    def create(self,pedido):
        return self.dao.create(pedido)
    
    def create_and_delete_carrinho(self, pedido, usuario_id):
        return self.dao.create_and_delete_carrinho(pedido, usuario_id)
    
    def obter_todos_os_pedidos(self):
        return self.dao.obter_todos_os_pedidos()
    
    def obter_ultimos_10_pedido(self):
        return self.dao.obter_ultimos_10_pedidos()
    
    def obter_pedidos_por_usuario_id(self,usuario_id):
        return self.dao.obter_pedidos_por_usuario_id(usuario_id)
    
    def deletar(self,pedido_id):
        return self.dao.deletar(pedido_id)
    
    def atualizar_status_pedido(self,pedido_id,novo_status):
        return self.dao.atualizar_status_pedido(pedido_id, novo_status)
    def calcular_valor_total_dos_pedidos(self):
        return self.dao.calcular_valor_total_dos_pedidos()
    
    def contar_quantidade_de_pedidos(self):
        return self.dao.contar_quantidade_de_pedidos()
    
    def calcular_media_dos_pedidos(self):
        return self.dao.calcular_media_dos_pedidos()
    
    def obter_id(self,pedido_id):
        return self.dao.obter_id(pedido_id)
    