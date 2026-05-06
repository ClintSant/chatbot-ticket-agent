"""
=============================================================
  AURA — Assistente Unificada de Resolução e Atendimento
  Módulo: main.py (API FastAPI)
=============================================================
  Execute com: uvicorn main:app --reload
=============================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ticket_agent import AURA, Ticket, Solicitante

# ─────────────────────────────────────────────────────────
# INICIALIZAÇÃO
# ─────────────────────────────────────────────────────────
app = FastAPI(title="AURA API", version="1.0.0")

# CORS — permite que o frontend (GitHub Pages) chame a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, substitua pelo domínio do frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia a AURA uma única vez
aura = AURA()

# ─────────────────────────────────────────────────────────
# MODELOS DE ENTRADA
# ─────────────────────────────────────────────────────────

class DadosSolicitante(BaseModel):
    nome: str
    setor: str
    gestor: str
    email: str

class ChamadoRequest(BaseModel):
    solicitante: DadosSolicitante
    departamento: str
    descricao: str

# ─────────────────────────────────────────────────────────
# ROTAS
# ─────────────────────────────────────────────────────────

@app.get("/")
def raiz():
    """Health check — verifica se a API está no ar."""
    return {"status": "online", "servico": "AURA API"}


@app.post("/chamado")
def criar_chamado(dados: ChamadoRequest):
    """
    Recebe os dados do chamado do frontend,
    processa com a AURA e retorna o resultado.
    """
    solicitante = Solicitante(
        nome=dados.solicitante.nome,
        setor=dados.solicitante.setor,
        gestor=dados.solicitante.gestor,
        email=dados.solicitante.email,
    )

    ticket = Ticket(
        solicitante=solicitante,
        departamento=dados.departamento,
        descricao=dados.descricao,
    )

    resultado = aura.processar(ticket)

    # Monta resposta JSON para o frontend
    return {
        "protocolo": resultado.protocolo,
        "duplicado_de": resultado.duplicado_de,
        "gravidade": resultado.gravidade,
        "categoria": resultado.categoria,
        "canal": resultado.canal,
        "sistema_afetado": resultado.sistema_afetado,
        "erro_detectado": resultado.erro_detectado,
        "resposta": resultado.resposta,
    }