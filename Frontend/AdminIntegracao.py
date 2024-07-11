from Classes.UsuarioAdmin import UsuarioAdmin
import json
import requests

def JSON2Admin(dadosJSON):
    return UsuarioAdmin(
        id=dadosJSON.get("id"),
        nome=dadosJSON.get("nome"),  # Use get() para evitar KeyError
        sobrenome=dadosJSON.get("sobrenome"),
        email=dadosJSON.get("email"),
        senha=dadosJSON.get("senha")
    )

class AdminNet:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:8000/api/admin'
    
    def incluir(self, usuario):
        resposta = requests.post(f"{self.baseURL}/cadastro", json=usuario.serialize())
        if resposta.status_code in [200, 201]:
            usuario_json = resposta.json()
            print(f"Resposta do servidor: {usuario_json}")
            return JSON2Admin(usuario_json)
        else:
            print(f"Erro ao incluir usuário: {resposta.status_code} - {resposta.text}")
            return None
    
    def obter_email(self, email):
        resposta = requests.get(f"{self.baseURL}/por_email/{email}")
        if resposta.status_code == 200:
            admin_json = resposta.json()
            return JSON2Admin(admin_json)
        return None
    
    def login(self, email, senha):
        resposta = requests.post(f"{self.baseURL}/login", json={"email": email, "senha": senha})
        if resposta.status_code == 200:
            return JSON2Admin(resposta.json())
        return None
    
    def get_usuario_by_id(self, usuarioAdmin_id):
        try:
            resposta = requests.get(f"{self.baseURL}/{usuarioAdmin_id}")
            resposta.raise_for_status()
            usuario_json = resposta.json()
            print(f"Resposta do servidor para get_usuario_by_id: {usuario_json}")
            return JSON2Admin(usuario_json)
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP: {http_err}")
            return None
        except json.JSONDecodeError as json_err:
            print(f"Erro ao decodificar JSON: {json_err}")
            return None
        except Exception as err:
            print(f"Outro erro: {err}")
            return None
