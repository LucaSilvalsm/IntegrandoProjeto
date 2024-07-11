from flask import Flask, render_template, request, redirect, flash, url_for, session,current_app,jsonify

from Classes.Usuario import Usuario
from Classes.UsuarioAdmin import UsuarioAdmin
from Classes.Produto import Produto
from Classes.Carrinho import Carrinho
from Classes.CarrinhoProdutoDTO import CarrinhoProdutoDTO
from UsuarioIntegracao import UsuarioNet
from AdminIntegracao import AdminNet
from ProdutoIntegracao import ProdutoNet
from CarrinhoIntegracao import CarrinhoNet
from page_controller import page_bp
from user_controller import user_bp
from werkzeug.utils import secure_filename

from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_session import Session
import secrets
import os
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = 'static/img/produtos'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'img', 'produtos')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração da chave secreta
app.secret_key = secrets.token_hex(24)

print(f"O código é: {app.secret_key}")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuração da sessão
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

usuarioNet = UsuarioNet()
adminNet = AdminNet()
produtoNet= ProdutoNet()
carrinhoNet = CarrinhoNet()

@login_manager.user_loader
def load_user(user_id):
    usuario = usuarioNet.get_usuario_by_id(user_id)
    if not usuario:
        usuario = adminNet.get_usuario_by_id(user_id)
    return usuario

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(page_bp, name='page_bp')

@app.post("/usuario/cadastro")
def incluir():
    try:
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        senha = request.form["senha"]
       
        endereco = request.form["endereco"]
        numero_casa = request.form["numero_casa"]
        complemento = request.form["complemento"]
        bairro = request.form["bairro"]

        # Verificar se o e-mail já está sendo utilizado
        if usuarioNet.obter_por_email(email):
            flash('Este email já está sendo utilizado.', 'error')
            return render_template("login.html")

        # Verificar se as senhas coincidem
       
        # Criar objeto de usuário e realizar a inclusão
        usuario = Usuario(nome, sobrenome, telefone, email, senha, endereco, numero_casa, complemento, bairro)
        novo_usuario = usuarioNet.incluir(usuario)

        if novo_usuario:
            login_user(novo_usuario)
            session['user_id'] = novo_usuario.id
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('page_bp.index'))

        flash('Erro ao cadastrar usuário.', 'error')
        return render_template("login.html")

    except Exception as e:
        flash(f'Erro ao adicionar usuário: {str(e)}', 'error')
        return render_template("login.html")

@app.post("/usuario/login/")
def login_usuario():
    email = request.form['email']
    senha = request.form['senha']

    usuario = usuarioNet.login(email=email, senha=senha)
    if usuario:
        login_user(usuario)
        session['user_id'] = usuario.id
        app.logger.info(f"Usuário {usuario.email} logado com sucesso. ID na sessão: {session.get('user_id')}")
            
        app.logger.info(f"Sessão do usuário: {session}")
        flash('Login realizado com sucesso!', 'success')

        return redirect(url_for('page_bp.index'))
    else:
        flash('Credenciais inválidas. Verifique seu email e senha.', 'error')
    
    return render_template('login.html')

@app.post("/admin/cadastro")
def admin_cadastro():
    try:
        nome = request.form["nome"]
        sobrenome = request.form["sobrenome"]
        email = request.form["email"]
        senha = request.form["senha"]   

        # Criar objeto de usuário e realizar a inclusão
        novo_admin = UsuarioAdmin(nome=nome, sobrenome=sobrenome, email=email, senha=senha)
        novo_usuario = adminNet.incluir(novo_admin)

        if novo_usuario:
            login_user(novo_usuario)
            session['user_id'] = novo_usuario.id
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('page_bp.admin/painel'))

        flash('Erro ao cadastrar usuário.', 'error')
        return render_template("login.html")

    except Exception as e:
        flash(f'Erro ao adicionar usuário: {str(e)}', 'error')
        return render_template("login.html")
    
@app.post("/admin/login")
def login_admin():
    email = request.form['email']
    senha = request.form['senha']

    usuarioAdmin = adminNet.login(email=email, senha=senha)
    if usuarioAdmin:
        login_user(usuarioAdmin)
        session['user_id'] = usuarioAdmin.id
        flash('Login realizado com sucesso!', 'success')

        return redirect(url_for('page_bp.painel'))
    else:
        flash('Credenciais inválidas. Verifique seu email e senha.', 'error')
    
    return render_template('login.html')


produtoNet = ProdutoNet()

