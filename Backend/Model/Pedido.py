from Model import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=db.func.current_timestamp())
    forma_pagamento = db.Column(db.String(100))
    endereco_entrega = db.Column(db.String(400))
    status = db.Column(db.String(100))
    valor_total = db.Column(db.Numeric(10, 2))
    observacao = db.Column(db.Text)
    itens_comprados = db.Column(db.Text)
    def __init__(self, usuario_id, forma_pagamento, endereco_entrega, status, valor_total, observacao,itens_comprados):
            self.usuario_id = usuario_id
            self.forma_pagamento = forma_pagamento
            self.endereco_entrega = endereco_entrega
            self.status = status
            self.valor_total = valor_total
            
            self.itens_comprados = itens_comprados
            
            # Formatar as observações dos itens
            observacoes_itens = []
            for item in itens_comprados:
                observacao_item = f"{item.nome_produto} - Quantidade: {item.quantidade} - Observação: {item.observacao}"
                observacoes_itens.append(observacao_item)

            self.observacao += "\n" + "\n".join(observacoes_itens)  # Adicionar observações dos itens ao campo observacao
            
    def serialize(self):
            return {
                'id': self.id,
                'usuario_id': self.usuario_id,
                'data_pedido': self.data_pedido.strftime('%Y-%m-%d %H:%M:%S'),  # Formato ISO 8601
                'forma_pagamento': self.forma_pagamento,
                'endereco_entrega': self.endereco_entrega,
                'status': self.status,
                'valor_total': str(self.valor_total),  # Converter para string
                'observacao': self.observacao,
                'itens_comprados': self.itens_comprados  # Certifique-se de que itens_comprados seja serializável
                # Adicione outros campos conforme necessário
            }
    def formatar_itens_comprados(self):
            # Exemplo: Converter itens_comprados para uma lista de dicionários
            return [
                {
                    'nome_produto': item.nome_produto,
                    'quantidade': item.quantidade,
                    'observacao': item.observacao
                }
                for item in self.itens_comprados
            ]