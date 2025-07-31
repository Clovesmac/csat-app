import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.routes.csat_persistent import csat_bp
from src.storage_manager import storage_manager

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

# Registrar blueprints
app.register_blueprint(csat_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    """Endpoint para verificar saúde da aplicação"""
    try:
        storage_info = storage_manager.get_storage_info()
        stats = storage_manager.get_stats()
        
        return {
            'status': 'healthy',
            'storage': storage_info,
            'stats': stats,
            'message': 'Aplicação funcionando com armazenamento persistente'
        }, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

@app.route('/api/system-info')
def system_info():
    """Informações do sistema e armazenamento"""
    try:
        storage_info = storage_manager.get_storage_info()
        stats = storage_manager.get_stats()
        
        return jsonify({
            'system': {
                'python_version': sys.version,
                'flask_version': '2.3.3',
                'storage_type': 'Persistent JSON File Storage'
            },
            'storage': storage_info,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=== CSAT Application with Persistent Storage ===")
    print(f"Storage location: {storage_manager.storage_dir}")
    
    # Verificar se há dados existentes
    stats = storage_manager.get_stats()
    print(f"Dados existentes: {stats['total']} registros")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

