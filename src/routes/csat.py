from flask import Blueprint, request, jsonify, make_response
from src.models.csat import db, CSATResponse
from datetime import datetime
import csv
import io

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
        
        # Criar nova resposta CSAT
        new_response = CSATResponse(
            rating=rating,
            context=data.get('context', ''),
            comment=data.get('comment', '')
        )
        
        # Salvar no banco de dados
        db.session.add(new_response)
        db.session.commit()
        
        return jsonify({
            'message': 'Avaliação salva com sucesso',
            'id': new_response.id,
            'data': new_response.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar avaliação: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat', methods=['GET'])
def get_csat_responses():
    """Obter todas as respostas CSAT"""
    try:
        responses = CSATResponse.query.order_by(CSATResponse.timestamp.desc()).all()
        return jsonify([response.to_dict() for response in responses])
    except Exception as e:
        print(f"Erro ao buscar avaliações: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat/stats', methods=['GET'])
def get_csat_stats():
    """Obter estatísticas das respostas CSAT"""
    try:
        responses = CSATResponse.query.all()
        
        if not responses:
            return jsonify({
                'total': 0,
                'average': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                'context_distribution': {}
            })
        
        total = len(responses)
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
        
        return jsonify({
            'total': total,
            'average': round(average, 2),
            'distribution': distribution,
            'context_distribution': context_distribution
        })
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@csat_bp.route('/csat/export', methods=['GET'])
def export_csat_to_csv():
    """Exportar todas as avaliações CSAT para CSV"""
    try:
        responses = CSATResponse.query.order_by(CSATResponse.timestamp.desc()).all()
        
        # Criar buffer de string para o CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escrever cabeçalho
        writer.writerow(['ID', 'Contexto', 'Avaliação', 'Comentário', 'Data/Hora'])
        
        # Escrever dados
        for response in responses:
            formatted_date = response.timestamp.strftime('%d/%m/%Y %H:%M:%S') if response.timestamp else ''
            
            rating_text = {
                1: '1 - Muito Insatisfeito',
                2: '2 - Insatisfeito', 
                3: '3 - Neutro',
                4: '4 - Satisfeito',
                5: '5 - Muito Satisfeito'
            }.get(response.rating, str(response.rating))
            
            writer.writerow([
                response.id,
                response.context or 'Não especificado',
                rating_text,
                response.comment or '',
                formatted_date
            ])
        
        output.seek(0)
        csv_data = output.getvalue()
        output.close()
        
        response = make_response(csv_data)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=csat_avaliacoes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
        return jsonify({'error': f'Erro ao exportar dados: {str(e)}'}), 500

@csat_bp.route('/csat/test-persistence', methods=['POST'])
def test_persistence():
    """Testar persistência adicionando dados de teste"""
    try:
        # Adicionar alguns dados de teste
        test_data = [
            {'rating': 5, 'context': 'Compra', 'comment': 'Teste PostgreSQL - Excelente!'},
            {'rating': 4, 'context': 'Suporte/Assistência', 'comment': 'Teste PostgreSQL - Muito bom!'},
            {'rating': 3, 'context': 'Devolução', 'comment': 'Teste PostgreSQL - Regular'}
        ]
        
        added_responses = []
        for data in test_data:
            new_response = CSATResponse(
                rating=data['rating'],
                context=data['context'],
                comment=data['comment']
            )
            db.session.add(new_response)
            db.session.flush()  # Para obter o ID
            added_responses.append(new_response.to_dict())
        
        db.session.commit()
        
        # Obter estatísticas atuais
        total_responses = CSATResponse.query.count()
        
        return jsonify({
            'message': 'Dados de teste adicionados com sucesso no PostgreSQL',
            'added_responses': added_responses,
            'total_responses': total_responses,
            'database': 'PostgreSQL'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro no teste de persistência: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

