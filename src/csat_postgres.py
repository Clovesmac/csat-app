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
    # Tentar usar PostgreSQL se disponível
    postgres_url = os.environ.get('DATABASE_URL')
    if postgres_url:
        return postgres_url
    
    # Fallback para SQLite local (para desenvolvimento)
    return f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')}"

