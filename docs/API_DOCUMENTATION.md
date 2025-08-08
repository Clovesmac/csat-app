# Documentação da API

API REST para o sistema de pesquisa NPS da Digital Sat.

## 📡 **Base URL**

```
Produção: https://g8h3ilc179d1.manus.space/api
Local: http://localhost:5000/api
```

## 🔐 **Autenticação**

Atualmente a API é pública e não requer autenticação. Para uso em produção, considere implementar autenticação via API key ou JWT.

## 📋 **Endpoints**

### 1. Health Check Geral

#### `GET /health`

Verifica o status geral da API.

**Resposta:**
```json
{
  "status": "ok",
  "message": "API de Pesquisas Digital Sat funcionando",
  "version": "1.0.0"
}
```

---

### 2. Health Check NPS

#### `GET /nps/health`

Verifica o status da API NPS e conexão com banco de dados.

**Resposta (Sucesso):**
```json
{
  "success": true,
  "message": "API NPS funcionando",
  "database_status": "conectado",
  "database_message": "Conexão com Supabase estabelecida com sucesso"
}
```

**Resposta (Erro):**
```json
{
  "success": true,
  "message": "API NPS funcionando",
  "database_status": "erro",
  "database_message": "Erro na conexão: [detalhes do erro]"
}
```

---

### 3. Criar Pesquisa NPS

#### `POST /nps`

Cria uma nova pesquisa NPS.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "filial": "blumenau",
  "score": 9,
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "(47) 99999-9999",
  "cnpj": "12.345.678/0001-90",
  "comentario": "Excelente atendimento!"
}
```

**Campos:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `filial` | string | ✅ | Código da filial (máx. 50 chars) |
| `score` | integer | ✅ | Nota de 0 a 10 |
| `nome` | string | ❌ | Nome do cliente (máx. 100 chars) |
| `email` | string | ❌ | Email válido (máx. 100 chars) |
| `telefone` | string | ❌ | Telefone com 10-11 dígitos |
| `cnpj` | string | ❌ | CNPJ com 14 dígitos |
| `comentario` | string | ❌ | Comentário (máx. 500 chars) |

**Resposta (Sucesso - 201):**
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

**Resposta (Erro - 400):**
```json
{
  "success": false,
  "message": "Dados inválidos",
  "error": "Score deve estar entre 0 e 10"
}
```

---

### 4. Listar Pesquisas

#### `GET /nps`

Lista pesquisas NPS com filtros opcionais.

**Query Parameters:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `filial` | string | Filtrar por filial |
| `limite` | integer | Limite de resultados (máx. 1000) |

**Exemplos:**
```
GET /nps
GET /nps?filial=blumenau
GET /nps?limite=50
GET /nps?filial=joinville&limite=100
```

**Resposta (Sucesso - 200):**
```json
{
  "success": true,
  "message": "Encontradas 3 pesquisas",
  "data": [
    {
      "id": 1,
      "filial": "blumenau",
      "score": 9,
      "categoria_nps": "promotor",
      "nome": "João Silva",
      "email": "joao@email.com",
      "comentario": "Excelente atendimento!",
      "timestamp": "2025-01-01T12:00:00Z"
    },
    {
      "id": 2,
      "filial": "blumenau",
      "score": 7,
      "categoria_nps": "neutro",
      "nome": "Maria Santos",
      "comentario": "Bom serviço",
      "timestamp": "2025-01-01T11:00:00Z"
    }
  ]
}
```

---

### 5. Estatísticas NPS

#### `GET /nps/estatisticas`

Obtém estatísticas das pesquisas NPS.

**Query Parameters:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `filial` | string | Filtrar por filial |

**Exemplos:**
```
GET /nps/estatisticas
GET /nps/estatisticas?filial=blumenau
```

**Resposta (Sucesso - 200):**
```json
{
  "success": true,
  "message": "Estatísticas calculadas com sucesso",
  "data": {
    "total": 100,
    "promotores": 60,
    "neutros": 25,
    "detratores": 15,
    "nps_score": 45.0,
    "percentual_promotores": 60.0,
    "percentual_neutros": 25.0,
    "percentual_detratores": 15.0
  }
}
```

**Campos da Resposta:**

| Campo | Descrição |
|-------|-----------|
| `total` | Total de pesquisas |
| `promotores` | Quantidade de promotores (score 9-10) |
| `neutros` | Quantidade de neutros (score 7-8) |
| `detratores` | Quantidade de detratores (score 0-6) |
| `nps_score` | Score NPS calculado (% promotores - % detratores) |
| `percentual_*` | Percentuais de cada categoria |

---

## 🏢 **Filiais Válidas**

| Código | Nome |
|--------|------|
| `balneario-camboriu` | Balneário Camboriú |
| `blumenau` | Blumenau |
| `brusque` | Brusque |
| `centro-distribuicao` | Centro de Distribuição |
| `gravatai` | Gravataí - RS |
| `itajai` | Itajaí |
| `itapema` | Itapema |
| `joinville` | Joinville |
| `lages` | Lages |
| `rio-do-sul` | Rio do Sul |
| `sao-jose` | São José |
| `tubarao` | Tubarão |

---

## ❌ **Códigos de Erro**

| Código | Descrição |
|--------|-----------|
| `200` | Sucesso |
| `201` | Criado com sucesso |
| `400` | Dados inválidos |
| `404` | Endpoint não encontrado |
| `500` | Erro interno do servidor |

---

## 📝 **Exemplos de Uso**

### JavaScript (Fetch)

```javascript
// Criar pesquisa NPS
const criarPesquisa = async (dados) => {
  try {
    const response = await fetch('/api/nps', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dados)
    });
    
    const resultado = await response.json();
    
    if (resultado.success) {
      console.log('Pesquisa criada:', resultado.data);
    } else {
      console.error('Erro:', resultado.error);
    }
  } catch (error) {
    console.error('Erro de rede:', error);
  }
};

