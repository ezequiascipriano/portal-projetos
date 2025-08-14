from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal_projetos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configurar timezone para Brasília
timezone = pytz.timezone('America/Sao_Paulo')

class Perfil(db.Model):
    __tablename__ = 'Perfis'
    
    id_perfil = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone))
    
    usuarios = db.relationship('Usuario', backref='perfil', lazy=True)

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey('Perfis.id_perfil'), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone))
    ultimo_login = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='ATIVO')
    
    projetos_criados = db.relationship('Projeto', backref='criador', lazy=True, foreign_keys='Projeto.id_usuario_criacao')
    projetos_atualizados = db.relationship('Projeto', backref='atualizador', lazy=True, foreign_keys='Projeto.id_usuario_ultima_atualizacao')
    
    def get_id(self):
        return str(self.id_usuario)

class Projeto(db.Model):
    __tablename__ = 'Projetos'
    
    id_projeto = db.Column(db.Integer, primary_key=True)
    id_usuario_criacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_usuario_ultima_atualizacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    codigo_projeto = db.Column(db.String(10), unique=True, nullable=False)
    nome_projeto = db.Column(db.String(100), nullable=False)
    controle_economico = db.Column(db.String(50), nullable=False)
    numero_iniciativa = db.Column(db.String(50), nullable=False)
    situacao_projeto = db.Column(db.String(20), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone))
    data_ultima_atualizacao = db.Column(db.DateTime)

class Incidente(db.Model):
    __tablename__ = 'Incidentes'
    
    id_incidente = db.Column(db.Integer, primary_key=True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('Projetos.id_projeto'), nullable=False)
    id_usuario_criacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_usuario_ultima_atualizacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)  # ALTA, MÉDIA, BAIXA
    status = db.Column(db.String(20), nullable=False)  # ABERTO, EM_ANÁLISE, EM_ANDAMENTO, RESOLVIDO, FECHADO
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone))
    data_ultima_atualizacao = db.Column(db.DateTime)
    data_resolucao = db.Column(db.DateTime)
    
    projeto = db.relationship('Projeto', backref='incidentes')
    criador = db.relationship('Usuario', foreign_keys=[id_usuario_criacao], backref='incidentes_criados')
    atualizador = db.relationship('Usuario', foreign_keys=[id_usuario_ultima_atualizacao], backref='incidentes_atualizados')

class Tarefa(db.Model):
    __tablename__ = 'Tarefas'
    
    id_tarefa = db.Column(db.Integer, primary_key=True)
    id_projeto = db.Column(db.Integer, db.ForeignKey('Projetos.id_projeto'), nullable=False)
    id_usuario_criacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), nullable=False)
    id_usuario_ultima_atualizacao = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    id_usuario_responsavel = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)  # ALTA, MÉDIA, BAIXA
    status = db.Column(db.String(20), nullable=False)  # PENDENTE, EM_ANDAMENTO, CONCLUIDA, CANCELADA
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone))
    data_ultima_atualizacao = db.Column(db.DateTime)
    data_limite = db.Column(db.Date)
    data_conclusao = db.Column(db.DateTime)
    
    projeto = db.relationship('Projeto', backref='tarefas')
    criador = db.relationship('Usuario', foreign_keys=[id_usuario_criacao], backref='tarefas_criadas')
    atualizador = db.relationship('Usuario', foreign_keys=[id_usuario_ultima_atualizacao], backref='tarefas_atualizadas')
    responsavel = db.relationship('Usuario', foreign_keys=[id_usuario_responsavel], backref='tarefas_responsavel')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.before_request
def auto_login_admin():
    from flask_login import login_user
    if not hasattr(g, 'auto_login_done'):
        admin = Usuario.query.filter_by(login='admin').first()
        if admin:
            login_user(admin)
            g.auto_login_done = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(login=login).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            usuario.ultimo_login = datetime.now(timezone)
            db.session.commit()
            return redirect(url_for('index'))
        flash('Login ou senha inválidos', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/projetos')
@login_required
def listar_projetos():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Filtros
    situacao = request.args.get('situacao', '')
    search = request.args.get('search', '')
    
    # Query base
    query = Projeto.query
    
    # Aplicar filtros
    if situacao:
        query = query.filter(Projeto.situacao_projeto == situacao)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Projeto.codigo_projeto.ilike(search_term),
                Projeto.nome_projeto.ilike(search_term)
            )
        )
    
    # Ordenar por data de última atualização (nulls last)
    query = query.order_by(Projeto.data_ultima_atualizacao.desc().nullslast())
    
    # Paginação
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    projetos = pagination.items
    
    return render_template('projetos.html', 
                         projetos=projetos, 
                         pagination=pagination)

