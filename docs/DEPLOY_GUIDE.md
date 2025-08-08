# Guia de Deploy

Este documento explica como fazer o deploy do sistema de pesquisa NPS da Digital Sat em diferentes plataformas.

## 🌐 **Opções de Deploy**

### 1. Manus Platform (Recomendado)
### 2. Vercel (Frontend) + Railway (Backend)
### 3. Netlify (Frontend) + Heroku (Backend)
### 4. Docker + VPS

---

## 🚀 **Deploy na Manus Platform**

### Pré-requisitos
- Projeto configurado localmente
- Supabase configurado

### Passos

#### 1. Preparar Projeto
```bash
# Build do frontend
cd frontend
npm run build

# Copiar build para backend
cp -r dist/* ../backend/src/static/
```

#### 2. Deploy
```bash
# Na pasta do backend
cd backend

# Deploy usando Manus CLI (se disponível)
manus deploy

# Ou seguir instruções específicas da plataforma
```

#### 3. Configurar Variáveis
Configure as variáveis de ambiente:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SECRET_KEY`

---

## ⚡ **Deploy Vercel + Railway**

### Frontend (Vercel)

#### 1. Preparar Repositório
```bash
# Criar repositório apenas do frontend
git subtree push --prefix=frontend origin frontend-only
```

#### 2. Deploy no Vercel
1. Conecte seu repositório GitHub
2. Configure build settings:
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Configure variáveis de ambiente:
   - `VITE_API_URL`: URL do backend no Railway

#### 3. Configurar Proxy (se necessário)
```javascript
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': {
        target: 'https://seu-backend.railway.app',
        changeOrigin: true
      }
    }
  }
}
```

### Backend (Railway)

#### 1. Preparar Projeto
```bash
# Criar Procfile
echo "web: python src/main.py" > backend/Procfile

# Atualizar main.py para usar PORT do ambiente
# app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

#### 2. Deploy no Railway
1. Conecte repositório GitHub
2. Configure variáveis de ambiente
3. Deploy automático

---

## 🌍 **Deploy Netlify + Heroku**

### Frontend (Netlify)

#### 1. Build Settings
- **Build command**: `npm run build`
- **Publish directory**: `dist`

#### 2. Redirects
Criar `frontend/public/_redirects`:
```
/api/* https://seu-app.herokuapp.com/api/:splat 200
/* /index.html 200
```

### Backend (Heroku)

#### 1. Preparar Projeto
```bash
# Criar Procfile
echo "web: python src/main.py" > backend/Procfile

# Criar runtime.txt
echo "python-3.11.0" > backend/runtime.txt
```

#### 2. Deploy
```bash
# Instalar Heroku CLI
# heroku create seu-app-nps

# Deploy
git subtree push --prefix=backend heroku main
```

---

## 🐳 **Deploy com Docker**

### Dockerfile Frontend
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Dockerfile Backend
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/main.py"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SECRET_KEY=${SECRET_KEY}
```

---

## 🔧 **Configurações de Produção**

### Variáveis de Ambiente

#### Obrigatórias
```env
SUPABASE_URL=https://xxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SECRET_KEY=sua-chave-secreta-muito-forte
```

#### Opcionais
```env
FLASK_ENV=production
PORT=5000
CORS_ORIGINS=https://seu-frontend.com
```

### Configurações de Segurança

#### 1. CORS
```python
# Configurar CORS para produção
CORS(app, origins=[
    "https://seu-frontend.com",
    "https://www.seu-frontend.com"
])
```

#### 2. HTTPS
- Sempre use HTTPS em produção
- Configure certificados SSL
- Redirecione HTTP para HTTPS

#### 3. Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/nps', methods=['POST'])
@limiter.limit("10 per minute")
def criar_pesquisa():
    # ...
```

---

## 📊 **Monitoramento**

### Logs
```python
import logging

# Configurar logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### Health Checks
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
```

### Métricas
- Configure alertas para erros 5xx
- Monitore tempo de resposta
- Acompanhe uso de recursos

---

## 🆘 **Solução de Problemas**

### Erro de CORS
```javascript
// Verificar se API_URL está correto
const API_URL = import.meta.env.VITE_API_URL || '/api';
```

### Erro de Build
```bash
# Limpar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Erro de Conexão com Banco
- Verificar variáveis de ambiente
- Testar conexão com Supabase
- Verificar logs do backend

---

## 📋 **Checklist de Deploy**

### Antes do Deploy
- [ ] Testes locais passando
- [ ] Build do frontend funcionando
- [ ] Variáveis de ambiente configuradas
- [ ] Supabase configurado
- [ ] CORS configurado corretamente

### Após o Deploy
- [ ] Health check funcionando
- [ ] Frontend carregando corretamente
- [ ] API respondendo
- [ ] Banco de dados conectado
- [ ] Formulário enviando dados
- [ ] Logs funcionando

### Monitoramento Contínuo
- [ ] Alertas configurados
- [ ] Backup do banco configurado
- [ ] SSL/HTTPS funcionando
- [ ] Performance monitorada

