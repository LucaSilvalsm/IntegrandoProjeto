from flask import Flask, jsonify, request, current_app as app, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

from flask_session import Session
import secrets
import os
import logging
logging.basicConfig(level=logging.DEBUG)
# Importando modelos e controladores
from Model import db, Usuario
from Model.Produto import Produto
from Model.Usuario import UsuarioAdmin
from Model.Carrinho import Carrinho
from Model.Pedido import Pedido
from Controller.Produto_aux import ProdutoController
from Controller.Pedido_aux import PedidoController
from Controller.Usuario_aux import UsuarioController
from Controller.Carrinho_aux import CarrinhoController
from Controller.UsuarioAdmin_aux import AdminController
from Controller.CarrinhoProduto import CarrinhoProdutoDTO

# Configuração do banco de dados
from Model.config import DATABASE


app = Flask(__name__)

# Configuração da chave secreta
app.secret_key = secrets.token_hex(24)

# Configuração do SQLAlchemy
DB_URL = f"postgresql://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração da pasta de upload de arquivos
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img', 'produtos')

# Configuração da sessão
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Inicialização do SQLAlchemy
db.init_app(app)

# Inicialização do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# Função para carregar o usuário pelo ID
# Função para carregar o usuário pelo ID
@login_manager.user_loader
def load_user(user_id):
    # Verifica se o usuário é cliente ou administrador
    if usuario := usuariocontroller.get_usuario_by_id(user_id):
        return usuario
    else:
        admincontroller = AdminController()
        return admincontroller.get_admin_by_id(user_id)
    
@app.get("/api/usuario/<int:id>")
def get_usuario_by_id(id):
    usuario = usuariocontroller.get_usuario_by_id(id)
    if usuario:
        return jsonify(usuario.serialize()), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404
# Rota para cadastro de usuários


@app.get("/api/admin/<int:id>")
def getByID(id):
    usuarioAdmin = admincontroller.get_usuario_by_id(id)
    if usuarioAdmin:
        return jsonify(usuarioAdmin.serialize()), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404
# Rota para cadastro de usuários




@app.post("/api/usuario/cadastro")
def incluir():
    data = request.json
    try:
        nome = data.get('nome')
        sobrenome = data.get('sobrenome')
        telefone = data.get('telefone')
        email = data.get('email')
        senha = data.get('senha')
        endereco = data.get('endereco')
        numero_casa = data.get('numero_casa')
        complemento = data.get('complemento')
        bairro = data.get('bairro')

        # Adicione log para verificar os valores
        logging.debug(f"Senha recebida: {senha}")
        # Verificar se o email já está sendo utilizado
        if usuariocontroller.obter_por_email(email):
            return jsonify({'message': 'Este email já está sendo utilizado.', 'error': 'Email already in use'}), 400

        novo_usuario = Usuario(nome=nome, sobrenome=sobrenome, telefone=telefone, email=email, senha=senha,
                               endereco=endereco, numero_casa=numero_casa, complemento=complemento, bairro=bairro)

        usuariocontroller.incluir(novo_usuario)
        login_user(novo_usuario)  # Faz o login do novo usuário
        return jsonify({'message': 'Usuário cadastrado com sucesso', 'usuario': novo_usuario.serialize()}), 201

    except Exception as e:
        return jsonify({'message': 'Erro ao cadastrar usuário', 'error': str(e)}), 500

# Rota para obter todos os usuários (apenas para exemplo)
@app.get("/api/usuario/lista")
def obter_todos():
    lista = usuariocontroller.obter_todos()
    return jsonify(lista)

# Rota para login de usuários
@app.post("/api/usuario/login")
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if email and senha:
        usuario = usuariocontroller.obter_por_email(email=email)
        if usuario and usuario.senha == senha:
            login_user(usuario)  # Faz o login do usuário
            session['user_id'] = usuario.id  # Usando o objeto session do Flask
            app.logger.info(f"Usuário {usuario.email} logado com sucesso. ID na sessão: {session.get('user_id')}")
            
            app.logger.info(f"Sessão do usuário: {session}")
            return jsonify(usuario.serialize()), 200

    return jsonify({'message': 'Credenciais inválidas.'}), 401

