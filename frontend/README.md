# Pesquisa NPS - Digital Sat

Aplicação web frontend para coleta de pesquisas NPS (Net Promoter Score) dos clientes da Digital Sat.

## 🚀 Funcionalidades

### ✅ Seleção de Filial
- **Via URL**: Parâmetro `filial` na URL (ex: `?filial=blumenau`)
- **Via Interface**: Dropdown com as 11 filiais quando não especificado na URL
- **Validação**: Verificação automática se a filial passada na URL é válida

### ✅ Pesquisa NPS Completa
- **Pergunta Principal**: "Em uma escala de 0 a 10, qual a probabilidade de você recomendar a Digital Sat para um amigo ou colega?"
- **Escala Visual**: Botões interativos de 0 a 10 com cores diferenciadas
- **Categorização Automática**:
  - 🔴 **Detratores**: 0-6 (vermelho)
  - 🟡 **Neutros**: 7-8 (amarelo)  
  - 🟢 **Promotores**: 9-10 (verde)
- **Feedback Visual**: Mensagens personalizadas baseadas na nota selecionada

### ✅ Informações Adicionais
- **Campos Opcionais**: Nome, email, telefone
- **Comentários**: Campo de texto livre (máximo 500 caracteres)
- **Validação**: Email com formato válido

### ✅ Página de Agradecimento
- **Confirmação**: Mensagem de agradecimento personalizada
- **Contato**: Informações completas da Digital Sat
- **Nova Pesquisa**: Botão para iniciar nova avaliação

## 🎨 Design e UX

### Identidade Visual
- **Cores**: Baseadas na identidade da Digital Sat (vermelho #E53E3E)
- **Tipografia**: Inter (moderna e legível)
- **Layout**: Clean, profissional e intuitivo

### Responsividade
- **Mobile First**: Otimizado para dispositivos móveis
- **Breakpoints**: Mobile, tablet e desktop
- **Touch Friendly**: Botões e elementos adequados para toque

### Acessibilidade
- **Contraste**: Cores com contraste adequado
- **Navegação**: Suporte completo para teclado
- **Screen Readers**: Labels e textos alternativos apropriados

## 🏢 Filiais Suportadas

1. Balneário Camboriú (`balneario-camboriu`)
2. Blumenau (`blumenau`)
3. Brusque (`brusque`)
4. Centro de Distribuição (`centro-distribuicao`)
5. Gravataí - RS (`gravatai`)
6. Itajaí (`itajai`)
7. Itapema (`itapema`)
8. Joinville (`joinville`)
9. Lages (`lages`)
10. Rio do Sul (`rio-do-sul`)
11. São José (`sao-jose`)
12. Tubarão (`tubarao`)

## 🔗 Exemplos de URL

```
# Seleção manual de filial
https://seu-dominio.com/

# Filial pré-selecionada via URL
https://seu-dominio.com/?filial=blumenau
https://seu-dominio.com/?filial=joinville
https://seu-dominio.com/?filial=sao-jose
```

## 🛠️ Tecnologias Utilizadas

- **React 18**: Framework principal
- **Tailwind CSS**: Estilização e responsividade
- **Lucide Icons**: Ícones modernos
- **Vite**: Build tool e dev server
- **shadcn/ui**: Componentes UI de alta qualidade

## 📱 Fluxo do Usuário

### Cenário 1: Sem filial na URL
1. Usuário acessa a aplicação
2. Seleciona filial no dropdown
3. Clica em "Continuar"
4. Preenche pesquisa NPS
5. Envia avaliação
6. Visualiza página de agradecimento

### Cenário 2: Com filial na URL
1. Usuário acessa URL com parâmetro de filial
2. Aplicação carrega diretamente o formulário NPS
3. Preenche pesquisa NPS
4. Envia avaliação
5. Visualiza página de agradecimento

## 🚀 Como Executar

```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## 📊 Dados Coletados

A aplicação coleta os seguintes dados:

```javascript
{
  score: number,        // Nota NPS (0-10)
  filial: string,       // ID da filial
  nome: string,         // Nome (opcional)
  email: string,        // Email (opcional)
  telefone: string,     // Telefone (opcional)
  comentario: string,   // Comentário (opcional)
  timestamp: string     // Data/hora do envio
}
```

## 🔧 Próximos Passos (Backend)

Para integração com backend, será necessário:

1. **API Endpoint**: Criar endpoint para receber dados da pesquisa
2. **Banco de Dados**: Estrutura para armazenar respostas
3. **Dashboard**: Interface para visualizar resultados
4. **Relatórios**: Análise de NPS por filial e período
5. **Notificações**: Alertas para scores baixos

## 📞 Contato Digital Sat

- **Telefones**: (47) 3263-5556 / (47) 3263-5555
- **Email**: contato@digitalsat.com.br
- **Site**: https://digitalsat.com.br
- **Horário**: Segunda à sexta, das 7h45 às 12h e das 13h30 às 18h

---

*Desenvolvido para a Digital Sat - Distribuidora de Produtos de Segurança Eletrônica e Conectividade*