@app.post("/admin/newproduto")
def new_produto():
    try:
        # Obter os dados do formulário
        nome_produto = request.form['nome']
        tipo_produto = request.form['tipoProdutos']

        # Processar tamanhos selecionados
        tamanhos_selecionados = request.form.getlist('tamanho[]')
        tamanho = ','.join(tamanhos_selecionados)

        # Processar ingredientes selecionados
        ingredientes_selecionados = request.form.getlist('ingrediente[]')
        ingrediente = ' - '.join(ingredientes_selecionados)

        preco = request.form['preco']
        descricao = request.form['descricao']
        imagem = request.files['image'] if 'image' in request.files else None

        # Processar o arquivo de imagem e definir o nome da imagem
        if imagem and allowed_file(imagem.filename):
            nome_imagem = secure_filename(imagem.filename)
            path_imagem = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_imagem)
            print(f'Saving image to: {path_imagem}')  # Debug: verificar o caminho da imagem
            imagem.save(path_imagem)
        else:
            flash('Erro ao processar imagem', 'error')
            return redirect(url_for('page_bp.admin_newproduto'))

        # Criar um novo objeto Produto com todos os dados
        novo_produto = Produto(
            nome_produto=nome_produto,
            tipo_produto=tipo_produto,
            tamanho=tamanho,
            ingrediente=ingrediente,
            preco=float(preco),
            descricao=descricao,
            imagem=nome_imagem
        )

        # Incluir o novo produto no banco de dados
        produto_inserido = produtoNet.incluir(novo_produto, path_imagem)  # Fornecendo o caminho da imagem

        flash('Produto adicionado com sucesso!', 'success')

        return redirect(url_for('page_bp.admin_newproduto'))

    except Exception as e:
        flash(f'Erro ao adicionar produto: {str(e)}', 'error')
        return redirect(url_for('page_bp.admin_newproduto'))



@app.post("/admin/produto/delete/")
def excluir():
    try:
        produto_id = request.form['id']
        produtoNet = ProdutoNet()  # Instanciação do ProdutoNet
        resposta = produtoNet.excluir(produto_id)

        if resposta == "Produto removido com sucesso":
            flash(f'Produto ID {produto_id} removido com sucesso', 'success')
        elif resposta == "Produto não encontrado":
            flash(f'Produto ID {produto_id} não encontrado para exclusão', 'error')
        else:
            flash(f'Erro ao excluir o produto ID {produto_id}: {resposta}', 'error')

        # Redireciona de volta para a página de todos os produtos após a exclusão
        return redirect(url_for('page_bp.all_produtos'))

    except Exception as e:
        flash(f'Erro ao excluir produto: {str(e)}', 'error')
        return redirect(url_for('page_bp.all_produtos')) 
@app.post("/carrinhoDTO")
@login_required
def carrinho_dto():
    if current_user.is_authenticated:
        app.logger.info(f"""
            Usuário autenticado:
            ID: {current_user.id}
        """)                
    else:
        app.logger.info("Usuário não autenticado")
    try:
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        observacao = request.form.get('observacao', '')
        produto = produtoNet.get_id(produto_id)
        if not produto:
            flash('Produto não encontrado', 'error')
            return redirect(url_for('index'))
        preco_total = float(produto.preco) * quantidade
        carrinho_produto_dto = CarrinhoProdutoDTO(
            produto_id=produto_id,
            nome_produto=produto.nome_produto,
            quantidade=quantidade,
            observacao=observacao,
            preco_total=preco_total,
            imagem_produto=produto.imagem
        )
        carrinho = Carrinho(
            usuario_id=current_user.id,
            produto_id=carrinho_produto_dto.produto_id,
            nome_produto=carrinho_produto_dto.nome_produto,
            quantidade=carrinho_produto_dto.quantidade,
            observacao=carrinho_produto_dto.observacao,
            preco_total=carrinho_produto_dto.preco_total,
            imagem_produto=carrinho_produto_dto.imagem_produto
        )
        print(f"""
            produto_id: {produto_id}, 
            quantidade: {quantidade}, 
            observacao: {observacao}
        """)

        print(f"""
            ID do usuário: {current_user.id}, 
            nome do produto: {produto.nome_produto}, 
            preco_total: {preco_total}
        """)

        print(f"""
            Carrinho a ser salvo: {carrinho.serialize()}
        """)

        resposta, status_code = carrinhoNet.criar_carrinho(carrinho)
        if status_code == 200:
            flash('Produto adicionado ao carrinho com sucesso!', 'success')
        else:
            flash(f'Erro ao adicionar produto ao carrinho: {resposta}', 'error')

        return redirect(url_for('page_bp.index'))
    
    except Exception as e:
        flash(f'Erro ao processar a requisição: {str(e)}', 'error')
        return redirect(url_for('page_bp.index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8008)
