-- Tabela de Perfis de Usuário
CREATE TABLE Perfis (
    id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_perfil TEXT UNIQUE NOT NULL,
    descricao TEXT
);

-- Tabela de Usuários
CREATE TABLE Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_perfil INTEGER NOT NULL,
    login TEXT UNIQUE NOT NULL,
    nome_completo TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_login DATETIME,
    status TEXT DEFAULT 'ATIVO',
    FOREIGN KEY (id_perfil) REFERENCES Perfis(id_perfil)
);

-- Tabela de Permissões
CREATE TABLE Permissoes (
    id_permissao INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_permissao TEXT UNIQUE NOT NULL,
    descricao TEXT
);

-- Tabela de Relacionamento entre Perfis e Permissões
CREATE TABLE PerfilPermissoes (
    id_perfil_permissao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_perfil INTEGER NOT NULL,
    id_permissao INTEGER NOT NULL,
    FOREIGN KEY (id_perfil) REFERENCES Perfis(id_perfil),
    FOREIGN KEY (id_permissao) REFERENCES Permissoes(id_permissao),
    UNIQUE (id_perfil, id_permissao)
);

-- Tabela de Projetos
CREATE TABLE Projetos (
    id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario_criacao INTEGER,
    id_usuario_ultima_atualizacao INTEGER,
    codigo_projeto TEXT UNIQUE NOT NULL,
    nome_projeto TEXT NOT NULL,
    controle_economico TEXT UNIQUE NOT NULL,
    numero_iniciativa TEXT UNIQUE NOT NULL,
    situacao_projeto TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_ultima_atualizacao) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Changes para Projetos
CREATE TABLE ProjetoChanges (
    id_projeto_change INTEGER PRIMARY KEY AUTOINCREMENT,
    id_projeto INTEGER,
    id_usuario_criacao INTEGER,
    id_usuario_fechamento INTEGER,
    numero_change TEXT UNIQUE NOT NULL,
    descricao TEXT,
    status TEXT,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME,
    FOREIGN KEY (id_projeto) REFERENCES Projetos(id_projeto),
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_fechamento) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Chamados para Projetos
CREATE TABLE ProjetoChamados (
    id_projeto_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_projeto INTEGER,
    id_usuario_criacao INTEGER,
    id_usuario_fechamento INTEGER,
    numero_chamado TEXT UNIQUE NOT NULL,
    descricao TEXT,
    status TEXT,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME,
    FOREIGN KEY (id_projeto) REFERENCES Projetos(id_projeto),
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_fechamento) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Incidentes
CREATE TABLE Incidentes (
    id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_projeto INTEGER,
    id_usuario_criacao INTEGER,
    id_usuario_ultima_atualizacao INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    prioridade TEXT NOT NULL,
    status TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_ultima_atualizacao DATETIME,
    data_resolucao DATETIME,
    FOREIGN KEY (id_projeto) REFERENCES Projetos(id_projeto),
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_ultima_atualizacao) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Esteiras do GitHub Afetadas
CREATE TABLE IncidenteEsteiras (
    id_incidente_esteira INTEGER PRIMARY KEY AUTOINCREMENT,
    id_incidente INTEGER,
    id_usuario_registro INTEGER,
    nome_esteira TEXT NOT NULL,
    status_tratamento TEXT,
    FOREIGN KEY (id_incidente) REFERENCES Incidentes(id_incidente),
    FOREIGN KEY (id_usuario_registro) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Changes para Incidentes
CREATE TABLE IncidenteChanges (
    id_incidente_change INTEGER PRIMARY KEY AUTOINCREMENT,
    id_incidente INTEGER,
    id_usuario_criacao INTEGER,
    id_usuario_fechamento INTEGER,
    numero_change TEXT UNIQUE NOT NULL,
    descricao TEXT,
    status TEXT,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME,
    FOREIGN KEY (id_incidente) REFERENCES Incidentes(id_incidente),
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_fechamento) REFERENCES Usuarios(id_usuario)
);

