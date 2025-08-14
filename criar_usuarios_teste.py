from app import app, db, Perfil, Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

def criar_usuarios_teste():
    with app.app_context():
        # Verificar se já existem usuários além do admin
        if Usuario.query.count() > 1:
            print("Usuários de teste já existem!")
            return
        
        # Buscar perfis
        perfil_admin = Perfil.query.filter_by(nome='ADMIN').first()
        perfil_usuario = Perfil.query.filter_by(nome='USUARIO').first()
        
        if not perfil_admin or not perfil_usuario:
            print("Perfis não encontrados!")
            return
        
        # Lista de usuários de teste
        usuarios_teste = [
            {
                'id_perfil': perfil_usuario.id_perfil,
                'login': 'joao.silva',
                'nome_completo': 'João Silva',
                'email': 'joao.silva@empresa.com',
                'senha': '123456',
                'status': 'ATIVO'
            },
            {
                'id_perfil': perfil_usuario.id_perfil,
                'login': 'maria.santos',
                'nome_completo': 'Maria Santos',
                'email': 'maria.santos@empresa.com',
                'senha': '123456',
                'status': 'ATIVO'
            },
            {
                'id_perfil': perfil_admin.id_perfil,
                'login': 'pedro.admin',
                'nome_completo': 'Pedro Administrador',
                'email': 'pedro.admin@empresa.com',
                'senha': '123456',
                'status': 'ATIVO'
            },
            {
                'id_perfil': perfil_usuario.id_perfil,
                'login': 'ana.oliveira',
                'nome_completo': 'Ana Oliveira',
                'email': 'ana.oliveira@empresa.com',
                'senha': '123456',
                'status': 'INATIVO'
            },
            {
                'id_perfil': perfil_usuario.id_perfil,
                'login': 'carlos.lima',
                'nome_completo': 'Carlos Lima',
                'email': 'carlos.lima@empresa.com',
                'senha': '123456',
                'status': 'ATIVO'
            }
        ]
        
        # Criar usuários
        for dados_usuario in usuarios_teste:
            usuario = Usuario(
                id_perfil=dados_usuario['id_perfil'],
                login=dados_usuario['login'],
                nome_completo=dados_usuario['nome_completo'],
                email=dados_usuario['email'],
                senha=generate_password_hash(dados_usuario['senha']),
                status=dados_usuario['status']
            )
            db.session.add(usuario)
        
        try:
            db.session.commit()
            print("Usuários de teste criados com sucesso!")
            print("\nUsuários criados:")
            for dados in usuarios_teste:
                print(f"- {dados['nome_completo']} ({dados['login']}) - Senha: {dados['senha']}")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuários: {str(e)}")

if __name__ == '__main__':
    criar_usuarios_teste()
