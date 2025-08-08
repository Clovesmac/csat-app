from datetime import datetime
from typing import Optional, Dict, Any
import re

class NPSPesquisaSimple:
    """Modelo simplificado para validação de dados de pesquisa NPS"""
    
    def __init__(self, **kwargs):
        self.filial = kwargs.get('filial', '')
        self.score = kwargs.get('score')
        self.nome = kwargs.get('nome', '')
        self.email = kwargs.get('email', '')
        self.telefone = kwargs.get('telefone', '')
        self.cnpj = kwargs.get('cnpj', '')
        self.comentario = kwargs.get('comentario', '')
        self.timestamp = kwargs.get('timestamp')
    
    def validate(self) -> tuple[bool, str]:
        """Valida os dados da pesquisa"""
        
        # Validar campos obrigatórios
        if not self.filial or not self.filial.strip():
            return False, "Filial é obrigatória"
        
        if self.score is None:
            return False, "Score é obrigatório"
        
        try:
            score_int = int(self.score)
            if score_int < 0 or score_int > 10:
                return False, "Score deve estar entre 0 e 10"
            self.score = score_int
        except (ValueError, TypeError):
            return False, "Score deve ser um número entre 0 e 10"
        
        # Validar email se fornecido
        if self.email and self.email.strip():
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, self.email):
                return False, "Email inválido"
        
        # Validar CNPJ se fornecido
        if self.cnpj and self.cnpj.strip():
            cnpj_clean = re.sub(r'[^\d]', '', self.cnpj)
            if len(cnpj_clean) != 14:
                return False, "CNPJ deve ter 14 dígitos"
        
        # Validar telefone se fornecido
        if self.telefone and self.telefone.strip():
            tel_clean = re.sub(r'[^\d]', '', self.telefone)
            if len(tel_clean) < 10 or len(tel_clean) > 11:
                return False, "Telefone deve ter 10 ou 11 dígitos"
        
        # Validar tamanhos
        if len(self.filial) > 50:
            return False, "Filial deve ter no máximo 50 caracteres"
        
        if self.nome and len(self.nome) > 100:
            return False, "Nome deve ter no máximo 100 caracteres"
        
        if self.email and len(self.email) > 100:
            return False, "Email deve ter no máximo 100 caracteres"
        
        if self.comentario and len(self.comentario) > 500:
            return False, "Comentário deve ter no máximo 500 caracteres"
        
        return True, "Dados válidos"
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o modelo para dicionário para inserção no banco"""
        
        # Adiciona timestamp se não existir
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        
        # Determina categoria NPS
        if self.score >= 9:
            categoria_nps = 'promotor'
        elif self.score >= 7:
            categoria_nps = 'neutro'
        else:
            categoria_nps = 'detrator'
        
        data = {
            'filial': self.filial.strip(),
            'score': self.score,
            'categoria_nps': categoria_nps,
            'timestamp': self.timestamp
        }
        
        # Adicionar campos opcionais apenas se não estiverem vazios
        if self.nome and self.nome.strip():
            data['nome'] = self.nome.strip()
        
        if self.email and self.email.strip():
            data['email'] = self.email.strip()
        
        if self.telefone and self.telefone.strip():
            data['telefone'] = self.telefone.strip()
        
        if self.cnpj and self.cnpj.strip():
            data['cnpj'] = self.cnpj.strip()
        
        if self.comentario and self.comentario.strip():
            data['comentario'] = self.comentario.strip()
        
        return data

class NPSResponse:
    """Classe para padronizar respostas da API"""
    
    def __init__(self, success: bool, message: str, data: Any = None, error: str = None):
        self.success = success
        self.message = message
        self.data = data
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'success': self.success,
            'message': self.message
        }
        
        if self.data is not None:
            result['data'] = self.data
        
        if self.error is not None:
            result['error'] = self.error
        
        return result

