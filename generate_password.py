from werkzeug.security import generate_password_hash

senha = 'admin@123'
senha_hash = generate_password_hash(senha)
print(f"Senha criptografada: {senha_hash}") 