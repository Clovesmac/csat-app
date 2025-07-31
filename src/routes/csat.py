from flask import Blueprint, request, jsonify, make_response
from src.storage_manager import storage_manager
from datetime import datetime

csat_bp = Blueprint('csat', __name__)

@csat_bp.route('/csat', methods=['POST'])
def create_csat_response():
    """Criar uma nova resposta CSAT"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data or 'rating' not in data:
            return jsonify({'error': 'Rating é obrigatório'}), 400
        
        rating = data.get('rating')
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating deve ser um número entre 1 e 5'}), 400
        
        # Salvar usando o gerenciador de armazenamento persistente
        response_id = storage_manager.add_response(
            rating=rating,
            context=data.get('context', ''),
            comment=data.get('comment', '')
        )
        
        return jsonify({
            'message': 'Avaliação salva com sucesso',
            'id': response_id,
            'storage_info': storage_manager.get_storage_info()
        }), 201
        
    except Exception as e:
        print(f"Erro ao salvar avaliação: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat', methods=['GET'])
def get_csat_responses():
    """Obter todas as respostas CSAT"""
    try:
        responses = storage_manager.get_all_responses()
        return jsonify(responses)
    except Exception as e:
        print(f"Erro ao buscar avaliações: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat/stats', methods=['GET'])
def get_csat_stats():
    """Obter estatísticas das respostas CSAT"""
    try:
        stats = storage_manager.get_stats()
        return jsonify(stats)
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat/export', methods=['GET'])
def export_csat_to_csv():
    """Exportar todas as avaliações CSAT para CSV"""
    try:
        csv_data = storage_manager.export_to_csv()
        
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=csat_avaliacoes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        return jsonify({'error': f'Erro ao exportar dados: {str(e)}'}), 500

@csat_bp.route('/csat/storage-info', methods=['GET'])
def get_storage_info():
    """Obter informações sobre o armazenamento"""
    try:
        info = storage_manager.get_storage_info()
        return jsonify(info)
    except Exception as e:
        print(f"Erro ao obter informações de armazenamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat/test-persistence', methods=['POST'])
def test_persistence():
    """Testar persistência adicionando dados de teste"""
    try:
        # Adicionar alguns dados de teste
        test_data = [
            {'rating': 5, 'context': 'Compra', 'comment': 'Teste de persistência - Excelente!'},
            {'rating': 4, 'context': 'Suporte/Assistência', 'comment': 'Teste de persistência - Muito bom!'},
            {'rating': 3, 'context': 'Devolução', 'comment': 'Teste de persistência - Regular'}
        ]
        
        added_ids = []
        for data in test_data:
            response_id = storage_manager.add_response(**data)
            added_ids.append(response_id)
        
        storage_info = storage_manager.get_storage_info()
        stats = storage_manager.get_stats()
        
        return jsonify({
            'message': 'Dados de teste adicionados com sucesso',
            'added_ids': added_ids,
            'storage_info': storage_info,
            'current_stats': stats
        }), 201
        
    except Exception as e:
        print(f"Erro no teste de persistência: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

