# 🤖 AURA — Assistente Unificada de Resolução e Atendimento

AURA é um chatbot de triagem inteligente de tickets corporativos, desenvolvido com Python, Streamlit e Groq (Llama 3.3 70B).

O sistema recebe demandas em linguagem natural, coleta dados do solicitante, classifica a gravidade, gera um número de protocolo e encaminha automaticamente para o departamento correto — sem intervenção humana na triagem.

---

## 🚀 Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| Streamlit | Interface de chat |
| Groq (Llama 3.3 70B) | Classificação e geração de respostas |
| Sentence Transformers | Embeddings semânticos para detecção de duplicados |
| Scikit-learn | Similaridade de cosseno |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## 🔄 Fluxo do sistema

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO ABRE O CHAT                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│         AURA envia mensagem de boas-vindas              │
│              session_state inicializado                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              COLETA DE DADOS DO SOLICITANTE             │
│                                                         │
│   1. Nome         → "Qual é o seu nome?"                │
│   2. Setor        → "Qual é o seu setor?"               │
│   3. Gestor       → "Qual é o seu gestor imediato?"     │
│   4. E-mail       → "Qual é o seu e-mail?"              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           SELEÇÃO DE DEPARTAMENTO (botões)              │
│                                                         │
│  [ TI/Sistemas ]  [ Infraestrutura ]  [ Financeiro ]   │
│  [ RH ]           [ Segurança ]       [ Serv. Gerais ] │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              USUÁRIO DESCREVE O PROBLEMA                │
│              (linguagem natural livre)                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           PIPELINE DE TRIAGEM AUTOMÁTICA                │
│                                                         │
│  [1] Embedding semântico (sentence-transformers)        │
│       ↓                                                 │
│  [2] Detecção de duplicados (cosine similarity ≥ 85%)   │
│       ↓ não duplicado                                   │
│  [3] Classificação via Groq/Llama:                      │
│       • Gravidade: 🔴 Alta | 🟡 Média | 🟢 Baixa        │
│       • Categoria e canal de encaminhamento             │
│       • Sistema afetado e erro detectado                │
│       ↓                                                 │
│  [4] Geração de protocolo: AURA-{ANO}-{XXXX}           │
│       ↓                                                 │
│  [5] Geração de resposta personalizada                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              RESULTADO EXIBIDO NO CHAT                  │
│                                                         │
│  • Resposta personalizada da AURA                       │
│  • Resumo: protocolo, gravidade, departamento           │
│  • Solicitante, gestor, e-mail                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              [ Abrir novo chamado ]                     │
│              [ Encerrar atendimento ]                   │
└─────────────────────────────────────────────────────────┘
```

### Critérios de gravidade

| Gravidade | Critério |
|---|---|
| 🔴 **Alta** | Sistema parado, dados em risco, problema persistente há mais de 2 dias, impacto em vários usuários |
| 🟡 **Média** | Impacto parcial, problema recente (menos de 2 dias), existe alternativa temporária |
| 🟢 **Baixa** | Dúvida, solicitação de melhoria, sem impacto imediato na operação |

---

## 📁 Estrutura do projeto

```
chatbot ticket-agent/
├── app.py            # Interface de chat (Streamlit)
├── ticket_agent.py   # Cérebro da AURA (lógica, IA, classificação)
├── .env              # Chave da API Groq (não versionado)
├── .gitignore        # Protege .env e arquivos temporários
└── README.md         # Documentação
```

---

## ⚙️ Como executar localmente

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/chatbot-ticket-agent.git
cd chatbot-ticket-agent
```

**2. Instale as dependências:**
```bash
pip install groq streamlit sentence-transformers scikit-learn numpy python-dotenv
```

**3. Configure a chave do Groq:**

Crie um arquivo `.env` na pasta do projeto:
```
GROQ_API_KEY=gsk_sua_chave_aqui
```

Obtenha sua chave gratuita em: https://console.groq.com/keys

**4. Execute:**
```bash
python -m streamlit run app.py
```

---

## 🧠 Decisões técnicas

**Por que Groq?**
A API do Groq oferece acesso gratuito ao Llama 3.3 70B com altíssima velocidade de inferência — ideal para um chatbot de atendimento em tempo real.

**Por que Sentence Transformers para detecção de duplicados?**
Em vez de usar o LLM para comparar tickets (caro e lento), usamos embeddings semânticos locais e similaridade de cosseno. Isso torna a detecção de duplicados rápida e sem custo de API.

**Por que Streamlit?**
Permite criar interfaces de chat interativas com poucos componentes nativos (`st.chat_message`, `st.chat_input`, `st.session_state`), sem necessidade de frontend separado.

---

## 👤 Autor

Desenvolvido por **Clinton Sant** — [LinkedIn](https://linkedin.com/in/clintonsant) | [GitHub](https://github.com/ClintSant)
