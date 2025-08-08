from typing import Dict, Any, List
from src.database.supabase_client import supabase_client
from src.models.nps_pesquisa import NPSPesquisaModel, NPSPesquisaResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPSService:
    """Serviço para operações relacionadas a pesquisas NPS"""
    
    def __init__(self):
        self.client = supabase_client.client
        self.table_name = 'nps_pesquisas'
    
    def criar_pesquisa(self, dados: Dict[str, Any]) -> NPSPesquisaResponse:
        """Cria uma nova pesquisa NPS"""
        try:
            # Validar dados usando Pydantic
            pesquisa = NPSPesquisaModel(**dados)
            
            # Converter para dicionário
            dados_inserir = pesquisa.to_dict()
            
            # Inserir no Supabase
            result = self.client.table(self.table_name).insert(dados_inserir).execute()
            
            if result.data:
                logger.info(f"Pesquisa NPS criada com sucesso: {result.data[0]['id']}")
                return NPSPesquisaResponse(
                    success=True,
                    message="Pesquisa NPS salva com sucesso",
                    data=result.data[0]
                )
            else:
                logger.error("Erro ao inserir pesquisa NPS: dados não retornados")
                return NPSPesquisaResponse(
                    success=False,
                    message="Erro ao salvar pesquisa",
                    error="Dados não foram inseridos"
                )
                
        except ValueError as e:
            logger.error(f"Erro de validação: {str(e)}")
            return NPSPesquisaResponse(
                success=False,
                message="Dados inválidos",
                error=str(e)
            )
        except Exception as e:
            logger.error(f"Erro ao criar pesquisa NPS: {str(e)}")
            return NPSPesquisaResponse(
                success=False,
                message="Erro interno do servidor",
                error=str(e)
            )
    
    def listar_pesquisas(self, filial: str = None, limite: int = 100) -> NPSPesquisaResponse:
        """Lista pesquisas NPS com filtros opcionais"""
        try:
            query = self.client.table(self.table_name).select('*')
            
            if filial:
                query = query.eq('filial', filial)
            
            result = query.order('timestamp', desc=True).limit(limite).execute()
            
            return NPSPesquisaResponse(
                success=True,
                message=f"Encontradas {len(result.data)} pesquisas",
                data=result.data
            )
            
        except Exception as e:
            logger.error(f"Erro ao listar pesquisas: {str(e)}")
            return NPSPesquisaResponse(
                success=False,
                message="Erro ao buscar pesquisas",
                error=str(e)
            )
    
    def obter_estatisticas(self, filial: str = None) -> NPSPesquisaResponse:
        """Obtém estatísticas das pesquisas NPS"""
        try:
            query = self.client.table(self.table_name).select('score, categoria_nps')
            
            if filial:
                query = query.eq('filial', filial)
            
            result = query.execute()
            
            if not result.data:
                return NPSPesquisaResponse(
                    success=True,
                    message="Nenhuma pesquisa encontrada",
                    data={
                        'total': 0,
                        'promotores': 0,
                        'neutros': 0,
                        'detratores': 0,
                        'nps_score': 0
                    }
                )
            
            # Calcular estatísticas
            total = len(result.data)
            promotores = len([p for p in result.data if p['categoria_nps'] == 'promotor'])
            detratores = len([p for p in result.data if p['categoria_nps'] == 'detrator'])
            neutros = total - promotores - detratores
            
            # Calcular NPS Score
            nps_score = ((promotores - detratores) / total) * 100 if total > 0 else 0
            
            estatisticas = {
                'total': total,
                'promotores': promotores,
                'neutros': neutros,
                'detratores': detratores,
                'nps_score': round(nps_score, 2),
                'percentual_promotores': round((promotores / total) * 100, 2) if total > 0 else 0,
                'percentual_neutros': round((neutros / total) * 100, 2) if total > 0 else 0,
                'percentual_detratores': round((detratores / total) * 100, 2) if total > 0 else 0
            }
            
            return NPSPesquisaResponse(
                success=True,
                message="Estatísticas calculadas com sucesso",
                data=estatisticas
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {str(e)}")
            return NPSPesquisaResponse(
                success=False,
                message="Erro ao calcular estatísticas",
                error=str(e)
            )

# Instância global do serviço
nps_service = NPSService()