@app.post('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso.'}), 200





@app.post("/api/usuario/nome_completo")
def nome_completo():
    data = request.json
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')
    nome_completo = usuariocontroller.nome_completo(nome, sobrenome)
    return jsonify({"nome_completo": nome_completo})

@app.post("/api/usuario/endereco_completo")
def endereco_completo():
    data = request.json
    endereco = data.get('endereco')
    numero_casa = data.get('numero_casa')
    complemento = data.get('complemento')
    bairro = data.get('bairro')
    telefone = data.get('telefone')
    endereco_completo = usuariocontroller.endereco_completo(endereco, numero_casa, complemento, bairro, telefone)
    return jsonify({"endereco_completo": endereco_completo})




@app.get("/api/usuario/por_email")
def obter_por_email():
    email = request.args.get('email')
    usuario = usuariocontroller.obter_por_email(email)
    if usuario:
        return jsonify(usuario.serialize()), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404
    

@app.post("/api/admin/cadastro")
def cadastro_admin():
    data = request.json
    print(f"Data received: {data}")
    
    nome = data.get('nome')
    sobrenome = data.get('sobrenome')    
    email = data.get('email')
    senha = data.get('senha')
    
    novo_admin = UsuarioAdmin(
        nome=nome,
        sobrenome=sobrenome,
        email=email,
        senha=senha    
    )
    
    try:
        if admincontroller.obter_email(email):
            return jsonify({'message': 'Email já cadastrado'}), 400

        admincontroller.incluir(novo_admin)
        login_user(novo_admin)

        return jsonify({'message': 'Usuário administrativo registrado com sucesso!', 'id': novo_admin.id}), 200

    except IntegrityError as e:
        return jsonify({'message': f'Erro ao registrar usuário administrativo: {str(e)}'}), 400

    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({'message': f'Erro ao adicionar usuário: {str(e)}'}), 400

@app.get("/api/admin/por_email/<string:email>")
def obter_email(email):
    usuarioadmin = admincontroller.obter_email(email)
    if usuarioadmin:
        return jsonify(usuarioadmin.serialize()), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
@app.post("/api/admin/login")
def login_admin():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if email and senha:
        usuario_admin = admincontroller.obter_email(email=email)
        if usuario_admin and usuario_admin.senha == senha:
            login_user(usuario_admin)
            return jsonify({'message': 'Login realizado com sucesso', 'id': usuario_admin.id}), 200

    return jsonify({'message': 'Credenciais inválidas.'}), 401
@app.get("/api/admin/lista")
def obter_lista():
    todos = admincontroller.obterTodos()
    serialized_todos = [usuario_admin.serialize() for usuario_admin in todos]
    return jsonify(serialized_todos)

@app.get
@app.post("/api/admin/newproduto")
def new_produto():
    data = request.form

    nome_produto = data.get('nome_produto')
    tipo_produto = data.get('tipo_produto')
    tamanhos_selecionados = data.getlist('tamanho[]')
    ingredientes_selecionados = data.getlist('ingrediente[]')
    preco = data.get('preco')
    descricao = data.get('descricao')
    imagem = request.files['imagem'] if 'imagem' in request.files else None

    tamanho = ','.join(tamanhos_selecionados)
    ingrediente = ' - '.join(ingredientes_selecionados)

    if imagem and allowed_file(imagem.filename):
        nome_imagem = secure_filename(imagem.filename)
        path_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem)
        imagem.save(path_imagem)
    else:
        return jsonify({'message': 'Erro ao processar imagem ou imagem ausente'}), 400

    try:
        novo_produto = Produto(
            nome_produto=nome_produto,
            tipo_produto=tipo_produto,
            tamanho=tamanho,
            ingrediente=ingrediente,
            preco=float(preco),
            descricao=descricao,
            imagem=nome_imagem
        )

        produtocontroller.incluir(novo_produto)
        return jsonify({'message': 'Produto adicionado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao adicionar produto: {str(e)}'}), 500 

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/api/admin/produto/lista")
def lista_produto():
    categorias = produtocontroller.todas_categorias()
    serialized_produtos_por_categoria = {
        categoria: [produto.serialize() for produto in produtos]
        for categoria, produtos in categorias.items()
    }
    return jsonify(serialized_produtos_por_categoria)

