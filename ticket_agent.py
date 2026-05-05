"""
=============================================================
  AURA — Assistente Unificada de Resolução e Atendimento
  Módulo: ticket_agent.py (cérebro da AURA)
=============================================================
Dependências:
  pip install groq sentence-transformers scikit-learn numpy python-dotenv

Configuração:
  Crie um arquivo .env com:
  GROQ_API_KEY=gsk_...
=============================================================
"""

import json
import re
import uuid
import random
import string
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import numpy as np
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

# ─────────────────────────────────────────────
# CANAIS DE ATENDIMENTO
# ─────────────────────────────────────────────

CANAIS = {
    "TI / Sistemas":   "Time de TI",
    "Infraestrutura":  "Infra",
    "Financeiro":      "Financeiro",
    "RH":              "Recursos Humanos",
    "Segurança":       "Segurança da Informação",
    "Serviços Gerais": "Serviços Gerais",
}

# ─────────────────────────────────────────────
# CRITÉRIOS DE GRAVIDADE
# Para ajustar, edite apenas este bloco.
# ─────────────────────────────────────────────

CRITERIOS_GRAVIDADE = """
- alta: sistema completamente parado, dados em risco, problema persistente há mais de 2 dias,
  impacto em vários usuários ou em operação crítica do negócio
- média: impacto parcial em 1 usuário, problema recente (menos de 2 dias), existe alternativa
  temporária, perda de produtividade mas sem parada total
- baixa: dúvida, solicitação de melhoria, sem impacto imediato na operação,
  problema cosmético ou informacional
"""

# ─────────────────────────────────────────────
# MODELO DE DADOS
# ─────────────────────────────────────────────

@dataclass
class Solicitante:
    """Dados pessoais coletados antes de abrir o chamado."""
    nome: str = ""
    setor: str = ""
    gestor: str = ""
    email: str = ""


@dataclass
class Ticket:
    """Representa um chamado aberto pelo usuário."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    solicitante: Solicitante = field(default_factory=Solicitante)
    departamento: str = ""        # escolhido pelo botão
    descricao: str = ""
    criado_em: str = field(default_factory=lambda: datetime.now().isoformat())

    # Preenchidos pela AURA após análise
    gravidade: Optional[str] = None
    categoria: Optional[str] = None
    canal: Optional[str] = None
    sistema_afetado: Optional[str] = None
    erro_detectado: Optional[str] = None
    protocolo: Optional[str] = None
    resposta: Optional[str] = None
    duplicado_de: Optional[str] = None
    embedding: Optional[list] = None


# ─────────────────────────────────────────────
# AGENTE AURA
# ─────────────────────────────────────────────

class AURA:
    """
    Agente de triagem inteligente da AURA.

    Fluxo por etapas:
      1. Coleta nome do solicitante
      2. Coleta setor do solicitante
      3. Coleta nome do gestor
      4. Usuário escolhe o departamento (botões)
      5. Usuário descreve o problema
      6. AURA classifica, gera protocolo e encaminha
      7. Pergunta se deseja abrir novo chamado
    """

    def __init__(self):
        self.llm = Groq()
        print("⏳ Inicializando AURA...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ AURA pronta.\n")
        self.tickets: list[Ticket] = []

    def gerar_protocolo(self) -> str:
        """Gera protocolo único: AURA-ANO-XXXX"""
        ano = datetime.now().year
        sufixo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"AURA-{ano}-{sufixo}"

    def classificar(self, ticket: Ticket) -> dict:
        """
        Classifica gravidade e categoria usando Groq/Llama.
        Os critérios ficam em CRITERIOS_GRAVIDADE — fácil de manter.
        """
        prompt = f"""
Você é a AURA, assistente de triagem de chamados corporativos.
Analise o relato abaixo e retorne SOMENTE um JSON válido, sem texto adicional.

