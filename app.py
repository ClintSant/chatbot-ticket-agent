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
st.title("🤖 AURA")
st.caption("Assistente Unificada de Resolução e Atendimento")

# ─────────────────────────────────────────────────────────
# SCROLL AUTOMÁTICO PARA O FINAL DO CHAT
# ─────────────────────────────────────────────────────────
st.components.v1.html("""
<script>
    function scrollToBottom() {
        window.parent.scrollTo({ top: window.parent.document.body.scrollHeight, behavior: 'smooth' });
    }
    setTimeout(scrollToBottom, 300);
</script>
""", height=0)

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
        "TI / Sistemas", "Infraestrutura", "Financeiro",
        "RH", "Segurança", "Serviços Gerais"
    ]
    cols = st.columns(3)
    for i, dep in enumerate(departamentos):
        if cols[i % 3].button(dep, use_container_width=True, key=f"dep_{dep}"):
            st.session_state.departamento = dep
            st.session_state.etapa = "aguardando_descricao"
            st.session_state.mensagens.append({
                "role": "assistant",
                "content": (
                    f"Entendido! Você selecionou **{dep}**. 👍\n\n"
                    f"Agora descreva sua demanda com o máximo de detalhes — "
                    f"pode mencionar o sistema afetado, o que está acontecendo e há quanto tempo."
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

        # ── Validação de campos obrigatórios ─────────────
        campos_obrigatorios = ["aguardando_nome", "aguardando_setor", "aguardando_gestor"]
        if st.session_state.etapa in campos_obrigatorios and not texto:
            st.warning("⚠️ Este campo é obrigatório. Por favor, preencha antes de continuar.")
            st.stop()

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

# ─────────────────────────────────────────────────────────
# BOTÃO "NÃO TENHO E-MAIL" — aparece apenas na etapa de email
# ─────────────────────────────────────────────────────────
if st.session_state.etapa == "aguardando_email":
    if st.button("📧 Não tenho e-mail / Não sei informar agora", use_container_width=True, key="sem_email"):
        email_ficticio = "suporte@aura.com.br"
        st.session_state.solicitante.email = email_ficticio
        st.session_state.etapa = "aguardando_departamento"
        nome = st.session_state.solicitante.nome
        resposta = (
            f"Sem problemas, **{nome}**! 😊\n\n"
            f"Para este chamado utilizaremos o e-mail de contato da equipe: "
            f"**{email_ficticio}**\n\n"
            f"Agora selecione o **departamento** para o qual deseja encaminhar seu chamado:"
        )
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        st.rerun()
