from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta aleatória para sessões

# Configuração da base de dados
DATABASE = 'utilizadores.db'

def get_db():
    """Estabelece conexão com a base de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa a base de dados com as tabelas necessárias"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabela de utilizadores (Nível 1 - com campos extra)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nome_completo VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            tentativas_login INTEGER DEFAULT 0,
            bloqueado_ate TIMESTAMP,
            token_recuperacao VARCHAR(100),
            token_expiracao TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Inicializar a base de dados quando a aplicação iniciar
init_db()

# --- Rotas Principais ---

@app.route('/')
def index():
    """Rota principal - redireciona para login"""
    return redirect(url_for('login'))

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    """Página de registo de novo utilizador"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmar_password = request.form.get('confirmar_password', '')
        nome_completo = request.form.get('nome_completo', '')
        email = request.form.get('email', '')
        
        # Validações
        erros = []
        
        if not username or not password:
            erros.append("Username e password são obrigatórios")
        
        # Nível 2 - Confirmação de password
        if password != confirmar_password:
            erros.append("As passwords não coincidem")
        
        if len(password) < 6:
            erros.append("A password deve ter pelo menos 6 caracteres")
        
        if erros:
            return render_template('registo.html', erros=erros)
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # Verificar se utilizador já existe
            cursor.execute('SELECT id FROM utilizadores WHERE username = ?', (username,))
            if cursor.fetchone():
                erros.append("Username já existe")
                return render_template('registo.html', erros=erros)
            
            # Verificar se email já existe (Nível 1)
            if email:
                cursor.execute('SELECT id FROM utilizadores WHERE email = ?', (email,))
                if cursor.fetchone():
                    erros.append("Email já registado")
                    return render_template('registo.html', erros=erros)
            
            # Criar hash da password
            senha_hash = generate_password_hash(password)
            
            # Inserir novo utilizador
            cursor.execute('''
                INSERT INTO utilizadores (username, password, nome_completo, email)
                VALUES (?, ?, ?, ?)
            ''', (username, senha_hash, nome_completo, email))
            
            conn.commit()
            conn.close()
            
            flash('Registo efetuado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
            
        except sqlite3.Error as e:
            erros.append(f"Erro na base de dados: {str(e)}")
            return render_template('registo.html', erros=erros)
    
    return render_template('registo.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar utilizador
        cursor.execute('''
            SELECT * FROM utilizadores 
            WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        
        if user:
            # Nível 3 - Verificar se conta está bloqueada
            if user['bloqueado_ate']:
                bloqueado_ate = datetime.strptime(user['bloqueado_ate'], '%Y-%m-%d %H:%M:%S')
                if bloqueado_ate > datetime.now():
                    tempo_restante = (bloqueado_ate - datetime.now()).seconds // 60
                    flash(f'Conta bloqueada. Tente novamente em {tempo_restante} minutos.', 'danger')
                    return render_template('login.html')
                else:
                    # Desbloquear conta
                    cursor.execute('''
                        UPDATE utilizadores 
                        SET tentativas_login = 0, bloqueado_ate = NULL 
                        WHERE id = ?
                    ''', (user['id'],))
                    conn.commit()
            
            # Verificar password
            if check_password_hash(user['password'], password):
                # Login bem sucedido - resetar tentativas
                cursor.execute('''
                    UPDATE utilizadores 
                    SET tentativas_login = 0, bloqueado_ate = NULL 
                    WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                
                # Criar sessão
                session["utilizador"] = username
                session["user_id"] = user['id']
                session["nome_completo"] = user['nome_completo']
                
                flash(f'Bem-vindo, {username}!', 'success')
                conn.close()
                return redirect(url_for('dashboard'))
            else:
                # Password incorreta
                tentativas = user['tentativas_login'] + 1
                
                # Nível 3 - Bloqueio após 3 tentativas
                if tentativas >= 3:
                    bloqueio = datetime.now() + timedelta(minutes=15)
                    cursor.execute('''
                        UPDATE utilizadores 
                        SET tentativas_login = ?, bloqueado_ate = ? 
                        WHERE id = ?
                    ''', (tentativas, bloqueio.strftime('%Y-%m-%d %H:%M:%S'), user['id']))
                    conn.commit()
                    conn.close()
                    
                    flash('Conta bloqueada por 15 minutos devido a múltiplas tentativas falhadas.', 'danger')
                else:
                    cursor.execute('''
                        UPDATE utilizadores 
                        SET tentativas_login = ? 
                        WHERE id = ?
                    ''', (tentativas, user['id']))
                    conn.commit()
                    conn.close()
                    
                    tentativas_restantes = 3 - tentativas
                    flash(f'Password incorreta. Tentativas restantes: {tentativas_restantes}', 'warning')
                
                return render_template('login.html')
        else:
            conn.close()
            flash('Utilizador não encontrado.', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Página protegida - Dashboard"""
    if "utilizador" not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         username=session.get('utilizador'),
                         nome_completo=session.get('nome_completo'))

@app.route('/logout')
def logout():
    """Terminar sessão"""
    session.pop("utilizador", None)
    session.pop("user_id", None)
    session.pop("nome_completo", None)
    
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('login'))

# --- Nível 4 - Recuperação de Password ---

@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    """Recuperação de password"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Por favor, insira o email.', 'warning')
            return render_template('recuperar_password.html')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Buscar utilizador pelo email
        cursor.execute('SELECT * FROM utilizadores WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            # Gerar token de recuperação
            token = secrets.token_urlsafe(32)
            expiracao = datetime.now() + timedelta(hours=1)
            
            cursor.execute('''
                UPDATE utilizadores 
                SET token_recuperacao = ?, token_expiracao = ? 
                WHERE id = ?
            ''', (token, expiracao.strftime('%Y-%m-%d %H:%M:%S'), user['id']))
            
            conn.commit()
            conn.close()
            
            # Em produção, enviaria um email com o link
            # Para demonstração, mostramos o token na tela
            flash(f'Token de recuperação gerado (demonstração): {token}', 'info')
            flash('Em produção, um email seria enviado com o link de recuperação.', 'info')
            
            return redirect(url_for('redefinir_password', token=token))
        else:
            conn.close()
            flash('Email não encontrado.', 'danger')
    
    return render_template('recuperar_password.html')

@app.route('/redefinir-password/<token>', methods=['GET', 'POST'])
def redefinir_password(token):
    """Redefinir password com token"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar token válido
    cursor.execute('''
        SELECT * FROM utilizadores 
        WHERE token_recuperacao = ? 
        AND token_expiracao > ?
    ''', (token, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nova_password = request.form['password']
        confirmar_password = request.form.get('confirmar_password', '')
        
        # Validações
        if nova_password != confirmar_password:
            flash('As passwords não coincidem.', 'warning')
            return render_template('redefinir_password.html', token=token)
        
        if len(nova_password) < 6:
            flash('A password deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('redefinir_password.html', token=token)
        
        # Atualizar password
        novo_hash = generate_password_hash(nova_password)
        cursor.execute('''
            UPDATE utilizadores 
            SET password = ?, token_recuperacao = NULL, 
                token_expiracao = NULL, tentativas_login = 0,
                bloqueado_ate = NULL
            WHERE id = ?
        ''', (novo_hash, user['id']))
        
        conn.commit()
        conn.close()
        
        flash('Password redefinida com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    conn.close()
    return render_template('redefinir_password.html', token=token)

if __name__ == '__main__':
    app.run(debug=True)