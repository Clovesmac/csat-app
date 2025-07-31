from flask import Blueprint, request, session, render_template_string, redirect, url_for, jsonify
from src.models.csat import db, CSATResponse
from functools import wraps
import os

admin_bp = Blueprint('admin', __name__)

# Senha para acesso administrativo
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

def require_admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_authenticated'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Senha incorreta')
    
    return render_template_string(LOGIN_TEMPLATE)

@admin_bp.route('/admin/logout')
def logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin')
@require_admin_auth
def dashboard():
    return render_template_string(ADMIN_TEMPLATE)

@admin_bp.route('/admin/api/data')
@require_admin_auth
def get_admin_data():
    try:
        # Buscar todas as avaliações
        responses = CSATResponse.query.order_by(CSATResponse.timestamp.desc()).all()
        
        # Calcular estatísticas
        total = len(responses)
        if total == 0:
            stats = {
                'total': 0,
                'average': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'context_distribution': {}
            }
        else:
            ratings = [r.rating for r in responses]
            average = sum(ratings) / total
            
            # Distribuição por rating
            distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for rating in ratings:
                distribution[rating] += 1
            
            # Distribuição por contexto
            context_distribution = {}
            for response in responses:
                context = response.context or 'Não especificado'
                context_distribution[context] = context_distribution.get(context, 0) + 1
            
            stats = {
                'total': total,
                'average': round(average, 2),
                'distribution': distribution,
                'context_distribution': context_distribution
            }
        
        # Converter avaliações para dict
        responses_data = [response.to_dict() for response in responses]
        
        return jsonify({
            'responses': responses_data,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Template de login
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        .login-header p {
            color: #666;
            font-size: 0.9rem;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 500;
        }
        input[type="password"] {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e1e5e9;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 0.75rem;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .error {
            color: #e74c3c;
            text-align: center;
            margin-top: 1rem;
            padding: 0.5rem;
            background: #fdf2f2;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Área Administrativa</h1>
            <p>Digite a senha para acessar o dashboard</p>
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label for="password">Senha:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">Entrar</button>
        </form>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

# Template do dashboard administrativo
ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Administrativo - CSAT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #334155;
        }
        .header {
            background: white;
            padding: 1rem 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            color: #1e293b;
        }
        .logout-btn {
            background: #ef4444;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .logout-btn:hover {
            background: #dc2626;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        .stat-card .value {
            font-size: 2rem;
            font-weight: bold;
            color: #1e293b;
        }
        .data-section {
            background: white;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .section-header {
            padding: 1.5rem;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .section-header h2 {
            color: #1e293b;
        }
        .export-btn {
            background: #10b981;
            color: white;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .export-btn:hover {
            background: #059669;
        }
        .table-container {
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        th {
            background: #f8fafc;
            font-weight: 600;
            color: #475569;
        }
        .rating {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        .rating-5 { background: #dcfce7; color: #166534; }
        .rating-4 { background: #fef3c7; color: #92400e; }
        .rating-3 { background: #fef3c7; color: #92400e; }
        .rating-2 { background: #fee2e2; color: #991b1b; }
        .rating-1 { background: #fee2e2; color: #991b1b; }
        .context {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background: #e0e7ff;
            color: #3730a3;
            border-radius: 15px;
            font-size: 0.75rem;
        }
        .loading {
            text-align: center;
            padding: 2rem;
            color: #64748b;
        }
        .error {
            text-align: center;
            padding: 2rem;
            color: #ef4444;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Dashboard CSAT</h1>
        <a href="/admin/logout" class="logout-btn">Sair</a>
    </div>

    <div class="container">
        <div class="stats-grid" id="statsGrid">
            <div class="loading">Carregando estatísticas...</div>
        </div>

        <div class="data-section">
            <div class="section-header">
                <h2>Avaliações Recentes</h2>
                <a href="/api/csat/export" class="export-btn">📥 Exportar CSV</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Avaliação</th>
                            <th>Contexto</th>
                            <th>Comentário</th>
                            <th>Data/Hora</th>
                        </tr>
                    </thead>
                    <tbody id="responsesTable">
                        <tr>
                            <td colspan="5" class="loading">Carregando dados...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        async function loadData() {
            try {
                const response = await fetch('/admin/api/data');
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Atualizar estatísticas
                updateStats(data.stats);
                
                // Atualizar tabela
                updateTable(data.responses);
                
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                document.getElementById('statsGrid').innerHTML = '<div class="error">Erro ao carregar dados: ' + error.message + '</div>';
                document.getElementById('responsesTable').innerHTML = '<tr><td colspan="5" class="error">Erro ao carregar dados</td></tr>';
            }
        }
        
        function updateStats(stats) {
            const statsHtml = `
                <div class="stat-card">
                    <h3>Total de Avaliações</h3>
                    <div class="value">${stats.total}</div>
                </div>
                <div class="stat-card">
                    <h3>Média de Satisfação</h3>
                    <div class="value">${stats.average}/5</div>
                </div>
                <div class="stat-card">
                    <h3>Muito Satisfeitos (5⭐)</h3>
                    <div class="value">${stats.distribution[5] || 0}</div>
                </div>
                <div class="stat-card">
                    <h3>Insatisfeitos (1-2⭐)</h3>
                    <div class="value">${(stats.distribution[1] || 0) + (stats.distribution[2] || 0)}</div>
                </div>
            `;
            document.getElementById('statsGrid').innerHTML = statsHtml;
        }
        
        function updateTable(responses) {
            if (responses.length === 0) {
                document.getElementById('responsesTable').innerHTML = '<tr><td colspan="5" style="text-align: center; color: #64748b;">Nenhuma avaliação encontrada</td></tr>';
                return;
            }
            
            const tableHtml = responses.map(response => {
                const date = new Date(response.timestamp).toLocaleString('pt-BR');
                const ratingText = {
                    1: '1⭐ Muito Insatisfeito',
                    2: '2⭐ Insatisfeito',
                    3: '3⭐ Neutro',
                    4: '4⭐ Satisfeito',
                    5: '5⭐ Muito Satisfeito'
                }[response.rating];
                
                return `
                    <tr>
                        <td>${response.id}</td>
                        <td><span class="rating rating-${response.rating}">${ratingText}</span></td>
                        <td><span class="context">${response.context || 'N/A'}</span></td>
                        <td>${response.comment ? (response.comment.length > 50 ? response.comment.substring(0, 50) + '...' : response.comment) : '-'}</td>
                        <td>${date}</td>
                    </tr>
                `;
            }).join('');
            
            document.getElementById('responsesTable').innerHTML = tableHtml;
        }
        
        // Carregar dados ao inicializar
        loadData();
        
        // Atualizar dados a cada 30 segundos
        setInterval(loadData, 30000);
    </script>
</body>
</html>
'''

