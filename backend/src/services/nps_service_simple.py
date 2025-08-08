from typing import Dict, Any
from src.database.supabase_client_simple import simple_supabase_client
from src.models.nps_pesquisa_simple import NPSPesquisaSimple, NPSResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NPSServiceSimple:
    """Serviço simplificado para operações relacionadas a pesquisas NPS"""
    
    def __init__(self):
        self.client = simple_supabase_client
        self.table_name = 'nps_pesquisas'
    
    def criar_pesquisa(self, dados: Dict[str, Any]) -> NPSResponse:
        """Cria uma nova pesquisa NPS"""
        try:
            # Validar dados usando modelo simplificado
            pesquisa = NPSPesquisaSimple(**dados)
            
            # Validar
            valido, mensagem = pesquisa.validate()
            if not valido:
                logger.error(f"Erro de validação: {mensagem}")
                return NPSResponse(
                    success=False,
                    message="Dados inválidos",
                    error=mensagem
                )
            
            # Converter para dicionário
            dados_inserir = pesquisa.to_dict()
            
            # Inserir no Supabase
            sucesso, resultado = self.client.insert(self.table_name, dados_inserir)
            
            if sucesso:
                logger.info(f"Pesquisa NPS criada com sucesso")
                return NPSResponse(
                    success=True,
                    message="Pesquisa NPS salva com sucesso",
                    data=resultado
                )
            else:
                logger.error(f"Erro ao inserir pesquisa NPS: {resultado}")
                return NPSResponse(
                    success=False,
                    message="Erro ao salvar pesquisa",
                    error=resultado.get('error', 'Erro desconhecido')
                )
                
        except Exception as e:
            logger.error(f"Erro ao criar pesquisa NPS: {str(e)}")
            return NPSResponse(
                success=False,
                message="Erro interno do servidor",
                error=str(e)
            )
    
    def listar_pesquisas(self, filial: str = None, limite: int = 100) -> NPSResponse:
        """Lista pesquisas NPS com filtros opcionais"""
        try:
            filtros = {}
            if filial:
                filtros['filial'] = filial
            
            sucesso, resultado = self.client.select(self.table_name, filtros, limite)
            
            if sucesso:
                return NPSResponse(
                    success=True,
                    message=f"Encontradas {len(resultado)} pesquisas",
                    data=resultado
                )
            else:
                return NPSResponse(
                    success=False,
                    message="Erro ao buscar pesquisas",
                    error=resultado.get('error', 'Erro desconhecido')
                )
            
        except Exception as e:
            logger.error(f"Erro ao listar pesquisas: {str(e)}")
            return NPSResponse(
                success=False,
                message="Erro ao buscar pesquisas",
                error=str(e)
            )
    
    def obter_estatisticas(self, filial: str = None) -> NPSResponse:
        """Obtém estatísticas das pesquisas NPS"""
        try:
            filtros = {}
            if filial:
                filtros['filial'] = filial
            
            sucesso, resultado = self.client.select(self.table_name, filtros, 1000)
            
            if not sucesso:
                return NPSResponse(
                    success=False,
                    message="Erro ao buscar dados para estatísticas",
                    error=resultado.get('error', 'Erro desconhecido')
                )
            
            if not resultado:
                return NPSResponse(
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
            total = len(resultado)
            promotores = len([p for p in resultado if p.get('categoria_nps') == 'promotor'])
            detratores = len([p for p in resultado if p.get('categoria_nps') == 'detrator'])
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
            
            return NPSResponse(
                success=True,
                message="Estatísticas calculadas com sucesso",
                data=estatisticas
            )
            
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {str(e)}")
            return NPSResponse(
                success=False,
                message="Erro ao calcular estatísticas",
                error=str(e)
            )

# Instância global do serviço
nps_service_simple = NPSServiceSimple()