// Obter estatísticas
const obterEstatisticas = async (filial = null) => {
  const url = filial ? `/api/nps/estatisticas?filial=${filial}` : '/api/nps/estatisticas';
  
  try {
    const response = await fetch(url);
    const resultado = await response.json();
    
    if (resultado.success) {
      console.log('Estatísticas:', resultado.data);
    }
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Python (Requests)

```python
import requests

# Criar pesquisa NPS
def criar_pesquisa(dados):
    url = 'https://g8h3ilc179d1.manus.space/api/nps'
    
    try:
        response = requests.post(url, json=dados)
        resultado = response.json()
        
        if resultado['success']:
            print('Pesquisa criada:', resultado['data'])
        else:
            print('Erro:', resultado['error'])
    except Exception as e:
        print('Erro:', e)

# Obter estatísticas
def obter_estatisticas(filial=None):
    url = 'https://g8h3ilc179d1.manus.space/api/nps/estatisticas'
    params = {'filial': filial} if filial else {}
    
    try:
        response = requests.get(url, params=params)
        resultado = response.json()
        
        if resultado['success']:
            print('Estatísticas:', resultado['data'])
    except Exception as e:
        print('Erro:', e)

# Exemplo de uso
dados_pesquisa = {
    'filial': 'blumenau',
    'score': 9,
    'nome': 'João Silva',
    'comentario': 'Excelente atendimento!'
}

criar_pesquisa(dados_pesquisa)
obter_estatisticas('blumenau')
```

### cURL

```bash
# Criar pesquisa NPS
curl -X POST https://g8h3ilc179d1.manus.space/api/nps \
  -H "Content-Type: application/json" \
  -d '{
    "filial": "blumenau",
    "score": 9,
    "nome": "João Silva",
    "comentario": "Excelente atendimento!"
  }'

# Obter estatísticas
curl https://g8h3ilc179d1.manus.space/api/nps/estatisticas?filial=blumenau

# Listar pesquisas
curl https://g8h3ilc179d1.manus.space/api/nps?limite=10
```

---

## 🔄 **Rate Limiting**

Atualmente não há rate limiting implementado. Para uso em produção, considere implementar:

- Limite por IP: 100 requests/hora
- Limite por endpoint: 10 requests/minuto para POST
- Headers de rate limit nas respostas

---

## 📊 **Monitoramento**

### Logs
Todas as operações são logadas com:
- Timestamp
- IP do cliente
- Endpoint acessado
- Status da resposta
- Tempo de processamento

### Métricas Recomendadas
- Requests por minuto
- Tempo de resposta médio
- Taxa de erro
- Distribuição de scores NPS
- Pesquisas por filial

