import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="SNS Digital - Guiné-Bissau 🇬🇼",
    page_icon="🇬🇼",
    layout="wide"
)

# --- INICIALIZAÇÃO DA BASE DE DADOS EM MEMÓRIA ---
if "historico_triagens" not in st.session_state:
    st.session_state.historico_triagens = []

if "historico_pontos" not in st.session_state:
    st.session_state.historico_pontos = []

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Guinea-Bissau.svg",
    width=120
)

st.sidebar.markdown("<span style='color:red; font-size:11px; font-weight:bold;'>Diolindo Mendes</span>", unsafe_allow_html=True)
st.sidebar.title("🇬🇼 SNS Digital")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["🩺 Triagem de Pacientes (Público)", "👨‍⚕️ Ponto Médico (Público)", "🔒 Painel do Administrador (Privado)"]
)

# --- 1. TRIAGEM DE PACIENTES ---
if menu == "🩺 Triagem de Pacientes (Público)":
    st.markdown("<span style='color:red; font-size:12px; font-weight:bold;'>Diolindo Mendes</span>", unsafe_allow_html=True)
    st.title("🩺 Portal de Triagem Hospitalar 🇬🇼")
    st.write("Preencha os dados do paciente e do médico responsável para efetuar a triagem.")

    col1, col2 = st.columns(2)
    with col1:
        nome_medico = st.text_input("Nome do Médico / Profissional Responsável")
        nome_paciente = st.text_input("Nome Completo do Paciente")
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
        if nome_medico and nome_paciente and sintomas:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
            novo_registo = {
                "Data/Hora": data_hora,
                "Médico Responsável": nome_medico,
                "Paciente": nome_paciente,
                "Especialidade": especialidade,
                "Urgência": urgencia,
                "Sintomas": sintomas
            }
            st.session_state.historico_triagens.append(novo_registo)
            st.success(f"Triagem do paciente **{nome_paciente}** registada com sucesso pelo(a) Dr(a). **{nome_medico}**!")
        else:
            st.warning("Por favor, preencha o nome do médico, do paciente e os sintomas.")

    # Exibição de todos os registos de triagem
    st.markdown("---")
    st.subheader("📋 Histórico de Pacientes Registados")
    if st.session_state.historico_triagens:
        st.dataframe(st.session_state.historico_triagens, use_container_width=True)
    else:
        st.info("Nenhum paciente registado até ao momento.")

# --- 2. PONTO MÉDICO ---
elif menu == "👨‍⚕️ Ponto Médico (Público)":
    st.markdown("<span style='color:red; font-size:12px; font-weight:bold;'>Diolindo Mendes</span>", unsafe_allow_html=True)
    st.title("👨‍⚕️ Registo de Ponto do Pessoal Médico")
    
    col_med1, col_med2 = st.columns(2)
    with col_med1:
        medico_nome = st.text_input("Nome do Profissional / ID")
    with col_med2:
        tipo_ponto = st.selectbox("Tipo de Registo", ["Entrada de Turno", "Saída de Turno", "Pausa"])
    
    if st.button("Registar Ponto"):
        if medico_nome:
            hora_ponto = datetime.now().strftime("%d/%m/%Y %H:%M")
            registo_ponto = {
                "Data/Hora": hora_ponto,
                "Profissional": medico_nome,
                "Tipo de Registo": tipo_ponto
            }
            st.session_state.historico_pontos.append(registo_ponto)
            st.success(f"Ponto de **{tipo_ponto}** registado com sucesso para **{medico_nome}** às {hora_ponto}!")
        else:
            st.warning("Insira o seu nome ou ID de funcionário.")

    # Exibição de todos os pontos registados
    st.markdown("---")
    st.subheader("👨‍⚕️ Médicos e Profissionais que Registaram Ponto")
    if st.session_state.historico_pontos:
        st.dataframe(st.session_state.historico_pontos, use_container_width=True)
    else:
        st.info("Nenhum registo de ponto efetuado até ao momento.")

# --- 3. PAINEL DO ADMINISTRADOR ---
elif menu == "🔒 Painel do Administrador (Privado)":
    st.markdown("<span style='color:red; font-size:12px; font-weight:bold;'>Diolindo Mendes</span>", unsafe_allow_html=True)
    st.title("🔒 Painel do Administrador")
    
    codigo = st.text_input("Insira o Código Mestre de Acesso", type="password")
    
    if codigo == "03032003":
        st.success("Acesso Autorizado!")
        
        st.subheader("📊 Resumo Geral do Sistema")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Triagens Registadas", len(st.session_state.historico_triagens))
        col_m2.metric("Total de Registos de Ponto", len(st.session_state.historico_pontos))

        st.markdown("---")
        st.subheader("📂 Registos de Triagens (Visão Administrativa)")
        st.dataframe(st.session_state.historico_triagens, use_container_width=True)

        st.subheader("📂 Registos de Ponto Médico (Visão Administrativa)")
        st.dataframe(st.session_state.historico_pontos, use_container_width=True)
        
    elif codigo != "":
        st.error("Código Mestre incorreto!")
