"""
=============================================================
  AURA — Assistente Unificada de Resolução e Atendimento
  Módulo: app.py (interface de chat)
=============================================================
  Execute com: python -m streamlit run app.py
=============================================================
"""

import streamlit as st
from ticket_agent import AURA, Ticket, Solicitante

st.set_page_config(page_title="AURA", page_icon="🤖", layout="centered")

# ─────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────

def msg_boas_vindas():
    return {
        "role": "assistant",
        "content": (
            "Olá! 👋 Eu sou a **AURA**, sua Assistente Unificada de Resolução e Atendimento.\n\n"
            "Estou aqui para registrar e encaminhar seu chamado da forma mais rápida possível.\n\n"
            "Para começar, qual é o seu **nome completo**?"
        )
    }

if "aura" not in st.session_state:
    st.session_state.aura = AURA()
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [msg_boas_vindas()]
if "etapa" not in st.session_state:
    st.session_state.etapa = "aguardando_nome"
if "solicitante" not in st.session_state:
    st.session_state.solicitante = Solicitante()
if "departamento" not in st.session_state:
    st.session_state.departamento = None
if "tema" not in st.session_state:
    st.session_state.tema = "escuro"

# ─────────────────────────────────────────────────────────
# VARIÁVEIS DE TEMA
# ─────────────────────────────────────────────────────────
if st.session_state.tema == "escuro":
    bg_primary     = "#1A1D21"
    bg_secondary   = "#2a2d31"
    bg_input       = "#2a2d31"
    text_primary   = "#f0f0f0"
    text_secondary = "#aaaaaa"
    accent_1       = "#6F42C1"
    accent_2       = "#17A2B8"
    border_color   = "#3a3d41"
    bubble_bot_bg  = "#2a2d31"
    bubble_bot_txt = "#e9ecef"
    bubble_usr_bg  = "linear-gradient(135deg, #6F42C1, #5a32a3)"
    btn_bg         = "#2a2d31"
    btn_hover      = "#6F42C1"
    page_bg        = "#0d0d0d"
else:
    bg_primary     = "#ffffff"
    bg_secondary   = "#f8f9fa"
    bg_input       = "#f8f9fa"
    text_primary   = "#212529"
    text_secondary = "#6c757d"
    accent_1       = "#007BFF"
    accent_2       = "#28A745"
    border_color   = "#dee2e6"
    bubble_bot_bg  = "#e9ecef"
    bubble_bot_txt = "#212529"
    bubble_usr_bg  = "linear-gradient(135deg, #007BFF, #0056b3)"
    btn_bg         = "#e9ecef"
    btn_hover      = "#007BFF"
    page_bg        = "#f0f2f5"

# ─────────────────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}

/* Página */
.stApp {{
    background-color: {page_bg} !important;
}}

/* Container principal */
section.main > div {{
    max-width: 720px;
    margin: 0 auto;
    padding-top: 1rem;
}}

/* Título */
h1 {{
    color: {text_primary} !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}}

/* Caption */
.stApp p.st-emotion-cache-16idsys, div[data-testid="stCaptionContainer"] p {{
    color: {text_secondary} !important;
    font-size: 13px !important;
}}

/* Mensagens do chat */
[data-testid="stChatMessage"] {{
    background-color: transparent !important;
    padding: 4px 0 !important;
}}

/* Balão do assistente */
[data-testid="stChatMessage"][data-testid*="assistant"] .stMarkdown,
div[data-testid="stChatMessageContent"] {{
    background-color: {bubble_bot_bg} !important;
    color: {bubble_bot_txt} !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 12px 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}}

/* Chat input */
[data-testid="stChatInput"] {{
    background-color: {bg_input} !important;
    border: 1.5px solid {border_color} !important;
    border-radius: 14px !important;
    color: {text_primary} !important;
}}

[data-testid="stChatInput"]:focus-within {{
    border-color: {accent_1} !important;
    box-shadow: 0 0 0 3px {accent_1}22 !important;
}}

