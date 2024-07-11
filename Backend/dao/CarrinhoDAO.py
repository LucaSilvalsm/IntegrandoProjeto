from Model import db, Carrinho

class CarrinhoDAO:
    
    def create(self, carrinho):
        try:
            db.session.add(carrinho)
            db.session.commit()
            return carrinho
        except Exception as e:
            db.session.rollback()
            raise e

    def obter_id(self, carrinho_id):
        return Carrinho.query.get(carrinho_id)

    def delete(self, carrinho_id):
        carrinho = Carrinho.query.get(carrinho_id)
        if carrinho:
            db.session.delete(carrinho)
            db.session.commit()

    def obter_itens_carrinho(self, usuario_id):
        return Carrinho.query.filter_by(usuario_id=usuario_id).all()

    def get_all(self):
        return Carrinho.query.all()

    def get_by_user(self, usuario_id):
        return Carrinho.query.filter_by(usuario_id=usuario_id).all()

    def close(self):
        db.session.close()