@app.route('/projetos/novo', methods=['GET', 'POST'])
@login_required
def criar_projeto():
    if request.method == 'POST':
        try:
            data_atual = datetime.now(timezone)
            projeto = Projeto(
                codigo_projeto=request.form['codigo_projeto'],
                nome_projeto=request.form['nome_projeto'],
                controle_economico=request.form['controle_economico'],
                numero_iniciativa=request.form['numero_iniciativa'],
                situacao_projeto=request.form['situacao_projeto'],
                id_usuario_criacao=current_user.id_usuario,
                id_usuario_ultima_atualizacao=current_user.id_usuario,
                data_ultima_atualizacao=data_atual
            )
            
            db.session.add(projeto)
            db.session.commit()
            flash('Projeto criado com sucesso!', 'success')
            return redirect(url_for('listar_projetos'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Erro ao criar projeto: {str(e)}')
            flash('Erro ao criar projeto. Verifique se o código do projeto já existe.', 'danger')
    
    return render_template('projeto_form.html', titulo='Novo Projeto')

@app.route('/projetos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    
    if request.method == 'POST':
        projeto.codigo_projeto = request.form['codigo_projeto']
        projeto.nome_projeto = request.form['nome_projeto']
        projeto.controle_economico = request.form['controle_economico']
        projeto.numero_iniciativa = request.form['numero_iniciativa']
        projeto.situacao_projeto = request.form['situacao_projeto']
        projeto.id_usuario_ultima_atualizacao = current_user.id_usuario
        projeto.data_ultima_atualizacao = datetime.now(timezone)
        
        try:
            db.session.commit()
            flash('Projeto atualizado com sucesso!', 'success')
            return redirect(url_for('listar_projetos'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar projeto. Verifique se o código do projeto ou controle econômico já existem.', 'danger')
    
    return render_template('projeto_form.html', titulo='Editar Projeto', projeto=projeto)

@app.route('/projetos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    
    try:
        db.session.delete(projeto)
        db.session.commit()
        flash('Projeto excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir projeto.', 'danger')
    
    return redirect(url_for('listar_projetos'))

@app.route('/projetos/<int:id>')
@login_required
def visualizar_projeto(id):
    projeto = Projeto.query.get_or_404(id)
    tarefas = Tarefa.query.filter_by(id_projeto=id).order_by(Tarefa.data_criacao.desc()).all()
    incidentes = Incidente.query.filter_by(id_projeto=id).order_by(Incidente.data_criacao.desc()).all()
    
    return render_template('projeto_detalhes.html', projeto=projeto, tarefas=tarefas, incidentes=incidentes)

@app.route('/api/dashboard/stats')
@login_required
def dashboard_stats():
    # Estatísticas de Projetos
    total_projetos = Projeto.query.count()
    projetos_ativos = Projeto.query.filter_by(situacao_projeto='ATIVO').count()
    projetos_concluidos = Projeto.query.filter_by(situacao_projeto='CONCLUIDO').count()
    projetos_cancelados = Projeto.query.filter_by(situacao_projeto='CANCELADO').count()
    
    hoje = datetime.now(timezone).date()
    atualizacoes_hoje = Projeto.query.filter(
        Projeto.data_ultima_atualizacao.isnot(None),
        db.func.date(Projeto.data_ultima_atualizacao) == hoje
    ).count()
    
    # Estatísticas de Incidentes
    total_incidentes = Incidente.query.count()
    incidentes_abertos = Incidente.query.filter_by(status='ABERTO').count()
    incidentes_em_analise = Incidente.query.filter_by(status='EM_ANÁLISE').count()
    incidentes_em_andamento = Incidente.query.filter_by(status='EM_ANDAMENTO').count()
    incidentes_resolvidos = Incidente.query.filter_by(status='RESOLVIDO').count()
    incidentes_fechados = Incidente.query.filter_by(status='FECHADO').count()
    
    # Incidentes por Prioridade
    incidentes_alta = Incidente.query.filter_by(prioridade='ALTA').count()
    incidentes_media = Incidente.query.filter_by(prioridade='MÉDIA').count()
    incidentes_baixa = Incidente.query.filter_by(prioridade='BAIXA').count()
    
    # Últimos Projetos
    ultimos_projetos = Projeto.query.order_by(Projeto.data_ultima_atualizacao.desc().nullslast()).limit(5).all()
    projetos_recentes = []
    for projeto in ultimos_projetos:
        projetos_recentes.append({
            'codigo_projeto': projeto.codigo_projeto,
            'nome_projeto': projeto.nome_projeto,
            'situacao_projeto': projeto.situacao_projeto,
            'data_ultima_atualizacao': projeto.data_ultima_atualizacao
        })
    
    # Últimos Incidentes
    ultimos_incidentes = Incidente.query.order_by(Incidente.data_ultima_atualizacao.desc().nullslast()).limit(5).all()
    incidentes_recentes = []
    for incidente in ultimos_incidentes:
        incidentes_recentes.append({
            'titulo': incidente.titulo,
            'projeto': {
                'codigo_projeto': incidente.projeto.codigo_projeto,
                'nome_projeto': incidente.projeto.nome_projeto
            },
            'status': incidente.status,
            'data_ultima_atualizacao': incidente.data_ultima_atualizacao
        })
    
    return jsonify({
        # Estatísticas de Projetos
        'total_projetos': total_projetos,
        'projetos_ativos': projetos_ativos,
        'projetos_concluidos': projetos_concluidos,
        'projetos_cancelados': projetos_cancelados,
        'atualizacoes_hoje': atualizacoes_hoje,
        
        # Estatísticas de Incidentes
        'total_incidentes': total_incidentes,
        'incidentes_abertos': incidentes_abertos,
        'incidentes_em_analise': incidentes_em_analise,
        'incidentes_em_andamento': incidentes_em_andamento,
        'incidentes_resolvidos': incidentes_resolvidos,
        'incidentes_fechados': incidentes_fechados,
        'incidentes_alta': incidentes_alta,
        'incidentes_media': incidentes_media,
        'incidentes_baixa': incidentes_baixa,
        
        # Listas Recentes
        'ultimos_projetos': projetos_recentes,
        'ultimos_incidentes': incidentes_recentes
    })

@app.route('/criar-admin', methods=['GET', 'POST'])
def criar_admin():
    if request.method == 'POST':
        # Verificar se já existe um perfil de administrador
        perfil_admin = Perfil.query.filter_by(nome='ADMIN').first()
        if not perfil_admin:
            perfil_admin = Perfil(
                nome='ADMIN',
                descricao='Usuário com acesso total ao sistema'
            )
            db.session.add(perfil_admin)
            db.session.commit()
        
        # Verificar se já existe um usuário admin
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario(
                id_perfil=perfil_admin.id_perfil,
                login='admin',
                nome_completo='Administrador do Sistema',
                email='admin@portalprojetos.com',
                senha=generate_password_hash('admin123'),
                status='ATIVO'
            )
            db.session.add(admin)
            db.session.commit()
            flash('Usuário administrador criado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Usuário administrador já existe!', 'warning')
            return redirect(url_for('login'))
    
    return render_template('criar_admin.html')

@app.route('/incidentes')
@login_required
def listar_incidentes():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    prioridade = request.args.get('prioridade', '')
    busca = request.args.get('busca', '')

    query = Incidente.query

    if status:
        query = query.filter_by(status=status)
    
    if prioridade:
        query = query.filter_by(prioridade=prioridade)
    
    if busca:
        query = query.filter(
            db.or_(
                Incidente.titulo.ilike(f'%{busca}%'),
                Incidente.descricao.ilike(f'%{busca}%'),
                Incidente.projeto.codigo_projeto.ilike(f'%{busca}%')
            )
        )

    pagination = db.paginate(
        query.order_by(Incidente.data_criacao.desc()),
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template('incidentes.html', incidentes=pagination.items, pagination=pagination)

@app.route('/incidentes/novo', methods=['GET', 'POST'])
@login_required
def criar_incidente():
    if request.method == 'POST':
        try:
            # Validação dos campos obrigatórios
            campos_obrigatorios = ['id_projeto', 'titulo', 'descricao', 'prioridade']
            for campo in campos_obrigatorios:
                if not request.form.get(campo):
                    flash(f'O campo {campo} é obrigatório.', 'danger')
                    return redirect(url_for('criar_incidente'))

            # Criação do incidente com os campos do formulário
            incidente = Incidente(
                id_projeto=request.form['id_projeto'],
                titulo=request.form['titulo'],
                descricao=request.form['descricao'],
                prioridade=request.form['prioridade'],
                status='ABERTO',  # Status inicial sempre como ABERTO
                id_usuario_criacao=current_user.id_usuario,
                id_usuario_ultima_atualizacao=current_user.id_usuario,
                data_criacao=datetime.now(timezone),
                data_ultima_atualizacao=datetime.now(timezone)
            )
            
            db.session.add(incidente)
            db.session.commit()
            
            flash('Incidente criado com sucesso!', 'success')
            return redirect(url_for('listar_incidentes'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar incidente: ' + str(e), 'danger')
            return redirect(url_for('criar_incidente'))
    
    projetos = Projeto.query.all()
    
    # Pré-selecionar projeto se fornecido via query parameter
    projeto_selecionado = request.args.get('projeto', '')
    
    return render_template('incidente_form.html', 
                         titulo='Novo Incidente', 
                         projetos=projetos,
                         projeto_selecionado=projeto_selecionado)

@app.route('/incidentes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_incidente(id):
    incidente = Incidente.query.get_or_404(id)
    
    if request.method == 'POST':
        incidente.titulo = request.form['titulo']
        incidente.descricao = request.form['descricao']
        incidente.prioridade = request.form['prioridade']
        incidente.status = request.form['status']
        incidente.id_usuario_ultima_atualizacao = current_user.id_usuario
        incidente.data_ultima_atualizacao = datetime.now(timezone)
        
        if incidente.status in ['RESOLVIDO', 'FECHADO']:
            incidente.data_resolucao = datetime.now(timezone)
        
        try:
            db.session.commit()
            flash('Incidente atualizado com sucesso!', 'success')
            return redirect(url_for('listar_incidentes'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar incidente.', 'danger')
    
    projetos = Projeto.query.all()
    return render_template('incidente_form.html', titulo='Editar Incidente', incidente=incidente, projetos=projetos)

@app.route('/incidentes/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_incidente(id):
    incidente = Incidente.query.get_or_404(id)
    
    try:
        db.session.delete(incidente)
        db.session.commit()
        flash('Incidente excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir incidente.', 'danger')
    
    return redirect(url_for('listar_incidentes'))

@app.route('/api/projetos')
@login_required
def api_projetos():
    projetos = Projeto.query.order_by(Projeto.codigo_projeto).all()
    return jsonify([{
        'id_projeto': p.id_projeto,
        'codigo_projeto': p.codigo_projeto,
        'nome_projeto': p.nome_projeto
    } for p in projetos])

# Rotas para manutenção de usuários
@app.route('/usuarios')
@login_required
def listar_usuarios():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Filtros
    status = request.args.get('status', '')
    perfil = request.args.get('perfil', '')
    search = request.args.get('search', '')
    
    # Query base
    query = Usuario.query
    
    # Aplicar filtros
    if status:
        query = query.filter(Usuario.status == status)
    if perfil:
        query = query.filter(Usuario.id_perfil == perfil)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Usuario.login.ilike(search_term),
                Usuario.nome_completo.ilike(search_term),
                Usuario.email.ilike(search_term)
            )
        )
    
    # Ordenar por nome completo
    query = query.order_by(Usuario.nome_completo)
    
    # Paginação
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    usuarios = pagination.items
    
    # Buscar perfis para o filtro
    perfis = Perfil.query.all()
    
    return render_template('usuarios.html', 
                         usuarios=usuarios, 
                         pagination=pagination,
                         perfis=perfis)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def criar_usuario():
    if request.method == 'POST':
        try:
            # Verificar se o login já existe
            if Usuario.query.filter_by(login=request.form['login']).first():
                flash('Login já existe. Escolha outro login.', 'danger')
                return redirect(url_for('criar_usuario'))
            
            # Verificar se o email já existe
            if Usuario.query.filter_by(email=request.form['email']).first():
                flash('Email já existe. Escolha outro email.', 'danger')
                return redirect(url_for('criar_usuario'))
            
            usuario = Usuario(
                id_perfil=request.form['id_perfil'],
                login=request.form['login'],
                nome_completo=request.form['nome_completo'],
                email=request.form['email'],
                senha=generate_password_hash(request.form['senha']),
                status=request.form['status']
            )
            
            db.session.add(usuario)
            db.session.commit()
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar usuário: ' + str(e), 'danger')
    
    perfis = Perfil.query.all()
    return render_template('usuario_form.html', titulo='Novo Usuário', perfis=perfis)

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        # Verificar se o login já existe (exceto para o próprio usuário)
        outro_usuario = Usuario.query.filter_by(login=request.form['login']).first()
        if outro_usuario and outro_usuario.id_usuario != usuario.id_usuario:
            flash('Login já existe. Escolha outro login.', 'danger')
            return redirect(url_for('editar_usuario', id=id))
        
        # Verificar se o email já existe (exceto para o próprio usuário)
        outro_usuario = Usuario.query.filter_by(email=request.form['email']).first()
        if outro_usuario and outro_usuario.id_usuario != usuario.id_usuario:
            flash('Email já existe. Escolha outro email.', 'danger')
            return redirect(url_for('editar_usuario', id=id))
        
        usuario.id_perfil = request.form['id_perfil']
        usuario.login = request.form['login']
        usuario.nome_completo = request.form['nome_completo']
        usuario.email = request.form['email']
        usuario.status = request.form['status']
        
        # Atualizar senha apenas se foi fornecida
        if request.form['senha']:
            usuario.senha = generate_password_hash(request.form['senha'])
        
        try:
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar usuário: ' + str(e), 'danger')
    
    perfis = Perfil.query.all()
    return render_template('usuario_form.html', titulo='Editar Usuário', usuario=usuario, perfis=perfis)

@app.route('/usuarios/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    
    # Não permitir excluir o próprio usuário
    if usuario.id_usuario == current_user.id_usuario:
        flash('Não é possível excluir o próprio usuário.', 'danger')
        return redirect(url_for('listar_usuarios'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir usuário.', 'danger')
    
    return redirect(url_for('listar_usuarios'))

# Rotas para manutenção de tarefas
@app.route('/tarefas')
@login_required
def listar_tarefas():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Filtros
    status = request.args.get('status', '')
    prioridade = request.args.get('prioridade', '')
    projeto = request.args.get('projeto', '')
    responsavel = request.args.get('responsavel', '')
    search = request.args.get('search', '')
    
    # Query base
    query = Tarefa.query
    
    # Aplicar filtros
    if status:
        query = query.filter(Tarefa.status == status)
    if prioridade:
        query = query.filter(Tarefa.prioridade == prioridade)
    if projeto:
        query = query.filter(Tarefa.id_projeto == projeto)
    if responsavel:
        query = query.filter(Tarefa.id_usuario_responsavel == responsavel)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Tarefa.titulo.ilike(search_term),
                Tarefa.descricao.ilike(search_term)
            )
        )
    
    # Ordenar por data de criação (mais recentes primeiro)
    query = query.order_by(Tarefa.data_criacao.desc())
    
    # Paginação
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tarefas = pagination.items
    
    # Buscar dados para os filtros
    projetos = Projeto.query.all()
    usuarios = Usuario.query.filter_by(status='ATIVO').all()
    
    return render_template('tarefas.html', 
                         tarefas=tarefas, 
                         pagination=pagination,
                         projetos=projetos,
                         usuarios=usuarios)

@app.route('/tarefas/novo', methods=['GET', 'POST'])
@login_required
def criar_tarefa():
    if request.method == 'POST':
        try:
            # Validação dos campos obrigatórios
            campos_obrigatorios = ['titulo', 'descricao', 'prioridade', 'id_projeto']
            for campo in campos_obrigatorios:
                if not request.form.get(campo):
                    flash(f'O campo {campo} é obrigatório.', 'danger')
                    return redirect(url_for('criar_tarefa'))
            
            tarefa = Tarefa(
                titulo=request.form['titulo'],
                descricao=request.form['descricao'],
                prioridade=request.form['prioridade'],
                status='PENDENTE',  # Status inicial sempre como PENDENTE
                id_projeto=request.form['id_projeto'],
                id_usuario_responsavel=request.form.get('id_usuario_responsavel'),
                id_usuario_criacao=current_user.id_usuario,
                id_usuario_ultima_atualizacao=current_user.id_usuario,
                data_criacao=datetime.now(timezone),
                data_ultima_atualizacao=datetime.now(timezone),
                data_limite=datetime.strptime(request.form['data_limite'], '%Y-%m-%d') if request.form.get('data_limite') else None
            )
            
            db.session.add(tarefa)
            db.session.commit()
            
            flash('Tarefa criada com sucesso!', 'success')
            return redirect(url_for('listar_tarefas'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar tarefa: ' + str(e), 'danger')
            return redirect(url_for('criar_tarefa'))
    
    projetos = Projeto.query.all()
    usuarios = Usuario.query.filter_by(status='ATIVO').all()
    
    # Pré-selecionar projeto se fornecido via query parameter
    projeto_selecionado = request.args.get('projeto', '')
    
    return render_template('tarefa_form.html', 
                         titulo='Nova Tarefa', 
                         projetos=projetos, 
                         usuarios=usuarios,
                         projeto_selecionado=projeto_selecionado)

@app.route('/tarefas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    
    if request.method == 'POST':
        tarefa.titulo = request.form['titulo']
        tarefa.descricao = request.form['descricao']
        tarefa.prioridade = request.form['prioridade']
        tarefa.status = request.form['status']
        tarefa.id_projeto = request.form['id_projeto']
        tarefa.id_usuario_responsavel = request.form.get('id_usuario_responsavel')
        tarefa.id_usuario_ultima_atualizacao = current_user.id_usuario
        tarefa.data_ultima_atualizacao = datetime.now(timezone)
        
        # Atualizar data limite se fornecida
        if request.form.get('data_limite'):
            tarefa.data_limite = datetime.strptime(request.form['data_limite'], '%Y-%m-%d')
        else:
            tarefa.data_limite = None
        
        # Atualizar data de conclusão se status for CONCLUIDA
        if tarefa.status == 'CONCLUIDA' and not tarefa.data_conclusao:
            tarefa.data_conclusao = datetime.now(timezone)
        elif tarefa.status != 'CONCLUIDA':
            tarefa.data_conclusao = None
        
        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('listar_tarefas'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar tarefa.', 'danger')
    
    projetos = Projeto.query.all()
    usuarios = Usuario.query.filter_by(status='ATIVO').all()
    return render_template('tarefa_form.html', titulo='Editar Tarefa', tarefa=tarefa, projetos=projetos, usuarios=usuarios)

@app.route('/tarefas/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    
    try:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir tarefa.', 'danger')
    
    return redirect(url_for('listar_tarefas'))

if __name__ == '__main__':
    with app.app_context():
        # Criar o banco de dados
        db.create_all()
        
        # Criar perfis padrão se não existirem
        if not Perfil.query.first():
            perfil_admin = Perfil(id_perfil=1, nome='ADMIN', descricao='Administrador do sistema')
            perfil_usuario = Perfil(id_perfil=2, nome='USUARIO', descricao='Usuário padrão')
            db.session.add(perfil_admin)
            db.session.add(perfil_usuario)
            db.session.commit()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario(
                id_perfil=1,
                login='admin',
                nome_completo='Administrador do Sistema',
                email='admin@sistema.com',
                senha=generate_password_hash('admin'),
                status='ATIVO'
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True) 