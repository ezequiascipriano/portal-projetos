# Portal de Projetos

Sistema de gerenciamento de projetos, tarefas e incidentes desenvolvido em Flask.

## 🚀 Funcionalidades

### 📊 Dashboard
- Visão geral com estatísticas em tempo real
- Gráficos de projetos e incidentes
- Lista dos últimos projetos e incidentes
- Atualização automática a cada 30 segundos

### 📋 Projetos
- Cadastro e edição de projetos
- Controle de situação (Ativo, Concluído, Cancelado)
- Visualização detalhada com tarefas e incidentes associados
- Filtros por situação e busca por código/nome

### ✅ Tarefas
- Criação e gerenciamento de tarefas por projeto
- Controle de prioridade (Alta, Média, Baixa)
- Status de progresso (Pendente, Em Andamento, Concluída, Cancelada)
- Atribuição de responsáveis
- Controle de data limite

### 🚨 Incidentes
- Registro e acompanhamento de incidentes
- Controle de prioridade e status
- Associação a projetos específicos
- Histórico de resolução

### 👥 Usuários
- Sistema de perfis (Admin, Usuário)
- Controle de acesso e permissões
- Gerenciamento de usuários ativos/inativos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite com SQLAlchemy
- **Frontend**: Bootstrap 5, Chart.js
- **Autenticação**: Flask-Login
- **Timezone**: pytz (America/Sao_Paulo)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/portal-projetos.git
   cd portal-projetos
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute o projeto**
   ```bash
   python app.py
   ```

6. **Acesse o sistema**
   - URL: http://127.0.0.1:5000
   - Login padrão: `admin`
   - Senha padrão: `admin`

## 📁 Estrutura do Projeto

```
portal-projetos/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências do projeto
├── schema.sql            # Schema do banco de dados
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Dashboard
│   ├── projetos.html     # Lista de projetos
│   ├── projeto_form.html # Formulário de projeto
│   ├── tarefas.html      # Lista de tarefas
│   ├── tarefa_form.html  # Formulário de tarefa
│   ├── incidentes.html   # Lista de incidentes
│   ├── incidente_form.html # Formulário de incidente
│   ├── usuarios.html     # Lista de usuários
│   ├── usuario_form.html # Formulário de usuário
│   └── login.html        # Página de login
├── instance/             # Arquivos de instância (banco de dados)
└── venv/                 # Ambiente virtual (não versionado)
```

## 🔐 Configuração Inicial

O sistema cria automaticamente:
- Perfis padrão (ADMIN, USUARIO)
- Usuário administrador (login: `admin`, senha: `admin`)
- Banco de dados SQLite

## 📊 Funcionalidades Principais

### Dashboard
- **Estatísticas em tempo real**: Total de projetos, incidentes, tarefas
- **Gráficos interativos**: Distribuição por status e prioridade
- **Listas recentes**: Últimos projetos e incidentes criados

### Gerenciamento de Projetos
- **CRUD completo**: Criar, visualizar, editar, excluir projetos
- **Filtros avançados**: Por situação, busca por código/nome
- **Visualização detalhada**: Tarefas e incidentes associados ao projeto

### Sistema de Tarefas
- **Controle de progresso**: Status e prioridade
- **Atribuição**: Responsáveis por tarefa
- **Datas**: Limite e conclusão
- **Filtros**: Por projeto, responsável, status, prioridade

### Gestão de Incidentes
- **Registro completo**: Título, descrição, prioridade
- **Acompanhamento**: Status de resolução
- **Histórico**: Data de criação e resolução
- **Associação**: Vinculação a projetos específicos

### Administração de Usuários
- **Perfis**: Controle de acesso por perfil
- **Status**: Usuários ativos/inativos
- **Segurança**: Senhas criptografadas

## 🔧 Scripts Úteis

### Recriar Banco de Dados
```bash
python recreate_db.py
```

### Criar Usuários de Teste
```bash
python criar_usuarios_teste.py
```

### Criar Projetos de Teste
```bash
python criar_projetos_teste.py
```

### Criar Tarefas de Teste
```bash
python criar_tarefas_teste.py
```

## 🚀 Deploy

### Desenvolvimento
```bash
python app.py
```

### Produção
Para deploy em produção, recomenda-se:
- Usar um servidor WSGI (Gunicorn, uWSGI)
- Configurar um banco de dados mais robusto (PostgreSQL, MySQL)
- Usar variáveis de ambiente para configurações sensíveis
- Configurar HTTPS

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma issue no repositório.

---

**Portal de Projetos** - Sistema completo de gerenciamento de projetos, tarefas e incidentes. 