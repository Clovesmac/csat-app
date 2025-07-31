"""
Gerenciador de armazenamento persistente para dados CSAT
Implementa múltiplas estratégias de persistência para garantir que os dados não sejam perdidos
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import threading

class PersistentStorage:
    """Gerenciador de armazenamento com múltiplas estratégias de persistência"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), '..', 'persistent_data')
        
        self.storage_dir = storage_dir
        self.json_file = os.path.join(storage_dir, 'csat_data.json')
        self.backup_file = os.path.join(storage_dir, 'csat_backup.json')
        self._lock = threading.Lock()
        
        # Criar diretório se não existir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Carregar dados existentes
        self._data = self._load_data()
        
    def _load_data(self) -> List[Dict]:
        """Carregar dados do arquivo JSON"""
        try:
            # Tentar carregar arquivo principal
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            
            # Tentar carregar backup
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                        
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
        
        return []
    
    def _save_data(self):
        """Salvar dados no arquivo JSON com backup"""
        try:
            with self._lock:
                # Criar backup do arquivo atual
                if os.path.exists(self.json_file):
                    import shutil
                    shutil.copy2(self.json_file, self.backup_file)
                
                # Salvar dados atuais
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(self._data, f, ensure_ascii=False, indent=2, default=str)
                    
                print(f"Dados salvos: {len(self._data)} registros")
                
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def add_response(self, rating: int, context: str = None, comment: str = None) -> int:
        """Adicionar nova resposta CSAT"""
        with self._lock:
            # Gerar novo ID
            next_id = max([item.get('id', 0) for item in self._data], default=0) + 1
            
            # Criar novo registro
            new_response = {
                'id': next_id,
                'rating': rating,
                'context': context or '',
                'comment': comment or '',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self._data.append(new_response)
            self._save_data()
            
            return next_id
    
    def get_all_responses(self) -> List[Dict]:
        """Obter todas as respostas"""
        with self._lock:
            # Ordenar por timestamp (mais recente primeiro)
            sorted_data = sorted(self._data, key=lambda x: x.get('timestamp', ''), reverse=True)
            return sorted_data.copy()
    
    def get_stats(self) -> Dict:
        """Obter estatísticas das respostas"""
        with self._lock:
            if not self._data:
                return {
                    'total': 0,
                    'average': 0,
                    'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                    'high_satisfaction': 0,
                    'last_update': None
                }
            
            ratings = [item['rating'] for item in self._data]
            total = len(ratings)
            average = sum(ratings) / total
            
            # Distribuição por rating
            distribution = {}
            for i in range(1, 6):
                distribution[i] = sum(1 for r in ratings if r == i)
            
            # Satisfação alta (4-5 estrelas)
            high_satisfaction = sum(1 for r in ratings if r >= 4)
            
            # Última atualização
            timestamps = [item.get('timestamp') for item in self._data if item.get('timestamp')]
            last_update = max(timestamps) if timestamps else None
            
            return {
                'total': total,
                'average': round(average, 1),
                'distribution': distribution,
                'high_satisfaction': high_satisfaction,
                'last_update': last_update
            }
    
    def export_to_csv(self) -> str:
        """Exportar dados para formato CSV"""
        import csv
        import io
        
        with self._lock:
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Cabeçalho
            writer.writerow(['ID', 'Contexto', 'Avaliação', 'Comentário', 'Data/Hora'])
            
            # Dados
            for item in sorted(self._data, key=lambda x: x.get('timestamp', ''), reverse=True):
                rating_text = {
                    1: '1 - Muito Insatisfeito',
                    2: '2 - Insatisfeito', 
                    3: '3 - Neutro',
                    4: '4 - Satisfeito',
                    5: '5 - Muito Satisfeito'
                }.get(item['rating'], str(item['rating']))
                
                # Formatar data
                timestamp_str = item.get('timestamp', '')
                if timestamp_str:
                    try:
                        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%d/%m/%Y %H:%M:%S')
                    except:
                        formatted_date = timestamp_str
                else:
                    formatted_date = ''
                
                writer.writerow([
                    item.get('id', ''),
                    item.get('context', ''),
                    rating_text,
                    item.get('comment', ''),
                    formatted_date
                ])
            
            return output.getvalue()
    
    def get_storage_info(self) -> Dict:
        """Obter informações sobre o armazenamento"""
        with self._lock:
            info = {
                'storage_type': 'JSON File Storage',
                'storage_location': self.json_file,
                'backup_location': self.backup_file,
                'total_records': len(self._data),
                'file_exists': os.path.exists(self.json_file),
                'backup_exists': os.path.exists(self.backup_file)
            }
            
            if os.path.exists(self.json_file):
                stat = os.stat(self.json_file)
                info['file_size'] = stat.st_size
                info['last_modified'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            return info

# Instância global do gerenciador de armazenamento
storage_manager = PersistentStorage()

