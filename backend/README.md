# API de Pesquisas Digital Sat

Backend para sistema de pesquisas da Digital Sat, incluindo pesquisas NPS e outros tipos de pesquisas.

## 🏗️ Arquitetura

- **Framework**: Flask (Python)
- **Banco de Dados**: Supabase (PostgreSQL)
- **Validação**: Pydantic
- **CORS**: Flask-CORS

## 📋 Pré-requisitos

1. **Projeto Supabase**: Crie um projeto em https://supabase.com/
2. **Tabela NPS**: Execute o SQL abaixo no Supabase SQL Editor

```sql
-- Criar tabela para pesquisas NPS
CREATE TABLE nps_pesquisas (
    id SERIAL PRIMARY KEY,
    filial VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 10),
    categoria_nps VARCHAR(20) NOT NULL CHECK (categoria_nps IN ('promotor', 'neutro', 'detrator')),
    nome VARCHAR(100),
    email VARCHAR(100),
    telefone VARCHAR(20),
    cnpj VARCHAR(20),
    comentario TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX idx_nps_filial ON nps_pesquisas(filial);
CREATE INDEX idx_nps_score ON nps_pesquisas(score);
CREATE INDEX idx_nps_categoria ON nps_pesquisas(categoria_nps);
CREATE INDEX idx_nps_timestamp ON nps_pesquisas(timestamp);

-- Habilitar RLS (Row Level Security) se necessário
ALTER TABLE nps_pesquisas ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserção e leitura (ajuste conforme necessário)
CREATE POLICY "Permitir todas operações" ON nps_pesquisas
    FOR ALL USING (true);
```

## ⚙️ Configuração

1. **Clone e configure o projeto**:
```bash
cd pesquisa-backend
source venv/bin/activate
```

2. **Configure as variáveis de ambiente** no arquivo `.env`:
```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta
```

3. **Obter credenciais do Supabase**:
   - URL: Painel Supabase → Settings → API → Project URL
   - Key: Painel Supabase → Settings → API → Project API keys → anon/public

## 🚀 Execução

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação
python src/main.py
```

A API estará disponível em: `http://localhost:5000`

## 📡 Endpoints da API

### Saúde da API
- `GET /api/health` - Status geral da API
- `GET /api/nps/health` - Status da API NPS e conexão com banco

### Pesquisas NPS
- `POST /api/nps` - Criar nova pesquisa NPS
- `GET /api/nps` - Listar pesquisas NPS
- `GET /api/nps/estatisticas` - Obter estatísticas NPS

## 📝 Exemplo de Uso

### Criar Pesquisa NPS
```bash
curl -X POST http://localhost:5000/api/nps \\
  -H "Content-Type: application/json" \\
  -d '{
    "filial": "blumenau",
    "score": 9,
    "nome": "João Silva",
    "email": "joao@email.com",
    "telefone": "(47) 99999-9999",
    "cnpj": "12.345.678/0001-90",
    "comentario": "Excelente atendimento!"
  }'
```

### Resposta de Sucesso
```json
{
  "success": true,
  "message": "Pesquisa NPS salva com sucesso",
  "data": {
    "id": 1,
    "filial": "blumenau",
    "score": 9,
    "categoria_nps": "promotor",
    "nome": "João Silva",
    "email": "joao@email.com",
    "telefone": "(47) 99999-9999",
    "cnpj": "12.345.678/0001-90",
    "comentario": "Excelente atendimento!",
    "timestamp": "2025-01-01T12:00:00Z"
  }
}
```

## 🔍 Validações

- **Score**: Obrigatório, entre 0 e 10
- **Filial**: Obrigatória, máximo 50 caracteres
- **Email**: Formato válido (se fornecido)
- **CNPJ**: 14 dígitos (se fornecido)
- **Telefone**: 10 ou 11 dígitos (se fornecido)
- **Comentário**: Máximo 500 caracteres

## 📊 Categorização NPS

- **Promotores**: Score 9-10
- **Neutros**: Score 7-8  
- **Detratores**: Score 0-6

## 🛠️ Estrutura do Projeto

```
pesquisa-backend/
├── src/
│   ├── config.py              # Configurações
│   ├── main.py                # Aplicação principal
│   ├── database/
│   │   └── supabase_client.py # Cliente Supabase
│   ├── models/
│   │   └── nps_pesquisa.py    # Modelos Pydantic
│   ├── routes/
│   │   └── nps.py             # Rotas da API NPS
│   ├── services/
│   │   └── nps_service.py     # Lógica de negócio
│   └── static/                # Frontend (quando integrado)
├── .env                       # Variáveis de ambiente
├── requirements.txt           # Dependências Python
└── README.md                  # Esta documentação
```

## 🔒 Segurança

- CORS configurado para permitir requisições do frontend
- Validação de dados com Pydantic
- Logs de operações importantes
- Tratamento de erros robusto

## 📈 Próximos Passos

1. Implementar autenticação/autorização
2. Adicionar cache (Redis)
3. Implementar rate limiting
4. Adicionar métricas e monitoramento
5. Testes automatizados