Solicitante: {ticket.solicitante.nome}
Setor: {ticket.solicitante.setor}
Departamento escolhido: {ticket.departamento}
Relato: "{ticket.descricao}"

Retorne exatamente neste formato:
{{
  "gravidade": "<alta|média|baixa>",
  "categoria": "<TI / Sistemas|Infraestrutura|Financeiro|RH|Segurança|Serviços Gerais>",
  "sistema_afetado": "<sistema mencionado ou null>",
  "erro_detectado": "<mensagem ou código de erro ou null>"
}}

Critérios de gravidade:
{CRITERIOS_GRAVIDADE}
"""
        resp = self.llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        texto = resp.choices[0].message.content.strip()
        texto = re.sub(r"```(?:json)?\s*|\s*```", "", texto).strip()
        dados = json.loads(texto)
        # Normaliza variações de grafia retornadas pelo modelo
        gravidade = dados.get("gravidade", "média").lower().strip()
        gravidade = gravidade.replace("mídia", "média").replace("media", "média").replace("alto", "alta").replace("baixo", "baixa")
        dados["gravidade"] = gravidade
        return dados

    def gerar_resposta(self, ticket: Ticket) -> str:
        """Gera mensagem de encerramento personalizada."""
        emoji = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}.get(ticket.gravidade, "⚪")
        prompt = f"""
Você é a AURA, assistente virtual de atendimento corporativo.
Escreva uma mensagem de confirmação para o solicitante.

Dados:
- Nome: {ticket.solicitante.nome}
- Setor: {ticket.solicitante.setor}
- Problema relatado: {ticket.descricao}
- Gravidade: {emoji} {ticket.gravidade}
- Protocolo gerado: {ticket.protocolo}

Instruções:
- Chame o solicitante pelo nome
- Confirme que entendeu o problema com suas palavras
- Informe que o chamado foi registrado com o protocolo acima
- Informe que um especialista humano entrará em contato em breve
- Para gravidade alta: transmita urgência e prioridade máxima
- NÃO mencione nomes de departamentos ou times
- Máximo 4 frases, tom humano e acolhedor
"""
        resp = self.llm.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()

    def detectar_duplicado(self, ticket: Ticket, limiar: float = 0.85) -> Optional[str]:
        """Detecta chamados similares por similaridade semântica."""
        if not self.tickets:
            return None
        emb = np.array(self.embedder.encode(ticket.descricao)).reshape(1, -1)
        for t in self.tickets:
            if t.embedding is None:
                continue
            sim = cosine_similarity(emb, np.array(t.embedding).reshape(1, -1))[0][0]
            if sim >= limiar:
                return t.protocolo
        return None

    def processar(self, ticket: Ticket) -> Ticket:
        """
        Pipeline completo de triagem.
        Recebe ticket já preenchido com solicitante, departamento e descrição.
        """
        # 1. Embedding
        ticket.embedding = self.embedder.encode(ticket.descricao).tolist()

        # 2. Duplicado
        dup = self.detectar_duplicado(ticket)
        if dup:
            ticket.duplicado_de = dup
            ticket.resposta = (
                f"⚠️ {ticket.solicitante.nome}, esse problema já foi registrado "
                f"no protocolo **{dup}**.\n\n"
                f"Você será acompanhado pela mesma tratativa. "
                f"Nenhuma ação adicional é necessária!"
            )
            return ticket

        # 3. Classificação
        dados = self.classificar(ticket)
        ticket.gravidade = dados.get("gravidade", "média")
        ticket.categoria = dados.get("categoria", ticket.departamento)
        ticket.canal = CANAIS.get(ticket.categoria, "Suporte TI")
        ticket.sistema_afetado = dados.get("sistema_afetado")
        ticket.erro_detectado = dados.get("erro_detectado")

        # 4. Protocolo
        ticket.protocolo = self.gerar_protocolo()

        # 5. Resposta
        ticket.resposta = self.gerar_resposta(ticket)

        self.tickets.append(ticket)
        return ticket
