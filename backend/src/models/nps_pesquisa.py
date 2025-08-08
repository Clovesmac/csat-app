from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, validator, Field
import re

class NPSPesquisaModel(BaseModel):
    """Modelo para validação de dados de pesquisa NPS"""
    
    # Campos obrigatórios
    filial: str = Field(..., min_length=1, max_length=50)
    score: int = Field(..., ge=0, le=10)
    
    # Campos opcionais
    nome: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    cnpj: Optional[str] = Field(None, max_length=20)
    comentario: Optional[str] = Field(None, max_length=500)
    
    # Campos automáticos
    timestamp: Optional[datetime] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v and v.strip():
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, v):
                raise ValueError('Email inválido')
        return v
    
    @validator('cnpj')
    def validate_cnpj(cls, v):
        if v and v.strip():
            # Remove caracteres especiais
            cnpj_clean = re.sub(r'[^\d]', '', v)
            if len(cnpj_clean) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
        return v
    
    @validator('telefone')
    def validate_telefone(cls, v):
        if v and v.strip():
            # Remove caracteres especiais
            tel_clean = re.sub(r'[^\d]', '', v)
            if len(tel_clean) < 10 or len(tel_clean) > 11:
                raise ValueError('Telefone deve ter 10 ou 11 dígitos')
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o modelo para dicionário para inserção no banco"""
        data = self.dict(exclude_none=True)
        
        # Adiciona timestamp se não existir
        if 'timestamp' not in data or data['timestamp'] is None:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Determina categoria NPS
        if self.score >= 9:
            data['categoria_nps'] = 'promotor'
        elif self.score >= 7:
            data['categoria_nps'] = 'neutro'
        else:
            data['categoria_nps'] = 'detrator'
        
        return data

class NPSPesquisaResponse(BaseModel):
    """Modelo para resposta da API"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

