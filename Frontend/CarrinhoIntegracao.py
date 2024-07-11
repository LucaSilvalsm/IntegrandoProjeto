import json
import requests
from Classes.Carrinho import Carrinho

def JSON2Carrinho(dadosJSON):
    carrinho = Carrinho(
        usuario_id=dadosJSON.get("usuario_id"),
        produto_id=dadosJSON.get("produto_id"),
        nome_produto=dadosJSON.get("nome_produto"),
        quantidade=dadosJSON.get("quantidade"),
        imagem_produto=dadosJSON.get("imagem_produto"),
        observacao=dadosJSON.get("observacao"),
        preco_total=dadosJSON.get("preco_total")
    )
    return carrinho

class CarrinhoNet:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:8000/api'

    def criar_carrinho(self, carrinho):
        url = f"{self.baseURL}/carrinhoDTO"
        headers = {'Content-Type': 'application/json'}
        try:
            resposta = requests.post(url, json=carrinho.serialize(), headers=headers)
            resposta.raise_for_status()
            return resposta.json(), resposta.status_code
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ao criar carrinho: {http_err}")
            return None, 500
        except Exception as err:
            print(f"Erro ao criar carrinho: {err}")
            return None, 500
        
    def get_id(self, id):
        url = f"{self.baseURL}/admin/produto/{id}"
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            produto_json = resposta.json()
            return JSON2Carrinho(produto_json)
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ao obter produto por ID: {http_err}")
            return None
        except Exception as err:
            print(f"Erro ao obter produto por ID: {err}")
            return None
