import requests
import json
from Classes.Produto import Produto

def JSON2Produto(dadosJSON):
    produto = Produto(
        id=dadosJSON.get("ID"),  # Use .get() para evitar KeyError se o campo não existir
        nome_produto=dadosJSON.get("Produto"),
        tipo_produto=dadosJSON.get("Tipo"),
        tamanho=dadosJSON.get("Tamanho"),
        ingrediente=dadosJSON.get("Ingrediente"),
        preco=dadosJSON.get("Preço"),
        descricao=dadosJSON.get("Descrição"),
        imagem=dadosJSON.get("Imagem")
    )
    return produto

class ProdutoNet:
    def __init__(self):
        self.baseURL = 'http://127.0.0.1:8000/api/admin/'

    def incluir(self, produto, imagem_path):
        files = {'imagem': open(imagem_path, 'rb')}
        data = {
            'nome_produto': produto.nome_produto,
            'tipo_produto': produto.tipo_produto,
            'tamanho[]': produto.tamanho.split(','),  # Supondo que tamanho é uma string separada por vírgulas
            'ingrediente[]': produto.ingrediente.split(' - '),  # Supondo que ingrediente é uma string separada por ' - '
            'preco': produto.preco,
            'descricao': produto.descricao
        }
        resposta = requests.post(f"{self.baseURL}/newproduto", data=data, files=files)
        return resposta.json() if resposta.status_code == 200 else {'message': resposta.text}

    def get_id(self, id):
        try:
            resposta = requests.get(f"{self.baseURL}/produto/{id}")
            resposta.raise_for_status()
            produto_json = resposta.json()
            print(f"Resposta do servidor para get_id: {produto_json}")  # Adicione um log para verificar a resposta
            return JSON2Produto(produto_json)
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
        resposta = requests.get(f"{self.baseURL}/produto/lista")
        produtos_por_categoria = json.loads(resposta.content)
        
        if not isinstance(produtos_por_categoria, dict):
            return {}

        return {
            categoria: [JSON2Produto(produto) for produto in produtos]
            for categoria, produtos in produtos_por_categoria.items()
        }
        
    def obter_por_tipo(self, tipo):
        resposta = requests.get(f"{self.baseURL}/produtos/{tipo}")
        produtos = json.loads(resposta.content)
        
        # Corrigir a URL da imagem para ser relativa à pasta de imagens estáticas
        for produto in produtos:
            if 'Imagem' in produto:
                if 'http://' in produto['Imagem'] or 'https://' in produto['Imagem']:
                    # Remove a parte inicial da URL até a pasta de imagens estáticas
                    produto['Imagem'] = produto['Imagem'].split('/static/img/produtos/')[-1]
            
        return [JSON2Produto(produto).serialize() for produto in produtos]
    
    def excluir(self, id):
        try:
            # Endpoint da API para excluir um produto pelo ID
            url = f"{self.baseURL}/produto/delete/{id}"
            resposta = requests.delete(url)

            if resposta.status_code == 200:
                return "Produto removido com sucesso"
            elif resposta.status_code == 404:
                return "Produto não encontrado"
            else:
                return f"Erro ao excluir o produto: {resposta.text}"

        except Exception as e:
            return f"Erro ao excluir o produto: {str(e)}"