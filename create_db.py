import sqlite3
import os
import stat

def create_database():
    # Remover o banco de dados se existir
    if os.path.exists('portal_projetos.db'):
        os.remove('portal_projetos.db')
    
    # Criar o banco de dados
    conn = sqlite3.connect('portal_projetos.db')
    conn.close()
    
    # Definir permissões de leitura e escrita
    os.chmod('portal_projetos.db', stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)
    
    print('Banco de dados criado com sucesso!')

if __name__ == '__main__':
    create_database() 