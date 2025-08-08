# Sistema de Pesquisa NPS - Digital Sat

Sistema completo de pesquisa Net Promoter Score (NPS) desenvolvido para a Digital Sat, com frontend React e backend Flask integrados.

## 🌐 **Demo Online**
**URL**: https://g8h3ilc179d1.manus.space

## 📋 **Sobre o Projeto**

A Digital Sat é uma distribuidora de produtos de segurança eletrônica e conectividade com mais de 25 anos de mercado. Este sistema permite coletar feedback dos clientes através de pesquisas NPS personalizadas por filial.

## ✨ **Funcionalidades**

### 🎯 **Pesquisa NPS Completa**
- Escala de avaliação de 0 a 10 com categorização automática
- Feedback personalizado baseado na nota (Promotor/Neutro/Detrator)
- Campos opcionais: nome, email, telefone, CNPJ
- Comentários com validação de caracteres
- Textos dinâmicos baseados na pontuação

### 🏢 **Sistema Multi-Filial**
- 12 filiais da Digital Sat disponíveis
- Seleção via dropdown ou parâmetro URL
- Pré-preenchimento de dados via URL

### 📱 **Interface Responsiva**
- Design moderno e profissional
- Totalmente responsivo (mobile/tablet/desktop)
- Rolagem automática ao selecionar nota
- Identidade visual da Digital Sat

### 🔧 **Backend Robusto**
- API REST completa com Flask
- Validação robusta de dados
- Integração com Supabase
- Logs e monitoramento
- CORS configurado

## 🏗️ **Arquitetura**

```
├── frontend/          # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── lib/          # Utilitários e dados
│   │   └── hooks/        # Hooks customizados
│   └── dist/             # Build de produção
│
├── backend/           # Flask + Python
│   ├── src/
│   │   ├── routes/       # Endpoints da API
│   │   ├── services/     # Lógica de negócio
│   │   ├── models/       # Modelos de dados
│   │   └── database/     # Conexão Supabase
│   └── requirements.txt  # Dependências Python
│
└── docs/              # Documentação
```

## 🚀 **Tecnologias Utilizadas**

### Frontend
- **React 18** - Framework JavaScript
- **Vite** - Build tool e dev server
- **Tailwind CSS** - Framework CSS
- **shadcn/ui** - Componentes UI
- **Lucide Icons** - Ícones

### Backend
- **Flask** - Framework web Python
- **Python 3.11** - Linguagem de programação
- **Supabase** - Banco de dados PostgreSQL
- **Flask-CORS** - Configuração CORS

### Deploy
- **Manus Platform** - Hospedagem e deploy

## 📊 **Filiais Disponíveis**

| Código | Nome | Região |
|--------|------|--------|
| `balneario-camboriu` | Balneário Camboriú | SC |
| `blumenau` | Blumenau | SC |
| `brusque` | Brusque | SC |
| `centro-distribuicao` | Centro de Distribuição | SC |
| `gravatai` | Gravataí | RS |
| `itajai` | Itajaí | SC |
| `itapema` | Itapema | SC |
| `joinville` | Joinville | SC |
| `lages` | Lages | SC |
| `rio-do-sul` | Rio do Sul | SC |
| `sao-jose` | São José | SC |
| `tubarao` | Tubarão | SC |

## 🔗 **Exemplos de Uso**

### Seleção Manual
```
https://g8h3ilc179d1.manus.space
```

### Filial Pré-selecionada
```
https://g8h3ilc179d1.manus.space/?filial=blumenau
https://g8h3ilc179d1.manus.space/?filial=joinville
```

### Filial + CNPJ Pré-preenchidos
```
https://g8h3ilc179d1.manus.space/?filial=blumenau&cnpj=12.345.678/0001-90
```

## 📡 **API Endpoints**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/health` | Status geral da API |
| `GET` | `/api/nps/health` | Status da API NPS |
| `POST` | `/api/nps` | Criar pesquisa NPS |
| `GET` | `/api/nps` | Listar pesquisas |
| `GET` | `/api/nps/estatisticas` | Estatísticas NPS |

## 🗄️ **Banco de Dados**

### Estrutura da Tabela `nps_pesquisas`

```sql
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
```

## ⚙️ **Configuração e Instalação**

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/nps-digital-sat.git
cd nps-digital-sat
```

### 2. Configure o Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Configure o Frontend
```bash
cd frontend
npm install
```

### 4. Configure o Supabase
1. Crie uma conta em [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Execute o SQL da estrutura do banco
4. Configure as variáveis de ambiente:

```env
# backend/.env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon
SECRET_KEY=sua-chave-secreta
```

### 5. Execute o Projeto

#### Desenvolvimento
```bash
# Backend (porta 5000)
cd backend
python src/main.py

# Frontend (porta 5173)
cd frontend
npm run dev
```

#### Produção
```bash
# Build do frontend
cd frontend
npm run build

# Copiar build para backend
cp -r dist/* ../backend/src/static/

# Executar backend com frontend integrado
cd ../backend
python src/main.py
```

## 📈 **Métricas NPS**

O sistema calcula automaticamente:
- **NPS Score**: (% Promotores - % Detratores)
- **Categorização**: Promotor (9-10), Neutro (7-8), Detrator (0-6)
- **Estatísticas**: Total de respostas, distribuição por categoria
- **Filtros**: Por filial e período

## 🔒 **Segurança**

- Validação de dados no frontend e backend
- Sanitização de inputs
- CORS configurado adequadamente
- Logs de operações importantes
- Tratamento robusto de erros

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 **Contato**

**Digital Sat** - Distribuidora de Produtos de Segurança Eletrônica e Conectividade
- Website: [digitalsat.com.br](https://digitalsat.com.br)
- Há mais de 25 anos levando soluções tecnológicas aos nossos clientes e parceiros

## 🙏 **Agradecimentos**

- Equipe Digital Sat pelo feedback e requisitos
- Comunidade React e Flask pelas ferramentas
- Supabase pela infraestrutura de banco de dados

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**

