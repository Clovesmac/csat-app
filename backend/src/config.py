import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    # Configurações do Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    @staticmethod
    def validate_config():
        """Valida se as configurações necessárias estão presentes"""
        if not Config.SUPABASE_URL:
            raise ValueError("SUPABASE_URL não configurada")
        if not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY não configurada")
        return True

