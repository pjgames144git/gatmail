import streamlit as json_style  # Apenas apelido lúdico
import streamlit as st
import datetime
import random

# Configuração da Página para simular o estilo de uma janela antiga
st.set_page_config(
    page_title="Gatmail - Web Mail Classic",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS personalizada para dar o visual Windows 98 / Anos 2000
st.markdown("""
    <style>
    .stApp {
        background-color: #008080; /* Clássico verde teal do Windows 95/98 */
        font-family: "MS Sans Serif", Arial, sans-serif;
    }
    .retro-window {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 10px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .retro-titlebar {
        background: linear-gradient(90deg, #000080, #1084d0);
        color: white;
        padding: 4px 8px;
        font-weight: bold;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -10px -10px 10px -10px;
    }
    .retro-button {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        padding: 4px 12px;
        font-weight: bold;
        cursor: pointer;
    }
    .email-box {
        background-color: white;
        border: 2px inset #808080;
        padding: 10px;
        min-height: 250px;
    }
    h1, h2, h3, p, label {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar o "Banco de Dados" na sessão do Streamlit
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "inbox" not in st.session_state:
    # E-mails iniciais estilo retro para dar vida ao app
    st.session_state.inbox = [
        {
            "id": 1,
            "sender": "admin@gatmail.com",
            "subject": "Bem-vindo ao Gatmail!",
            "date": "19/06/2001 14:32",
            "body": "Olá!\n\nSeja muito bem-vindo ao Gatmail, o seu serviço de correio eletrônico retrô para clientes legados e web.\nAproveite a navegação nostálgica!\n\nAtenciosamente,\nEquipe Gatmail."
        },
        {
            "id": 2,
            "sender": "suporte@gatmail.com",
            "subject": "Dicas para o Windows 98",
            "date": "20/06/2001 09:15",
            "body": "Lembre-se de configurar suas portas corretamente se for tentar usar o Outlook Express.\nDivirta-se revivendo a internet dos anos 2000!"
        }
    ]

# -------------------------------------------------------------------------
# TELA DE LOGIN (Estilo Tela de Entrada do MSN / Webmail Antigo)
# -------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="retro-window">
                <div class="retro-titlebar">
                    <span>Gatmail Login - Internet Explorer</span>
                    <span>[_][O][X]</span>
                </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; margin-top: 5px;'>Gatmail ✉️</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 12px;'>O seu portal de e-mail retrô</p>", unsafe_allow_html=True)
        
        user_input = st.text_input("Nome da conta:", placeholder="seu-usuario")
        pass_input = st.text_input("Senha:", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Entrar na Caixa de Entrada", use_container_width=True):
            if user_input.strip() != "":
                st.session_state.logged_in = True
                # Limpa o domínio se o usuário digitou completo
                clean_user = user_input.split("@")[0]
                st.session_state.username = clean_user
                st.rerun()
            else:
                st.warning("Por favor, digite um nome de usuário válido.")
                
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# CAIXA DE ENTRADA / WEBMAIL (Estilo Outlook Express / Escargot)
# -------------------------------------------------------------------------
else:
    full_email = f"{st.session_state.username}@gatmail.com"
    
    # Barra de Navegação Superior Estilo Menu de Aplicativo Antigo
    st.markdown(f"""
        <div class="retro-window" style="margin-bottom: 10px; padding: 5px;">
            <b>Conectado como:</b> <span style="color: #000080; font-weight: bold;">{full_email}</span> 
            | <a href="#" target="_self" onclick="location.reload();">Sair</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Abas de navegação do webmail
    aba_atual = st.radio("Ações", ["📥 Caixa de Entrada", "✉️ Escrever Mensagem"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("---")
    
    if aba_atual == "📥 Caixa de Entrada":
        st.markdown("### Suas Mensagens")
        
        if not st.session_state.inbox:
            st.info("Sua caixa de entrada está vazia.")
        else:
            # Tabela estilo lista de mensagens antiga
            for msg in reversed(st.session_state.inbox):
                with st.expander(f"De: {msg['sender']} — Assunto: {msg['subject']} ({msg['date']})"):
                    st.text_area("Mensagem:", value=msg['body'], height=150, disabled=True, key=f"msg_body_{msg['id']}")
                    
                    col_del, _ = st.columns([1, 4])
                    with col_del:
                        if st.button("Excluir", key=f"del_{msg['id']}"):
                            st.session_state.inbox = [m for m in st.session_state.inbox if m['id'] != msg['id']]
                            st.rerun()

    elif aba_atual == "✉️ Escrever Mensagem":
        st.markdown("### Nova Mensagem de Correio")
        
        destinatario = st.text_input("Para:", placeholder="amigo@gatmail.com")
        assunto = st.text_input("Assunto:")
        corpo = st.text_area("Mensagem:", height=200)
        
        col_send, col_back = st.columns([1, 4])
        with col_send:
            if st.button("Enviar E-mail"):
                if destinatario and assunto:
                    nova_msg = {
                        "id": random.randint(1000, 9999),
                        "sender": full_email,
                        "subject": assunto,
                        "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "body": corpo
                    }
                    st.session_state.inbox.append(nova_msg)
                    st.success("Mensagem enviada com sucesso para o servidor Gatmail!")
                else:
                    st.error("Preencha pelo menos o destinatário e o assunto.")
