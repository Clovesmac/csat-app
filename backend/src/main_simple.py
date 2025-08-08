import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.routes.nps_simple import nps_simple_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurar CORS para permitir requisições do frontend
CORS(app, origins="*")

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Registrar blueprints
app.register_blueprint(nps_simple_bp, url_prefix='/api')

@app.route('/api/health')
def health():
    """Endpoint de saúde geral da API"""
    return jsonify({
        'status': 'ok',
        'message': 'API de Pesquisas Digital Sat funcionando',
        'version': '1.0.0'
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir arquivos estáticos do frontend"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({
            'error': 'Static folder not configured',
            'message': 'Frontend não configurado'
        }), 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'API de Pesquisas Digital Sat',
                'endpoints': {
                    'health': '/api/health',
                    'nps_health': '/api/nps/health',
                    'criar_nps': 'POST /api/nps',
                    'listar_nps': 'GET /api/nps',
                    'estatisticas_nps': 'GET /api/nps/estatisticas'
                }
            })

if __name__ == '__main__':
    try:
        # Verificar configurações na inicialização
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if supabase_url and supabase_key:
            print("✅ Configurações do Supabase carregadas")
        else:
            print("⚠️  Configurações do Supabase não encontradas - API funcionará em modo de teste")
        
        print("🚀 Iniciando API de Pesquisas Digital Sat...")
        app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")

