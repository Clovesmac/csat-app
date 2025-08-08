from supabase import create_client, Client
from src.config import Config

class SupabaseClient:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            try:
                Config.validate_config()
                self._client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            except Exception as e:
                print(f"Erro ao conectar com Supabase: {e}")
                self._client = None
    
    @property
    def client(self) -> Client:
        if self._client is None:
            raise Exception("Cliente Supabase não inicializado")
        return self._client
    
    def test_connection(self):
        """Testa a conexão com o Supabase"""
        try:
            # Tenta fazer uma consulta simples para testar a conexão
            result = self._client.table('nps_pesquisas').select('*').limit(1).execute()
            return True, "Conexão com Supabase estabelecida com sucesso"
        except Exception as e:
            return False, f"Erro na conexão: {str(e)}"

# Instância global do cliente
supabase_client = SupabaseClient()

