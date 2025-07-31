from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class CSATResponse(db.Model):
    __tablename__ = 'csat_response'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    context = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'context': self.context,
            'comment': self.comment,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

# Configuração para usar PostgreSQL ou SQLite como fallback
def get_database_url():
    # Usar PostgreSQL do Render.com
    postgres_url = os.environ.get('DATABASE_URL')
    if postgres_url:
        return postgres_url
    
    # URL padrão do PostgreSQL do Render.com (para produção)
    render_postgres_url = "postgresql://csat_user:hkdsCJ9zEjXO0TjdMivgwmdEr0e6SUZb@dpg-d25m5rndiees73c2faqg-a.singapore-postgres.render.com/csat_db"
    
    # Verificar se estamos em produção (Render.com)
    if os.environ.get('RENDER'):
        return render_postgres_url
    
    # Para desenvolvimento local, usar a URL do Render também
    return render_postgres_url

