from Model import db
from Model.Usuario import Usuario

class UsuarioDAO:
    def incluir(self, usuario):
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            raise e

    def get_usuario_by_id(self, usuario_id):
        return Usuario.query.get(usuario_id)

    def excluir(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            
    def nome_completo(self, nome, sobrenome):
        return f"{nome} {sobrenome}"

    def endereco_completo(self, endereco, numero_casa, complemento, bairro, telefone):
        return f"{endereco} - {numero_casa} - {complemento} - {bairro} - {telefone}"

    def obter_todos(self):
        usuarios = Usuario.query.all()  # Consulta todos os usuários do banco de dados
        lista_usuarios = [usuario.serialize() for usuario in usuarios]  # Serializa cada usuário em um dicionário

        return lista_usuarios
    def obter_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def close(self):
        db.session.close()
