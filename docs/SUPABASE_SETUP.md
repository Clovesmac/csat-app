# Configuração do Supabase

Este guia explica como configurar o banco de dados Supabase para o sistema de pesquisa NPS da Digital Sat.

## 📋 **Pré-requisitos**

- Conta no [Supabase](https://supabase.com) (gratuita)
- Acesso ao painel administrativo do Supabase

## 🚀 **Passo a Passo**

### 1. Criar Conta no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "Start your project"
3. Faça login com GitHub, Google ou email
4. Confirme sua conta via email

### 2. Criar Novo Projeto

1. No dashboard, clique em "New Project"
2. Escolha sua organização
3. Preencha os dados:
   - **Name**: `nps-digital-sat`
   - **Database Password**: Crie uma senha forte
   - **Region**: Escolha a região mais próxima (ex: South America)
4. Clique em "Create new project"
5. Aguarde alguns minutos para o projeto ser criado

### 3. Configurar Banco de Dados

#### 3.1 Acessar SQL Editor
1. No painel lateral, clique em "SQL Editor"
2. Clique em "New query"

#### 3.2 Executar Script de Criação
Cole e execute o seguinte SQL:

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

-- Habilitar RLS (Row Level Security)
ALTER TABLE nps_pesquisas ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserção e leitura
CREATE POLICY "Permitir todas operações" ON nps_pesquisas
    FOR ALL USING (true);

-- Inserir dados de exemplo (opcional)
INSERT INTO nps_pesquisas (filial, score, categoria_nps, nome, email, comentario) VALUES
('blumenau', 9, 'promotor', 'João Silva', 'joao@email.com', 'Excelente atendimento!'),
('joinville', 7, 'neutro', 'Maria Santos', 'maria@email.com', 'Bom serviço, pode melhorar'),
('sao-jose', 3, 'detrator', 'Pedro Costa', 'pedro@email.com', 'Atendimento demorado');
```

#### 3.3 Verificar Criação
1. Clique em "Table Editor" no painel lateral
2. Verifique se a tabela `nps_pesquisas` foi criada
3. Confirme se os dados de exemplo foram inseridos

### 4. Obter Credenciais

#### 4.1 URL do Projeto
1. Vá para "Settings" → "API"
2. Copie a **Project URL**
   - Formato: `https://xxxxxxxxx.supabase.co`

#### 4.2 Chave da API
1. Na mesma página "Settings" → "API"
2. Copie a **anon/public key**
   - Começa com `eyJ...`

### 5. Configurar Variáveis de Ambiente

#### 5.1 Backend Local
Crie o arquivo `backend/.env`:

```env
SUPABASE_URL=https://xxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
```

#### 5.2 Deploy em Produção
Configure as mesmas variáveis no seu serviço de deploy.

### 6. Testar Conexão

#### 6.1 Teste Local
```bash
cd backend
source venv/bin/activate
python src/main.py
```

Acesse: `http://localhost:5000/api/nps/health`

Resposta esperada:
```json
{
  "success": true,
  "message": "API NPS funcionando",
  "database_status": "conectado",
  "database_message": "Conexão com Supabase estabelecida com sucesso"
}
```

#### 6.2 Teste de Inserção
```bash
curl -X POST http://localhost:5000/api/nps \
  -H "Content-Type: application/json" \
  -d '{
    "filial": "blumenau",
    "score": 10,
    "nome": "Teste",
    "comentario": "Teste de integração"
  }'
```

### 7. Monitoramento

#### 7.1 Logs
- Acesse "Logs" no painel do Supabase
- Monitore queries e erros

#### 7.2 Métricas
- Acesse "Reports" para ver estatísticas
- Monitore uso de recursos

## 🔒 **Segurança**

### Configurações Recomendadas

1. **RLS (Row Level Security)**
   - Já habilitado no script
   - Controla acesso aos dados

2. **Políticas de Acesso**
   - Política atual permite todas operações
   - Ajuste conforme necessário

3. **Chaves de API**
   - Use `anon key` para operações públicas
   - Mantenha `service_role key` segura

### Políticas Avançadas (Opcional)

```sql
-- Política mais restritiva (exemplo)
DROP POLICY "Permitir todas operações" ON nps_pesquisas;

-- Permitir apenas inserção
CREATE POLICY "Permitir inserção" ON nps_pesquisas
    FOR INSERT WITH CHECK (true);

-- Permitir leitura apenas para administradores
CREATE POLICY "Permitir leitura admin" ON nps_pesquisas
    FOR SELECT USING (auth.role() = 'admin');
```

## 📊 **Consultas Úteis**

### Estatísticas NPS
```sql
SELECT 
    filial,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE categoria_nps = 'promotor') as promotores,
    COUNT(*) FILTER (WHERE categoria_nps = 'neutro') as neutros,
    COUNT(*) FILTER (WHERE categoria_nps = 'detrator') as detratores,
    ROUND(
        (COUNT(*) FILTER (WHERE categoria_nps = 'promotor') * 100.0 / COUNT(*)) -
        (COUNT(*) FILTER (WHERE categoria_nps = 'detrator') * 100.0 / COUNT(*)), 2
    ) as nps_score
FROM nps_pesquisas 
GROUP BY filial
ORDER BY nps_score DESC;
```

### Pesquisas por Período
```sql
SELECT 
    DATE(created_at) as data,
    COUNT(*) as total_pesquisas,
    AVG(score) as nota_media
FROM nps_pesquisas 
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY data DESC;
```

## 🆘 **Solução de Problemas**

### Erro de Conexão
- Verifique se a URL e chave estão corretas
- Confirme se o projeto está ativo no Supabase

### Erro de Permissão
- Verifique se RLS está configurado corretamente
- Confirme se as políticas permitem a operação

### Erro de Inserção
- Verifique se os dados atendem às validações
- Confirme se a tabela foi criada corretamente

## 📞 **Suporte**

- [Documentação Supabase](https://supabase.com/docs)
- [Discord Supabase](https://discord.supabase.com)
- [GitHub Issues](https://github.com/supabase/supabase/issues)

