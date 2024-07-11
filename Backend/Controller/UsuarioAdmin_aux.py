from dao.UsuarioAdminDAO import UsuarioAdminDAO

class AdminController:
    def __init__(self):
        self.dao = UsuarioAdminDAO()
        
    def incluir(self, usuario_admin):
        return self.dao.incluir(usuario_admin)
    
    def alterar(self, usuario_admin):
        return self.dao.alterar(usuario_admin)
    
    def excluir(self, id):
        return self.dao.excluir(id)
    
    def obterTodos(self):
        return self.dao.obterTodos()
    
    def obter_email(self, email):
        return self.dao.obter_por_email(email)
    
    def obter(self, id):
        return self.dao.obter(id)
    
    def get_usuario_by_id(self,id):
        return self.dao.get_usuario_by_id(id)(id)
    
    
    def close(self):
        return self.dao.close()
