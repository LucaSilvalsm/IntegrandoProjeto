class Usuario:
    def __init__(self, nome, sobrenome, telefone, email, senha, endereco=None, numero_casa=None, complemento=None, bairro=None):
        self.id = None
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.endereco = endereco
        self.numero_casa = numero_casa
        self.complemento = complemento
        self.bairro = bairro
        self.tipo_usuario = 'Cliente'
    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "telefone": self.telefone,
            "email": self.email,
            "senha": self.senha,
            "endereco": self.endereco,
            "numero_casa": self.numero_casa,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "tipo_usuario": self.tipo_usuario
        } 
    def get_id(self):
        return str(self.id)
   
    @property
    def is_active(self):
        # Implemente a lógica para verificar se o usuário está ativo
        # Exemplo: return self.ativo
        return True  # Ajuste conforme necessário

    @property
    def is_authenticated(self):
        # Implemente a lógica para verificar se o usuário está autenticado
        # Exemplo: return self.autenticado
        return True  # Ajuste conforme necessário

    @property
    def is_anonymous(self):
        return False
