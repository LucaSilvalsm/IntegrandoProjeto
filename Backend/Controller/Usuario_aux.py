from Model import Usuario
from dao.UsuarioDAO import UsuarioDAO


class UsuarioController:
    def __init__(self):
        self.dao=UsuarioDAO()
    
    def incluir(self,usuario):
        return self.dao.incluir(usuario)
    
    def excluir(self,usuario_id):
        return self.dao.excluir(usuario_id)
    
    def get_usuario_by_id(self,usuario_id):
        return self.dao.get_usuario_by_id(usuario_id)
    
    def obter_todos(self):
        return self.dao.obter_todos()
    
    def nome_completo(self,nome,sobrenome):
        return self.dao.nome_completo(nome, sobrenome)
    
    def endereco_completo(self,endereco, numero_casa, complemento, bairro, telefone):
        return self.dao.endereco_completo(endereco, numero_casa, complemento, bairro, telefone)
    def obter_por_email(self,email):
        return self.dao.obter_por_email(email)