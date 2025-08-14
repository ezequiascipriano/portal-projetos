from app import app, db, Perfil, Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

def recreate_database():
    with app.app_context():
        # Remover todas as tabelas existentes
        db.drop_all()
        
        # Criar todas as tabelas novamente
        db.create_all()
        
        # Criar perfis padrão
        perfil_admin = Perfil(
            nome='ADMIN',
            descricao='Administrador do sistema'
        )
        perfil_usuario = Perfil(
            nome='USUARIO',
            descricao='Usuário padrão'
        )
        
        db.session.add(perfil_admin)
        db.session.add(perfil_usuario)
        db.session.commit()
        
        # Criar usuário admin padrão
        admin = Usuario(
            id_perfil=perfil_admin.id_perfil,
            login='admin',
            nome_completo='Administrador do Sistema',
            email='admin@sistema.com',
            senha=generate_password_hash('admin'),
            status='ATIVO'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Banco de dados recriado com sucesso!")
        print("Usuário admin criado:")
        print("Login: admin")
        print("Senha: admin")

if __name__ == '__main__':
    recreate_database()

