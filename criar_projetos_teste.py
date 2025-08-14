from app import app, db, Projeto, Usuario
from datetime import datetime
import pytz

timezone = pytz.timezone('America/Sao_Paulo')

def criar_projetos_teste():
    with app.app_context():
        # Verificar se já existem projetos
        if Projeto.query.count() > 0:
            print("Projetos de teste já existem!")
            return
        
        # Buscar usuário admin
        admin = Usuario.query.filter_by(login='admin').first()
        if not admin:
            print("Usuário admin não encontrado!")
            return
        
        # Lista de projetos de teste
        projetos_teste = [
            {
                'codigo_projeto': 'PROJ001',
                'nome_projeto': 'Portal de Projetos',
                'controle_economico': 'CE001',
                'numero_iniciativa': 'NI001',
                'situacao_projeto': 'ATIVO'
            },
            {
                'codigo_projeto': 'PROJ002',
                'nome_projeto': 'Sistema de Gestão',
                'controle_economico': 'CE002',
                'numero_iniciativa': 'NI002',
                'situacao_projeto': 'ATIVO'
            },
            {
                'codigo_projeto': 'PROJ003',
                'nome_projeto': 'Aplicativo Mobile',
                'controle_economico': 'CE003',
                'numero_iniciativa': 'NI003',
                'situacao_projeto': 'CONCLUIDO'
            },
            {
                'codigo_projeto': 'PROJ004',
                'nome_projeto': 'Migração de Dados',
                'controle_economico': 'CE004',
                'numero_iniciativa': 'NI004',
                'situacao_projeto': 'CANCELADO'
            }
        ]
        
        # Criar projetos
        for dados_projeto in projetos_teste:
            projeto = Projeto(
                codigo_projeto=dados_projeto['codigo_projeto'],
                nome_projeto=dados_projeto['nome_projeto'],
                controle_economico=dados_projeto['controle_economico'],
                numero_iniciativa=dados_projeto['numero_iniciativa'],
                situacao_projeto=dados_projeto['situacao_projeto'],
                id_usuario_criacao=admin.id_usuario,
                id_usuario_ultima_atualizacao=admin.id_usuario,
                data_criacao=datetime.now(timezone),
                data_ultima_atualizacao=datetime.now(timezone)
            )
            db.session.add(projeto)
        
        try:
            db.session.commit()
            print("Projetos de teste criados com sucesso!")
            print(f"\nTotal de projetos criados: {len(projetos_teste)}")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar projetos: {str(e)}")

if __name__ == '__main__':
    criar_projetos_teste()
