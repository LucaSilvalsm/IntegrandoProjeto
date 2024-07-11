from flask import Blueprint,redirect,url_for,flash
from flask_login import login_user, current_user,logout_user



user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/logout')
def logout():
    # Utiliza o método do Flask-Login para deslogar o usuário
    logout_user()

    # Flash message opcional para informar o usuário que ele foi deslogado com sucesso
    flash('Você foi deslogado com sucesso.', 'success')

    # Redireciona para a página de login, ou para onde desejar após o logout
    return redirect(url_for('page_bp.login'))