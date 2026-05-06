# AURA — Assistente Unificada de Resolução e Atendimento

AURA é um chatbot de triagem inteligente de chamados corporativos. O sistema recebe demandas em linguagem natural, coleta dados do solicitante, classifica a gravidade, gera um número de protocolo e encaminha automaticamente para o departamento correto — sem intervenção humana na triagem.

O projeto nasceu de uma experiência real: trabalhar em um ambiente onde chamados chegavam sem categorização, sem prioridade e sem um dono claro. A AURA foi construída para resolver exatamente esse problema.

---

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal do backend |
| FastAPI | API REST que conecta frontend e backend |
| HTML / CSS / JS | Interface de chat (frontend puro) |
| Groq (Llama 3.3 70B) | Classificação de gravidade e geração de respostas |
| Sentence Transformers | Embeddings semânticos para detecção de duplicados |
| Scikit-learn | Similaridade de cosseno entre tickets |
| python-dotenv | Gerenciamento seguro da chave de API |

---

## Fluxo do sistema

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO ABRE O CHAT                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│         AURA envia mensagem de boas-vindas              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              COLETA DE DADOS DO SOLICITANTE             │
│                                                         │
│   1. Nome completo                                      │
│   2. Setor na empresa                                   │
│   3. Gestor imediato                                    │
│   4. E-mail (ou botão "Não tenho e-mail")               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           SELECAO DE DEPARTAMENTO (botoes)              │
│                                                         │
│  [ TI/Sistemas ]  [ Infraestrutura ]  [ Financeiro ]   │
│  [ RH ]           [ Seguranca ]       [ Serv. Gerais ] │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              USUARIO DESCREVE O PROBLEMA                │
│              (linguagem natural livre)                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           PIPELINE DE TRIAGEM AUTOMATICA                │
│                                                         │
│  [1] Embedding semantico (sentence-transformers)        │
│       ↓                                                 │
│  [2] Deteccao de duplicados (cosine similarity >= 85%)  │
│       ↓ nao duplicado                                   │
│  [3] Classificacao via Groq/Llama:                      │
│       - Gravidade: Alta | Media | Baixa                 │
│       - Categoria e canal de encaminhamento             │
│       - Sistema afetado e erro detectado                │
│       ↓                                                 │
│  [4] Geracao de protocolo: AURA-{ANO}-{XXXX}           │
│       ↓                                                 │
│  [5] Geracao de resposta personalizada                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              RESULTADO EXIBIDO NO CHAT                  │
│                                                         │
│  - Resposta personalizada da AURA                       │
│  - Resumo: protocolo, gravidade, departamento           │
│  - Dados do solicitante: nome, setor, gestor, e-mail    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│      [ Abrir novo chamado ] [ Encerrar atendimento ]    │
└─────────────────────────────────────────────────────────┘
```

### Criterios de gravidade

| Gravidade | Criterio |
|---|---|
| Alta | Sistema parado, dados em risco, problema persistente ha mais de 2 dias, impacto em varios usuarios |
| Media | Impacto parcial, problema recente (menos de 2 dias), existe alternativa temporaria |
| Baixa | Duvida, solicitacao de melhoria, sem impacto imediato na operacao |

---

## Estrutura do projeto

```
chatbot-ticket-agent/
├── backend/
│   ├── main.py          # API FastAPI — conecta frontend ao cerebro da AURA
│   ├── ticket_agent.py  # Cerebro da AURA (logica, IA, classificacao)
│   └── requirements.txt # Dependencias do backend
├── frontend/
│   └── index.html       # Interface de chat (HTML/CSS/JS puro)
├── .env                 # Chave da API Groq (nao versionado)
├── .gitignore           # Protege .env e arquivos temporarios
└── README.md            # Documentacao
```

---

## Como executar localmente

1. Clone o repositorio:

```bash
git clone https://github.com/ClintSant/chatbot-ticket-agent.git
cd chatbot-ticket-agent
```

2. Instale as dependencias:

```bash
pip install fastapi uvicorn groq sentence-transformers scikit-learn numpy python-dotenv
```

3. Configure a chave do Groq. Crie um arquivo .env dentro da pasta backend/:

```
GROQ_API_KEY=gsk_sua_chave_aqui
```

Obtenha sua chave gratuita em: https://console.groq.com/keys

4. Rode o backend:

```bash
cd backend
python -m uvicorn main:app --reload
```

5. Abra o frontend: abra o arquivo frontend/index.html diretamente no navegador.

---

## Decisoes tecnicas

**Por que Groq?**
A API do Groq oferece acesso gratuito ao Llama 3.3 70B com altissima velocidade de inferencia — ideal para um chatbot de atendimento em tempo real.

**Por que Sentence Transformers para deteccao de duplicados?**
Em vez de usar o LLM para comparar tickets (caro e lento), usamos embeddings semanticos locais e similaridade de cosseno. Isso torna a deteccao de duplicados rapida e sem custo de API.

**Por que FastAPI + HTML puro em vez de Streamlit?**
Separar o frontend do backend permite maior controle visual e de UX. O frontend em HTML/CSS/JS puro replica fielmente o design planejado, com temas escuro/claro, animacoes e botoes customizados — algo dificil de alcançar com Streamlit.

**Por que os criterios de gravidade ficam no prompt?**
Manter os criterios como texto no prompt facilita a manutencao — se a empresa quiser ajustar o que e "alta" ou "media", basta editar uma constante no codigo, sem retreinar nenhum modelo.

---

## Autor

Desenvolvido por Clinton Sant — [LinkedIn](https://linkedin.com/in/clintonsant) | [GitHub](https://github.com/ClintSant)
