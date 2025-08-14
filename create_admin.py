from app import app, db, Usuario, Perfil
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # Verifica se o perfil ADMIN existe
        perfil_admin = Perfil.query.filter_by(nome='ADMIN').first()
        if not perfil_admin:
            perfil_admin = Perfil(nome='ADMIN', descricao='Administrador com acesso total ao sistema')
            db.session.add(perfil_admin)
            db.session.commit()
            print("Perfil ADMIN criado com sucesso!")

        # Verifica se o usuário admin já existe
        admin = Usuario.query.filter_by(login='admin').first()
        if not admin:
            admin = Usuario(
                id_perfil=perfil_admin.id_perfil,
                login='admin',
                nome_completo='Administrador do Sistema',
                email='admin@empresa.com',
                senha=generate_password_hash('admin@123'),
                status='ATIVO'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe!")

if __name__ == '__main__':
    create_admin() 