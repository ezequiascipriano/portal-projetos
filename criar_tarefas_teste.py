from app import app, db, Projeto, Usuario, Tarefa
from datetime import datetime, timedelta
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

def criar_tarefas_teste():
    with app.app_context():
        # Verificar se já existem tarefas
        if Tarefa.query.count() > 0:
            print("Tarefas de teste já existem!")
            return
        
        # Buscar projetos e usuários
        projetos = Projeto.query.all()
        usuarios = Usuario.query.filter_by(status='ATIVO').all()
        
        if not projetos:
            print("Nenhum projeto encontrado!")
            return
        
        if not usuarios:
            print("Nenhum usuário encontrado!")
            return
        
        # Lista de tarefas de teste
        tarefas_teste = [
            {
                'titulo': 'Desenvolver interface do usuário',
                'descricao': 'Criar as telas principais do sistema com Bootstrap e responsividade',
                'prioridade': 'ALTA',
                'status': 'EM_ANDAMENTO',
                'projeto': projetos[0] if projetos else None,
                'responsavel': usuarios[0] if usuarios else None,
                'data_limite': datetime.now(timezone).date() + timedelta(days=7)
            },
            {
                'titulo': 'Configurar banco de dados',
                'descricao': 'Implementar as migrações e configurações do SQLAlchemy',
                'prioridade': 'ALTA',
                'status': 'CONCLUIDA',
                'projeto': projetos[0] if projetos else None,
                'responsavel': usuarios[0] if usuarios else None,
                'data_limite': datetime.now(timezone).date() - timedelta(days=2)
            },
            {
                'titulo': 'Implementar autenticação',
                'descricao': 'Sistema de login e controle de acesso com Flask-Login',
                'prioridade': 'MÉDIA',
                'status': 'PENDENTE',
                'projeto': projetos[0] if projetos else None,
                'responsavel': usuarios[1] if len(usuarios) > 1 else None,
                'data_limite': datetime.now(timezone).date() + timedelta(days=14)
            },
            {
                'titulo': 'Criar documentação técnica',
                'descricao': 'Documentar APIs e funcionalidades do sistema',
                'prioridade': 'BAIXA',
                'status': 'PENDENTE',
                'projeto': projetos[0] if projetos else None,
                'responsavel': None,
                'data_limite': datetime.now(timezone).date() + timedelta(days=30)
            },
            {
                'titulo': 'Testes de integração',
                'descricao': 'Implementar testes automatizados para as principais funcionalidades',
                'prioridade': 'MÉDIA',
                'status': 'PENDENTE',
                'projeto': projetos[0] if projetos else None,
                'responsavel': usuarios[2] if len(usuarios) > 2 else None,
                'data_limite': datetime.now(timezone).date() + timedelta(days=21)
            }
        ]
        
        # Criar tarefas
        for dados_tarefa in tarefas_teste:
            if dados_tarefa['projeto']:
                tarefa = Tarefa(
                    titulo=dados_tarefa['titulo'],
                    descricao=dados_tarefa['descricao'],
                    prioridade=dados_tarefa['prioridade'],
                    status=dados_tarefa['status'],
                    id_projeto=dados_tarefa['projeto'].id_projeto,
                    id_usuario_responsavel=dados_tarefa['responsavel'].id_usuario if dados_tarefa['responsavel'] else None,
                    id_usuario_criacao=usuarios[0].id_usuario,
                    id_usuario_ultima_atualizacao=usuarios[0].id_usuario,
                    data_criacao=datetime.now(timezone),
                    data_ultima_atualizacao=datetime.now(timezone),
                    data_limite=dados_tarefa['data_limite'],
                    data_conclusao=datetime.now(timezone) if dados_tarefa['status'] == 'CONCLUIDA' else None
                )
                db.session.add(tarefa)
        
        try:
            db.session.commit()
            print("Tarefas de teste criadas com sucesso!")
            print(f"\nTotal de tarefas criadas: {len(tarefas_teste)}")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar tarefas: {str(e)}")

if __name__ == '__main__':
    criar_tarefas_teste()
