from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.services.nps_service import nps_service
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Criar blueprint para rotas NPS
nps_bp = Blueprint('nps', __name__)

@nps_bp.route('/nps', methods=['POST'])
@cross_origin()
def criar_pesquisa_nps():
    """Endpoint para criar uma nova pesquisa NPS"""
    try:
        # Verificar se o request tem dados JSON
        if not request.is_json:
            return jsonify({
                'success': False,
                'message': 'Content-Type deve ser application/json',
                'error': 'Invalid content type'
            }), 400
        
        dados = request.get_json()
        
        # Verificar se dados foram enviados
        if not dados:
            return jsonify({
                'success': False,
                'message': 'Nenhum dado foi enviado',
                'error': 'Empty request body'
            }), 400
        
        # Criar pesquisa usando o serviço
        resultado = nps_service.criar_pesquisa(dados)
        
        # Determinar status code baseado no resultado
        status_code = 201 if resultado.success else 400
        
        return jsonify(resultado.dict()), status_code
        
    except Exception as e:
        logger.error(f"Erro no endpoint criar_pesquisa_nps: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor',
            'error': str(e)
        }), 500

@nps_bp.route('/nps', methods=['GET'])
@cross_origin()
def listar_pesquisas_nps():
    """Endpoint para listar pesquisas NPS"""
    try:
        # Obter parâmetros de query
        filial = request.args.get('filial')
        limite = request.args.get('limite', 100, type=int)
        
        # Validar limite
        if limite > 1000:
            limite = 1000
        
        # Listar pesquisas usando o serviço
        resultado = nps_service.listar_pesquisas(filial=filial, limite=limite)
        
        status_code = 200 if resultado.success else 400
        
        return jsonify(resultado.dict()), status_code
        
    except Exception as e:
        logger.error(f"Erro no endpoint listar_pesquisas_nps: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor',
            'error': str(e)
        }), 500

@nps_bp.route('/nps/estatisticas', methods=['GET'])
@cross_origin()
def obter_estatisticas_nps():
    """Endpoint para obter estatísticas das pesquisas NPS"""
    try:
        # Obter parâmetros de query
        filial = request.args.get('filial')
        
        # Obter estatísticas usando o serviço
        resultado = nps_service.obter_estatisticas(filial=filial)
        
        status_code = 200 if resultado.success else 400
        
        return jsonify(resultado.dict()), status_code
        
    except Exception as e:
        logger.error(f"Erro no endpoint obter_estatisticas_nps: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro interno do servidor',
            'error': str(e)
        }), 500

@nps_bp.route('/nps/health', methods=['GET'])
@cross_origin()
def health_check():
    """Endpoint para verificar saúde da API"""
    try:
        # Testar conexão com Supabase
        from src.database.supabase_client import supabase_client
        sucesso, mensagem = supabase_client.test_connection()
        
        return jsonify({
            'success': True,
            'message': 'API NPS funcionando',
            'database_status': 'conectado' if sucesso else 'erro',
            'database_message': mensagem
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Erro no health check',
            'error': str(e)
        }), 500

