import requests
import json
from Classes.Usuario import Usuario

def JSON2Usuario(dadosJSON):
    print(f"JSON recebido: {dadosJSON}")  # Adicione um log para verificar o JSON recebido
    usuario = Usuario(
        nome=dadosJSON["nome"],
        sobrenome=dadosJSON["sobrenome"],
        telefone=dadosJSON["telefone"],
        email=dadosJSON["email"],
        senha=dadosJSON["senha"],
        endereco=dadosJSON.get("endereco"),
        numero_casa=dadosJSON.get("numero_casa"),
        complemento=dadosJSON.get("complemento"),
        bairro=dadosJSON.get("bairro")
    )
    usuario.id = dadosJSON["id"]
    usuario.tipo_usuario = dadosJSON["tipo_usuario"]
    return usuario

class UsuarioNet:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:8000/api/usuario'

    def incluir(self, usuario):
        resposta = requests.post(f"{self.baseURL}/cadastro", json=usuario.serialize())
        if resposta.status_code == 201:
            usuario_json = resposta.json()
            return JSON2Usuario(usuario_json['usuario'])
        else:
            print(f"Erro ao incluir usuário: {resposta.status_code} - {resposta.text}")
            return None
    def excluir(self, usuario_id):
        resposta = requests.delete(f"{self.baseURL}/{usuario_id}")
        return resposta.status_code

    def get_usuario_by_id(self, usuario_id):
        try:
            resposta = requests.get(f"{self.baseURL}/{usuario_id}")
            resposta.raise_for_status()
            usuario_json = resposta.json()
            print(f"Resposta do servidor para get_usuario_by_id: {usuario_json}")  # Adicione um log para verificar a resposta
            return JSON2Usuario(usuario_json)
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP: {http_err}")
            return None
        except json.JSONDecodeError as json_err:
            print(f"Erro ao decodificar JSON: {json_err}")
            return None
        except Exception as err:
            print(f"Outro erro: {err}")
            return None

    def obter_todos(self):
        resposta = requests.get(f"{self.baseURL}/lista")
        return [JSON2Usuario(usuario) for usuario in json.loads(resposta.content)]

    
    def login(self, email, senha):
        resposta = requests.post(f"{self.baseURL}/login", json={"email": email, "senha": senha})
        if resposta.status_code == 200:
            usuario_json = resposta.json()
            return JSON2Usuario(usuario_json)
        else:
            return None
            
    def nome_completo(self, nome, sobrenome):
        resposta = requests.post(f"{self.baseURL}/nome_completo", json={"nome": nome, "sobrenome": sobrenome})
        return resposta.json()["nome_completo"]

    def endereco_completo(self, endereco, numero_casa, complemento, bairro, telefone):
        resposta = requests.post(f"{self.baseURL}/endereco_completo", json={
            "endereco": endereco,
            "numero_casa": numero_casa,
            "complemento": complemento,
            "bairro": bairro,
            "telefone": telefone
        })
        return resposta.json()["endereco_completo"]

    def obter_por_email(self, email):
        resposta = requests.get(f"{self.baseURL}/por_email", params={"email": email})
        if resposta.status_code == 200:
            if resposta.content:
                return JSON2Usuario(json.loads(resposta.content))
            else:
                return None  # Retornar None ou outro valor adequado caso a resposta esteja vazia
        else:
            return None  # Tratar adequadamente outros códigos de status de erro