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
