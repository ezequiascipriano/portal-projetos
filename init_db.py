from app import app, db, Perfil, Usuario, Projeto, Incidente
from werkzeug.security import generate_password_hash
import os
import pytz
from datetime import datetime

def init_db():
    # Criar o banco de dados e todas as tabelas
    with app.app_context():
        # Remover o banco de dados se existir
        if os.path.exists('portal_projetos.db'):
            os.remove('portal_projetos.db')
        
        # Criar todas as tabelas
        db.create_all()
        
        # Configurar timezone para Brasília
        timezone = pytz.timezone('America/Sao_Paulo')
        data_atual = datetime.now(timezone)
        
        # Criar perfis padrão
        admin_perfil = db.session.query(Perfil).filter_by(nome='ADMIN').first()
        if not admin_perfil:
            admin_perfil = Perfil(
                nome='ADMIN',
                descricao='Administrador do sistema'
            )
            db.session.add(admin_perfil)
        
        usuario_perfil = db.session.query(Perfil).filter_by(nome='USUARIO').first()
        if not usuario_perfil:
            usuario_perfil = Perfil(
                nome='USUARIO',
                descricao='Usuário comum'
            )
            db.session.add(usuario_perfil)
        
        # Criar usuário admin padrão
        admin = db.session.query(Usuario).filter_by(login='admin').first()
        if not admin:
            admin = Usuario(
                id_perfil=1,  # ID do perfil ADMIN
                login='admin',
                nome_completo='Administrador do Sistema',
                email='admin@portalprojetos.com',
                senha=generate_password_hash('admin123'),
                status='ATIVO'
            )
            db.session.add(admin)
        
        # Criar um projeto de exemplo
        projeto = db.session.query(Projeto).filter_by(codigo_projeto='PRJ000001').first()
        if not projeto:
            projeto = Projeto(
                id_projeto=1,
                codigo_projeto='PRJ000001',
                nome_projeto='Projeto de Exemplo',
                controle_economico='CE001',
                numero_iniciativa='INI001',
                situacao_projeto='ATIVO',
                id_usuario_criacao=1,
                id_usuario_ultima_atualizacao=1,
                data_ultima_atualizacao=data_atual
            )
            db.session.add(projeto)
        
        # Criar um incidente de exemplo
        incidente = db.session.query(Incidente).filter_by(titulo='Incidente de Exemplo').first()
        if not incidente:
            incidente = Incidente(
                id_projeto=1,
                titulo='Incidente de Exemplo',
                descricao='Este é um incidente de exemplo criado durante a inicialização do banco de dados.',
                prioridade='MÉDIA',
                status='ABERTO',
                id_usuario_criacao=1,
                id_usuario_ultima_atualizacao=1,
                data_ultima_atualizacao=data_atual
            )
            db.session.add(incidente)
        
        # Commit das alterações
        db.session.commit()
        print('Banco de dados inicializado com sucesso!')

if __name__ == '__main__':
    init_db() 