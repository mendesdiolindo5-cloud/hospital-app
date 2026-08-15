import streamlit as st
import json
from datetime import datetime

# Configuração da página Web para telemóveis e computadores
st.set_page_config(
    page_title="Sistema Hospitalar & Ministério",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização da base de dados em memória do site (Session State)
if "triagens" not in st.session_state:
    st.session_state.triagens = []

if "medicos_ativos" not in st.session_state:
    st.session_state.medicos_ativos = {}

if "notificacoes" not in st.session_state:
    st.session_state.notificacoes = []

# PIN de Acesso Restrito
CODIGO_MESTRE = "03032003"

# --- BARRA LATERAL (MENU E AUTENTICAÇÃO) ---
st.sidebar.title("🏥 SNS Digital")
opcao = st.sidebar.radio(
    "Navegação", 
    ["🩺 Triagem de Pacientes (Público)", "👨‍⚕️ Ponto Médico (Público)", "🔒 Painel do Administrador (Privado)"]
)

# Exibição de Notificações na Barra Lateral
st.sidebar.markdown("---")
st.sidebar.subheader("🔔 Notificações do Sistema")
if st.session_state.notificacoes:
    for notif in reversed(st.session_state.notificacoes[-5:]):
        st.sidebar.info(notif)
else:
    st.sidebar.write("Sem notificações recentes.")

# --- ECRÃ 1: TRIAGEM DE PACIENTES (PÚBLICO) ---
if opcao == "🩺 Triagem de Pacientes (Público)":
    st.title("🩺 Portal de Triagem Hospitalar")
    st.caption("Preencha os dados do paciente para encaminhamento automático.")

    col1, col2 = st.columns(2)
    with col1:
        nome_paciente = st.text_input("Nome Completo do Paciente")
        sintomas = st.text_area("Sintomas Apresentados")
    with col2:
        especialidade = st.selectbox(
            "Especialidade Médica",
            ["Cardiologia", "Neurologia", "Pediatria", "Ortopedia", "Cirurgia Geral", "Clínica Geral"]
        )
        prioridade = st.select_slider(
            "Nível de Urgência (Manchester)",
            options=["🟢 Verde (Pouco Urgente)", "🟡 Amarelo (Urgente)", "🟠 Laranja (Muito Urgente)", "🔴 Vermelho (Emergência)"]
        )

    if st.button("Submeter Triagem"):
        if nome_paciente and sintomas:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registo = {
                "paciente": nome_paciente,
                "sintomas": sintomas,
                "especialidade": especialidade,
                "prioridade": prioridade,
                "data_hora": agora
            }
            st.session_state.triagens.append(registo)
            
            # Gera a Notificação
            msg_notif = f"🚨 Nova Triagem: {nome_paciente} ({especialidade}) às {datetime.now().strftime('%H:%M')}"
            st.session_state.notificacoes.append(msg_notif)
            
            st.success("✅ Triagem submetida com sucesso!")
            st.rerun()
        else:
            st.warning("Por favor, preencha o nome e os sintomas.")

# --- ECRÃ 2: PONTO MÉDICO (PÚBLICO) ---
elif opcao == "👨‍⚕️ Ponto Médico (Público)":
    st.title("👨‍⚕️ Registo de Ponto do Corpo Médico")
    
    col1, col2 = st.columns(2)
    with col1:
        nome_medico = st.text_input("Nome do Médico(a)")
        cedula = st.text_input("Cédula Profissional")
    with col2:
        especialidade_med = st.selectbox("Especialidade", ["Cardiologia", "Pediatria", "Ortopedia", "Clínica Geral", "Urgência"])

    btn_entrar, btn_sair = st.columns(2)
    
    with btn_entrar:
        if st.button("🟢 Entrar em Turno"):
            if nome_medico and cedula:
                agora = datetime.now().strftime("%H:%M:%S")
                st.session_state.medicos_ativos[cedula] = {
                    "nome": nome_medico,
                    "especialidade": especialidade_med,
                    "entrada": agora
                }
                st.session_state.notificacoes.append(f"👨‍⚕️ Entrada: Dr(a). {nome_medico} ({especialidade_med})")
                st.success(f"Turno iniciado para Dr(a). {nome_medico}")
                st.rerun()

    with btn_sair:
        if st.button("🔴 Encerrar Turno"):
            if cedula in st.session_state.medicos_ativos:
                medico = st.session_state.medicos_ativos.pop(cedula)
                st.session_state.notificacoes.append(f"🚪 Saída: Dr(a). {medico['nome']}")
                st.warning(f"Turno encerrado para Dr(a). {medico['nome']}")
                st.rerun()

# --- ECRÃ 3: PAINEL RESTRITO (SÓ COM CÓDIGO) ---
elif opcao == "🔒 Painel do Administrador (Privado)":
    st.title("🔒 Área Restrita de Gestão & Ministério da Saúde")
    
    # Campo de Código Seguro
    codigo_inserido = st.text_input("Insira o Código Mestre de Acesso:", type="password")

    if codigo_inserido == CODIGO_MESTRE:
        st.success("🔓 Acesso Concedido! Bem-vindo ao Painel de Controlo Central.")
        
        # Dashboard de Dados
        st.subheader("📊 Estatísticas em Tempo Real")
        col_a, col_b = st.columns(2)
        col_a.metric("Médicos em Serviço", len(st.session_state.medicos_ativos))
        col_b.metric("Total de Triagens Hoje", len(st.session_state.triagens))

        # Tabela de Médicos Ativos
        st.markdown("---")
        st.subheader("👨‍⚕️ Médicos Atualmente em Turno")
        if st.session_state.medicos_ativos:
            st.json(st.session_state.medicos_ativos)
        else:
            st.write("Nenhum médico em turno no momento.")

        # Tabela de Pacientes
        st.subheader("📋 Lista de Triagens Efetuadas")
        if st.session_state.triagens:
            st.dataframe(st.session_state.triagens)
        else:
            st.write("Nenhum paciente na fila de triagem.")

        # Integração Ministério da Saúde (JSON Export)
        st.markdown("---")
        st.subheader("🌐 Pacote de Transmissão para o Ministério da Saúde")
        pacote_ministerio = {
            "hospital_id": "HOSP-NACIONAL-01",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "medicos_em_turno": st.session_state.medicos_ativos,
            "registos_triagem": st.session_state.triagens
        }
        st.json(pacote_ministerio)

    elif codigo_inserido != "":
        st.error("❌ Código Incorreto! Acesso negado.")