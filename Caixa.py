import streamlit as st

# Configuração inicial da página com ícone e título da Guiné-Bissau
st.set_page_config(
    page_title="SNS Digital - Guiné-Bissau 🇬🇼 - Diolindo Mendes",
    page_icon="🇬🇼",
    layout="wide"
)

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Guinea-Bissau.svg",
    width=150
)
st.sidebar.title("🇬🇼 SNS Digital")

menu = st.sidebar.radio(
    "Navegação",
    ["🩺 Triagem de Pacientes (Público)", "👨‍⚕️ Ponto Médico (Público)", "🔒 Painel do Administrador (Privado)"]
)

# --- 1. TRIAGEM DE PACIENTES ---
if menu == "🩺 Triagem de Pacientes (Público)":
    st.title("🩺 Portal de Triagem Hospitalar 🇬🇼")
    st.write("Preencha os dados do paciente para encaminhamento automático.")

    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo do Paciente")
        sintomas = st.text_area("Sintomas Apresentados")
    with col2:
        especialidade = st.selectbox(
            "Especialidade Médica",
            ["Cardiologia", "Pediatria", "Ortopedia", "Clínica Geral", "Urgência Geral"]
        )
        urgencia = st.select_slider(
            "Nível de Urgência (Manchester)",
            options=["🟢 Verde (Pouco Urgente)", "🟡 Amarelo (Urgente)", "🔴 Vermelho (Emergência)"]
        )

    if st.button("Submeter Triagem"):
        if nome and sintomas:
            st.success(f"Triagem registada com sucesso para **{nome}**!")
        else:
            st.warning("Por favor, preencha o nome e os sintomas do paciente.")

# --- 2. PONTO MÉDICO ---
elif menu == "👨‍⚕️ Ponto Médico (Público)":
    st.title("👨‍⚕️ Registo de Ponto do Pessoal Médico")
    
    medico_nome = st.text_input("Nome do Profissional / ID")
    tipo_ponto = st.selectbox("Tipo de Registo", ["Entrada de Turno", "Saída de Turno", "Pausa"])
    
    if st.button("Registar Ponto"):
        if medico_nome:
            st.success(f"Ponto de **{tipo_ponto}** registado para **{medico_nome}**!")
        else:
            st.warning("Insira o seu nome ou ID de funcionário.")

# --- 3. PAINEL DO ADMINISTRADOR ---
elif menu == "🔒 Painel do Administrador (Privado)":
    st.title("🔒 Painel do Administrador")
    
    codigo = st.text_input("Insira o Código Mestre de Acesso", type="password")
    
    if codigo == "03032003":
        st.success("Acesso Autorizado!")
        st.subheader("📊 Estatísticas do Sistema")
        st.metric("Pacientes Atendidos Hoje", "24")
        st.metric("Médicos em Serviço", "8")
    elif codigo != "":
        st.error("Código Mestre incorreto!")