-- Tabela de Chamados para Incidentes
CREATE TABLE IncidenteChamados (
    id_incidente_chamado INTEGER PRIMARY KEY AUTOINCREMENT,
    id_incidente INTEGER,
    id_usuario_criacao INTEGER,
    id_usuario_fechamento INTEGER,
    numero_chamado TEXT UNIQUE NOT NULL,
    descricao TEXT,
    status TEXT,
    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_fechamento DATETIME,
    FOREIGN KEY (id_incidente) REFERENCES Incidentes(id_incidente),
    FOREIGN KEY (id_usuario_criacao) REFERENCES Usuarios(id_usuario),
    FOREIGN KEY (id_usuario_fechamento) REFERENCES Usuarios(id_usuario)
);

-- Inserção de Perfis Padrão
INSERT INTO Perfis (nome_perfil, descricao) VALUES 
('ADMIN', 'Administrador com acesso total ao sistema'),
('GESTOR_PROJETO', 'Usuário com permissões de gestão de projetos'),
('ANALISTA_TI', 'Analista de TI com permissões de registro de incidentes'),
('CONSULTA', 'Usuário apenas com permissão de consulta');

-- Inserção de Permissões Padrão
INSERT INTO Permissoes (nome_permissao, descricao) VALUES 
('CRIAR_PROJETO', 'Permissão para criar novos projetos'),
('EDITAR_PROJETO', 'Permissão para editar projetos existentes'),
('EXCLUIR_PROJETO', 'Permissão para excluir projetos'),
('CRIAR_INCIDENTE', 'Permissão para criar novos incidentes'),
('EDITAR_INCIDENTE', 'Permissão para editar incidentes'),
('EXCLUIR_INCIDENTE', 'Permissão para excluir incidentes'),
('GERENCIAR_USUARIOS', 'Permissão para gerenciar usuários do sistema'),
('CONSULTAR_PROJETO', 'Permissão para consultar projetos'),
('CONSULTAR_INCIDENTE', 'Permissão para consultar incidentes');

-- Associação de Permissões para Perfil ADMIN
INSERT INTO PerfilPermissoes (id_perfil, id_permissao)
SELECT p.id_perfil, pm.id_permissao
FROM Perfis p, Permissoes pm
WHERE p.nome_perfil = 'ADMIN';

-- Inserção do usuário ADMIN com senha criptografada
INSERT INTO Usuarios (
    id_perfil, 
    login, 
    nome_completo, 
    email, 
    senha, 
    status
) VALUES (
    (SELECT id_perfil FROM Perfis WHERE nome_perfil = 'ADMIN'),
    'admin',
    'Administrador do Sistema',
    'admin@empresa.com',
    'scrypt:32768:8:1$DRBJyuqN2CPNf8ID$f94aa7ddec69a29542721b447ea6d2ab87200d756d81a0eecf859fd508814945f65ab34f7772604ad2a5cb47d09c126cc9cc2c24312b11090df5b70a4a4269f0',
    'ATIVO'
);

-- Índices para melhorar performance
CREATE INDEX idx_projeto_codigo ON Projetos(codigo_projeto);
CREATE INDEX idx_projeto_nome ON Projetos(nome_projeto);
CREATE INDEX idx_change_projeto ON ProjetoChanges(id_projeto);
CREATE INDEX idx_chamado_projeto ON ProjetoChamados(id_projeto);
CREATE INDEX idx_incidente_projeto ON Incidentes(id_projeto);
CREATE INDEX idx_esteira_incidente ON IncidenteEsteiras(id_incidente);
CREATE INDEX idx_change_incidente ON IncidenteChanges(id_incidente);
CREATE INDEX idx_chamado_incidente ON IncidenteChamados(id_incidente);

-- Índices para controle de acesso
CREATE INDEX idx_usuario_login ON Usuarios(login);
CREATE INDEX idx_usuario_perfil ON Usuarios(id_perfil);
CREATE INDEX idx_projeto_usuario_criacao ON Projetos(id_usuario_criacao);
CREATE INDEX idx_projeto_usuario_atualizacao ON Projetos(id_usuario_ultima_atualizacao);
CREATE INDEX idx_incidente_usuario_criacao ON Incidentes(id_usuario_criacao);
CREATE INDEX idx_incidente_usuario_atualizacao ON Incidentes(id_usuario_ultima_atualizacao); 