/* Botões */
.stButton > button {{
    background: {btn_bg} !important;
    color: {text_primary} !important;
    border: 1.5px solid {border_color} !important;
    border-radius: 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover {{
    background: {accent_1} !important;
    color: #ffffff !important;
    border-color: {accent_1} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px {accent_1}44 !important;
}}

/* Divider */
hr {{
    border-color: {border_color} !important;
    opacity: 0.4 !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {accent_1}66; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# HEADER COM TOGGLE DE TEMA
# ─────────────────────────────────────────────────────────
col_title, col_toggle = st.columns([5, 1])
with col_title:
    st.title("🤖 AURA")
    st.caption("Assistente Unificada de Resolução e Atendimento")
with col_toggle:
    st.write("")
    tema_label = "☀️ Claro" if st.session_state.tema == "escuro" else "🌙 Escuro"
    if st.button(tema_label, key="toggle_tema"):
        st.session_state.tema = "claro" if st.session_state.tema == "escuro" else "escuro"
        st.rerun()

st.divider()

# ─────────────────────────────────────────────────────────
# SCROLL AUTOMÁTICO
# ─────────────────────────────────────────────────────────
st.components.v1.html("""
<script>
    setTimeout(() => {
        window.parent.scrollTo({ top: window.parent.document.body.scrollHeight, behavior: 'smooth' });
    }, 300);
</script>
""", height=0)

# ─────────────────────────────────────────────────────────
# EXIBE HISTÓRICO
# ─────────────────────────────────────────────────────────
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────
# BOTÕES DE DEPARTAMENTO
# ─────────────────────────────────────────────────────────
if st.session_state.etapa == "aguardando_departamento":
    departamentos = [
        "💻 TI / Sistemas", "🔧 Infraestrutura", "💰 Financeiro",
        "👥 RH", "🔐 Segurança", "🏢 Serviços Gerais"
    ]
    cols = st.columns(3)
    for i, dep in enumerate(departamentos):
        if cols[i % 3].button(dep, use_container_width=True, key=f"dep_{dep}"):
            dep_limpo = dep.split(" ", 1)[1]  # remove emoji
            st.session_state.departamento = dep_limpo
            st.session_state.etapa = "aguardando_descricao"
            st.session_state.mensagens.append({
                "role": "assistant",
                "content": (
                    f"Entendido! Você selecionou **{dep_limpo}**. 👍\n\n"
                    f"Agora descreva sua demanda com o máximo de detalhes — "
                    f"pode mencionar o sistema afetado, o que está acontecendo e há quanto tempo."
                )
            })
            st.rerun()

# ─────────────────────────────────────────────────────────
# BOTÃO "NÃO TENHO E-MAIL"
# ─────────────────────────────────────────────────────────
if st.session_state.etapa == "aguardando_email":
    if st.button("📧 Não tenho e-mail / Não sei informar agora", use_container_width=True, key="sem_email"):
        email_ficticio = "suporte@aura.com.br"
        st.session_state.solicitante.email = email_ficticio
        st.session_state.etapa = "aguardando_departamento"
        nome = st.session_state.solicitante.nome
        st.session_state.mensagens.append({
            "role": "assistant",
            "content": (
                f"Sem problemas, **{nome}**! 😊\n\n"
                f"Para este chamado utilizaremos o e-mail da equipe: **{email_ficticio}**\n\n"
                f"Agora selecione o **departamento** para o qual deseja encaminhar seu chamado:"
            )
        })
        st.rerun()

# ─────────────────────────────────────────────────────────
# BOTÕES PÓS-ATENDIMENTO
# ─────────────────────────────────────────────────────────
if st.session_state.etapa == "concluido":
    col1, col2 = st.columns(2)
    if col1.button("🔄 Abrir novo chamado", use_container_width=True, key="novo"):
        st.session_state.etapa = "aguardando_nome"
        st.session_state.solicitante = Solicitante()
        st.session_state.departamento = None
        st.session_state.mensagens.append({
            "role": "assistant",
            "content": "Certo! Vamos abrir um novo chamado. 😊\n\nQual é o seu **nome completo**?"
        })
        st.rerun()
    if col2.button("✅ Encerrar atendimento", use_container_width=True, key="encerrar"):
        st.session_state.mensagens.append({
            "role": "assistant",
            "content": (
                f"Obrigada pelo contato, **{st.session_state.solicitante.nome}**! 😊\n\n"
                f"Seu chamado está registrado e nossa equipe entrará em contato "
                f"no e-mail **{st.session_state.solicitante.email}** em breve.\n\n"
                f"Tenha um ótimo dia!"
            )
        })
        st.session_state.etapa = "encerrado"
        st.rerun()

# ─────────────────────────────────────────────────────────
# BOTÃO REINICIAR
# ─────────────────────────────────────────────────────────
if st.session_state.etapa == "encerrado":
    if st.button("🔁 Iniciar novo atendimento", use_container_width=True, key="reiniciar"):
        st.session_state.mensagens = [msg_boas_vindas()]
        st.session_state.etapa = "aguardando_nome"
        st.session_state.solicitante = Solicitante()
        st.session_state.departamento = None
        st.rerun()

# ─────────────────────────────────────────────────────────
# INPUT DO USUÁRIO
# ─────────────────────────────────────────────────────────
etapas_com_input = [
    "aguardando_nome", "aguardando_setor",
    "aguardando_gestor", "aguardando_email",
    "aguardando_descricao"
]

if st.session_state.etapa in etapas_com_input:
    entrada = st.chat_input("Digite sua mensagem...")

    if entrada:
        texto = entrada.strip()
        resposta = ""

        st.session_state.mensagens.append({"role": "user", "content": texto})
        with st.chat_message("user"):
            st.markdown(texto)

        # ── Etapa 1: nome ─────────────────────────────────
        if st.session_state.etapa == "aguardando_nome":
            if len(texto) < 2:
                resposta = "Por favor, informe seu **nome completo** para continuarmos. 😊"
            else:
                nome = texto.split()[0].capitalize()
                st.session_state.solicitante.nome = nome
                st.session_state.etapa = "aguardando_setor"
                resposta = f"Prazer, **{nome}**! 😊 Qual é o seu **setor** na empresa?"

        # ── Etapa 2: setor ────────────────────────────────
        elif st.session_state.etapa == "aguardando_setor":
            if len(texto) < 2:
                resposta = "Por favor, informe o **setor** onde você trabalha para continuarmos."
            else:
                st.session_state.solicitante.setor = texto
                st.session_state.etapa = "aguardando_gestor"
                nome = st.session_state.solicitante.nome
                resposta = f"Anotado! Qual é o nome do seu **gestor imediato**, {nome}?"

        # ── Etapa 3: gestor ───────────────────────────────
        elif st.session_state.etapa == "aguardando_gestor":
            if len(texto) < 2:
                resposta = "Por favor, informe o nome do seu **gestor imediato** para continuarmos."
            else:
                st.session_state.solicitante.gestor = texto
                st.session_state.etapa = "aguardando_email"
                resposta = "Perfeito! Qual é o seu **e-mail** para contato?"

        # ── Etapa 4: email ────────────────────────────────
        elif st.session_state.etapa == "aguardando_email":
            st.session_state.solicitante.email = texto
            st.session_state.etapa = "aguardando_departamento"
            nome = st.session_state.solicitante.nome
            resposta = (
                f"Ótimo, **{nome}**! Agora selecione o **departamento** "
                f"para o qual deseja encaminhar seu chamado:"
            )

        # ── Etapa 5: descrição + processamento ───────────
        elif st.session_state.etapa == "aguardando_descricao":
            if len(texto) < 10:
                resposta = "Por favor, descreva o problema com mais detalhes para que possamos ajudá-lo melhor. 😊"
            else:
                with st.chat_message("assistant"):
                    with st.spinner("Analisando seu chamado..."):
                        ticket = Ticket(
                            solicitante=st.session_state.solicitante,
                            departamento=st.session_state.departamento,
                            descricao=texto,
                        )
                        resultado = st.session_state.aura.processar(ticket)

                    if resultado.duplicado_de:
                        resposta_final = resultado.resposta
                    else:
                        emoji = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}.get(resultado.gravidade, "⚪")
                        resposta_final = (
                            f"{resultado.resposta}\n\n"
                            f"---\n"
                            f"📋 **Resumo do chamado**\n"
                            f"- **Protocolo:** `{resultado.protocolo}`\n"
                            f"- **Solicitante:** {resultado.solicitante.nome} — {resultado.solicitante.setor}\n"
                            f"- **Gestor:** {resultado.solicitante.gestor}\n"
                            f"- **E-mail:** {resultado.solicitante.email}\n"
                            f"- **Gravidade:** {emoji} {resultado.gravidade}\n"
                            f"- **Departamento:** {resultado.departamento}\n"
                            f"- **Encaminhado para:** {resultado.canal}\n"
                            f"- **Sistema:** {resultado.sistema_afetado or '—'}\n"
                            f"- **Erro:** {resultado.erro_detectado or '—'}"
                        )

                    st.markdown(resposta_final)
                    st.session_state.mensagens.append({"role": "assistant", "content": resposta_final})

                followup = "Posso te ajudar com mais alguma coisa?"
                st.session_state.mensagens.append({"role": "assistant", "content": followup})
                with st.chat_message("assistant"):
                    st.markdown(followup)

                st.session_state.etapa = "concluido"
                st.rerun()

        if resposta:
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
            with st.chat_message("assistant"):
                st.markdown(resposta)
            if st.session_state.etapa == "aguardando_departamento":
                st.rerun()
