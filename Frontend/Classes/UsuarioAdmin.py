class UsuarioAdmin:
    def __init__(self, nome, sobrenome, email, senha, id=None):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome        
        self.email = email
        self.senha = senha       
        self.tipo_usuario = 'Administrador'

    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sobrenome": self.sobrenome,            
            "email": self.email,
            "senha": self.senha,            
            "tipo_usuario": self.tipo_usuario
        } 

    def get_id(self):
        return str(self.id)
   
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
