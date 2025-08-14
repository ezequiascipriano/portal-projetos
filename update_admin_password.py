from app import app, db, Usuario
from werkzeug.security import generate_password_hash

def update_admin_password():
    with app.app_context():
        admin = Usuario.query.filter_by(login='admin').first()
        if admin:
            admin.senha = generate_password_hash('admin@123')
            db.session.commit()
            print("Senha do admin atualizada com sucesso!")
        else:
            print("Usuário admin não encontrado!")

if __name__ == '__main__':
    update_admin_password() 