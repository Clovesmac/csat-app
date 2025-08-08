import os
import requests
from typing import Dict, Any, Tuple

class SimpleSupabaseClient:
    """Cliente Supabase simplificado usando apenas requests"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def insert(self, table: str, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Insere dados em uma tabela"""
        try:
            if not self.url or not self.key:
                return False, {'error': 'Configurações do Supabase não encontradas'}
            
            url = f"{self.url}/rest/v1/{table}"
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            
            if response.status_code in [200, 201]:
                return True, response.json()[0] if response.json() else data
            else:
                return False, {'error': f'HTTP {response.status_code}: {response.text}'}
                
        except Exception as e:
            return False, {'error': str(e)}
    
    def select(self, table: str, filters: Dict[str, Any] = None, limit: int = 100) -> Tuple[bool, Dict[str, Any]]:
        """Seleciona dados de uma tabela"""
        try:
            if not self.url or not self.key:
                return False, {'error': 'Configurações do Supabase não encontradas'}
            
            url = f"{self.url}/rest/v1/{table}"
            params = {'limit': limit}
            
            if filters:
                for key, value in filters.items():
                    params[f'{key}'] = f'eq.{value}'
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, {'error': f'HTTP {response.status_code}: {response.text}'}
                
        except Exception as e:
            return False, {'error': str(e)}
    
    def test_connection(self) -> Tuple[bool, str]:
        """Testa a conexão com o Supabase"""
        try:
            if not self.url or not self.key:
                return False, "Configurações do Supabase não encontradas"
            
            # Tenta fazer uma consulta simples
            success, result = self.select('nps_pesquisas', limit=1)
            
            if success:
                return True, "Conexão com Supabase estabelecida com sucesso"
            else:
                return False, f"Erro na conexão: {result.get('error', 'Erro desconhecido')}"
                
        except Exception as e:
            return False, f"Erro na conexão: {str(e)}"

# Instância global do cliente
simple_supabase_client = SimpleSupabaseClient()

