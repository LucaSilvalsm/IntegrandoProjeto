# controller/page_controller.py
from flask import Blueprint, render_template, flash, redirect, url_for, session,request,current_app
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from ProdutoIntegracao import ProdutoNet
from UsuarioIntegracao import UsuarioNet

page_bp = Blueprint('page_bp', __name__)
produtoNet= ProdutoNet()

@page_bp.route('/')
def index():
    print("Acessando a rota /")
    
    artesanais = produtoNet.obter_por_tipo("Artesanal")
    tradicionais = produtoNet.obter_por_tipo("Tradicional")
    bebidas = produtoNet.obter_por_tipo("Bebida")
    porcao = produtoNet.obter_por_tipo("Porcao")
   
    return render_template("index.html", artesanais=artesanais, tradicionais=tradicionais, bebidas=bebidas, porcao=porcao)


@page_bp.route("/teste")
def teste():
    if current_user.is_authenticated:
        return f"Usuário autenticado: {current_user.email}"
    else:
        return "Nenhum usuário autenticado"

@page_bp.route("/login")
def login():
    

    # Se o método HTTP for GET, renderize o formulário de login
    return render_template('login.html')



@page_bp.route("/cadastro/usuario")
def cadastro():
    print("Acessando a rota /cadastro")
    return render_template('cadastro.html')

@page_bp.route("/admin/login")
def login_admin():
    return render_template ('login_adm.html')

@page_bp.route("/admin/painel")
def painel():
    return render_template ("./admin/painel.html")


@page_bp.route("/admin/cadastro_admin")
def cadastro_login():
    return render_template('cadastro_admin.html')

@page_bp.route("/admin/produto")
def admin_newproduto():
    return render_template("/admin/newproduto.html")

@page_bp.route("/produto/<int:produto_id>", methods=['GET'])
@login_required
def detalhes_produto(produto_id):
    produtoNet = ProdutoNet()
    produto = produtoNet.get_id(produto_id)
    if not produto:
        return render_template('produto_nao_encontrado.html')
    
    return render_template('detalhes_produto.html', produto=produto)

@page_bp.route("/admin/allProdutos")
def all_produtos():
    
    produtoNet = ProdutoNet()  # Instanciação correta do ProdutoNet
    produtos = produtoNet.obter_todos()
    print("Acessando a rota /admin/allProdutos")
    print("os produtos sao: ",produtos)
    return render_template('/admin/all_produtos.html',produtos=produtos)
    