@app.get("/api/admin/produtos/<tipo>")
def tipo_produto(tipo):
    produtos = produtocontroller.tipo_produto(tipo)
    produtos_serializados = [produto.serialize() for produto in produtos]
    return jsonify(produtos_serializados)

@app.delete("/api/admin/produto/delete/<int:id>")
def delete(id):
    produto = produtocontroller.obter(id)
    if produto:
        try:
            produtocontroller.excluir(id)
            return jsonify("Produto apagado com sucesso")
        except Exception as e:
            return jsonify(f"Erro ao excluir o produto: {str(e)}"), 500
    else:
        return jsonify("Produto não encontrado"), 404

@app.get("/api/admin/produto/<int:id>")
def produto_id(id):
    produto = produtocontroller.obter(id)
    
    if produto:
        return jsonify(produto.serialize())
    else:
        abort(404, f"Produto com ID {id} não encontrado")

@app.put("/api/admin/produto/update/<int:id>")
def update(id):
    data = request.form
    
    nome_produto = data.get('nome_produto')
    tipo_produto = data.get('tipo_produto')
    tamanhos_selecionados = data.getlist('tamanho[]')
    ingredientes_selecionados = data.getlist('ingrediente[]')
    preco = data.get('preco')
    descricao = data.get('descricao')
    imagem = request.files['imagem'] if 'imagem' in request.files else None

    tamanho = ','.join(tamanhos_selecionados)
    ingrediente = ' - '.join(ingredientes_selecionados)

    if imagem and allowed_file(imagem.filename):
        nome_imagem = secure_filename(imagem.filename)
        path_imagem = os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem)
        imagem.save(path_imagem)
    else:
        return jsonify({'message': 'Erro ao processar imagem ou imagem ausente'}), 400

    try:
        novo_produto = Produto(
            nome_produto=nome_produto,
            tipo_produto=tipo_produto,
            tamanho=tamanho,
            ingrediente=ingrediente,
            preco=float(preco),
            descricao=descricao,
            imagem=nome_imagem
        )

        produtocontroller.alterar(id, novo_produto)
        return jsonify({'message': 'Produto atualizado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'message': f'Erro ao atualizar produto: {str(e)}'}), 500

@app.post("/api/carrinho")
@login_required
def criando_carrinho():
    if current_user.is_authenticated:
        app.logger.info(f"Usuário autenticado: {current_user.id}")
       
    else:
        app.logger.info("Usuário não autenticado")
        return jsonify({"message": "Usuário não autenticado"}), 401
    
    try:        
        headers = {
            "Authorization": f"Bearer {current_user.auth_token}" 
        }
        data = request.json
        
        produto_id = data.get("produto_id")
        quantidade = int(data.get("quantidade"))
        observacao = data.get("observacao")
        
        produto = produtocontroller.get_produto_by_id(produto_id)
        
        if not produto:
            return jsonify("Produto não encontrado"), 404
        imagem_produto = produto.imagem
        preco_total = produto.preco * quantidade
        
        carrinho = Carrinho(
            usuario_id=current_user.id,  # Onde está definido o usuario_id?
            produto_id=produto_id,
            nome_produto=produto.nome_produto,
            quantidade=quantidade,
            imagem_produto=imagem_produto,
            observacao=observacao,
            preco_total=preco_total
        )
        carrinhocontroller.create(carrinho)
        return jsonify('Produto adicionado com sucesso ao carrinho'), 200
    
    except ValueError as ve:
        return jsonify(f"Erro nos dados fornecidos: {str(ve)}"), 400
    
    except Exception as e:
        return jsonify(f"Erro ao adicionar ao carrinho: {str(e)}"), 500
@app.post("/api/carrinhoDTO")
@login_required
def carrinho_dto():
    if current_user.is_authenticated:
        app.logger.info(f"Usuário autenticado: {current_user.id}")
        # Restante do código da função
    else:
        app.logger.info("Usuário não autenticado")
        return jsonify({"message": "Usuário não autenticado"}), 401
    try:
        headers = {
            "Authorization": f"Bearer {current_user.auth_token}"  # Supondo que 'auth_token' seja um campo no modelo de usuário
        }

        data = request.json
        produto_id = data.get("produto_id")
        quantidade = int(data.get("quantidade"))
        observacao = data.get("observacao")
        
        # Simulando a obtenção de um produto pelo ID
        produto = produtocontroller.get_produto_by_id(produto_id)        
        if not produto:
            return jsonify("Produto não encontrado"), 404
        
        imagem_produto = produto.imagem
        preco_total = produto.preco * quantidade
        
        carrinho_produto_dto = CarrinhoProdutoDTO(
            produto_id=produto_id,
            nome_produto=produto.nome_produto,
            quantidade=quantidade,
            observacao=observacao,
            preco_total=preco_total,
            imagem_produto=imagem_produto
        )
        
        # Simulando a criação de um carrinho
        carrinho = Carrinho(
            usuario_id=current_user.id,
            produto_id=carrinho_produto_dto.produto_id,
            nome_produto=carrinho_produto_dto.nome_produto,
            quantidade=carrinho_produto_dto.quantidade,
            imagem_produto=carrinho_produto_dto.imagem_produto,
            observacao=carrinho_produto_dto.observacao,
            preco_total=carrinho_produto_dto.preco_total
        )
        
        carrinhocontroller.create(carrinho)
        return jsonify('Produto adicionado com sucesso ao carrinho'), 200
    
    except ValueError as ve:
        return jsonify(f"Erro nos dados fornecidos: {str(ve)}"), 400
    
    except Exception as e:
        return jsonify(f"Erro ao adicionar ao carrinho: {str(e)}"), 500
@app.get("/api/carrinho/lista/<int:id>")
def lista_carrinho(id):
    itens_carrinho = carrinhocontroller.obter_itens_carrinho(id)
    return jsonify([item.serialize() for item in itens_carrinho])

@app.delete("/api/carrinho/delete/<int:carrinho_id>")
def delete_carrinho(carrinho_id):
    try:
        # Verifica se o carrinho com o ID fornecido existe
        carrinho = carrinhocontroller.obter_id(carrinho_id)

        if carrinho:
            carrinhocontroller.delete(carrinho_id)
            return jsonify("Produto removido do carrinho", "success"), 200
        else:
            return jsonify("Carrinho não encontrado"), 404

    except Exception as e:
        return jsonify(f"Erro ao deletar o carrinho: {str(e)}"), 500

@app.post("/api/pedido")
def criar_pedido():
    data = request.json

    forma_pagamento = data.get("forma_pagamento")
    observacao_item = []
    itens_comprados = []

    itens_carrinho = carrinhocontroller.obter_itens_carrinho(current_user.id)

    for item in itens_carrinho:
        descricao_item = f"{item.nome_produto}  - Observação: {item.observacao}\n"
        observacao_item.append(descricao_item)

        item_comprado = f"{item.nome_produto} - Quantidade: {item.quantidade}\n"
        itens_comprados.append(item_comprado)

    valor_total = sum(item.preco_total for item in itens_carrinho)

    usuario_data = usuariocontroller.get_usuario_by_id(current_user.id)
    endereco_completo = usuariocontroller.endereco_completo(
        usuario_data.endereco, usuario_data.numero_casa,
        usuario_data.complemento, usuario_data.bairro, usuario_data.telefone
    )

    pedido = Pedido(
        usuario_id=current_user.id,
        forma_pagamento=forma_pagamento,
        endereco_entrega=endereco_completo,
        status='Preparando',
        valor_total=valor_total,
        observacao='\n'.join(observacao_item),
        itens_comprados='\n'.join(itens_comprados)
    )

    pedido_id = pedidocontroller.create_and_delete_carrinho(pedido, current_user.id)
    
    return jsonify({"message": "Pedido Realizado com Sucesso", "pedido_id": pedido_id})

@app.get("/api/admin/pedidos/lista")
def pedidos_admin():
    pedido_lista = pedidocontroller.obter_todos_os_pedidos()
    # Serializando a lista de pedidos
    pedidos_serializados = [pedido.serialize() for pedido in pedido_lista]
    return jsonify(pedidos_serializados)

@app.get("/api/admin/painel/lista10")
def pedido10_admin():
    pedido_lista10 = pedidocontroller.obter_ultimos_10_pedido()
    # Serializando a lista de pedidos
    pedidos_serializados = [pedido.serialize() for pedido in pedido_lista10]
    return jsonify(pedidos_serializados)

@app.delete("/api/admin/pedidos/delete/<int:pedido_id>")
def delete_pedido(pedido_id):
    try:
        pedido=pedidocontroller.obter_id(pedido_id)
        if pedido:
            pedidocontroller.deletar(pedido_id)
            return jsonify("Pedido apagado com sucesso","success"),200
        else:
            return jsonify("Pedido não encontrado"), 404

    except Exception as e:
        return jsonify(f"Erro ao deletar o carrinho: {str(e)}"), 500

@app.put("/api/admin/pedidos/update")
def atualizar_pedido():
    try:
        data = request.get_json()
        pedido_id = data.get('pedido_id')
        novo_status = data.get('novo_status')
        
        if not pedido_id or not novo_status:
            return jsonify({"error": "pedido_id e novo_status são obrigatórios"}), 400
        
        atualizado = pedidocontroller.atualizar_status_pedido(pedido_id, novo_status)
        
        if atualizado:
            return jsonify({"message": "Status do pedido atualizado com sucesso"}), 200
        else:
            return jsonify({"error": "Pedido não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.get("/api/pedidos/<int:usuario_id>")
def pedido_usuario(usuario_id):
    try:
        pedido_usuario = pedidocontroller.obter_pedidos_por_usuario_id(usuario_id)
        pedidos_serializados = [pedido.serialize() for pedido in pedido_usuario]
        return jsonify(pedidos_serializados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/admin/painel")
def media():
    media = pedidocontroller.calcular_media_dos_pedidos()
    total = pedidocontroller.calcular_valor_total_dos_pedidos()
    quantidade = pedidocontroller.contar_quantidade_de_pedidos()
    
    response = {
        "TKM": f"R$: {media}",
        "Total de Venda": f"R$: {total}",
        "Quantidade de Pedidos": quantidade
    }
    
    return jsonify(response)
# Rota para logout de usuários

if __name__ == '__main__':
    # Criação das tabelas no banco de dados
    with app.app_context():
        print("Criando tabelas no banco de dados...")
        db.create_all()
        print("Tabelas criadas com sucesso.")
    
    # Instanciando os controladores dentro do contexto da aplicação
    with app.app_context():
        usuariocontroller = UsuarioController()
        produtocontroller = ProdutoController()
        admincontroller = AdminController()
        carrinhocontroller = CarrinhoController()
        pedidocontroller = PedidoController()

    # Execução do aplicativo Flask
    app.run(debug=True, port=8000)
