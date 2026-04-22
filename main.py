import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO VISUAL PREMIUM ---
st.set_page_config(page_title="ENGINEERING PRO | ERP", layout="wide")

# CSS para Customização de Interface (Estilo Dark Moderno)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    .stExpander { border: 1px solid #374151; border-radius: 8px; margin-bottom: 10px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS INTEGRAL (DA FUNDAÇÃO À CHAVE) ---
DB_MESTRE = {
    "🏗️ ETAPA 1: INFRAESTRUTURA": {
        "Locação e Gabarito": {"un": "m²", "p": 15.0},
        "Escavação de Valas/Sapatas": {"un": "m³", "p": 120.0},
        "Sapata / Fundação (Mão de Obra)": {"un": "un", "p": 280.0},
        "Viga Baldrame": {"un": "m", "p": 85.0},
        "Impermeabilização de Fundação": {"un": "m²", "p": 35.0},
    },
    "🧱 ETAPA 2: ESTRUTURA E ALVENARIA": {
        "Colunas / Pilares": {"un": "m", "p": 165.0},
        "Vigas de Cintamento": {"un": "m", "p": 140.0},
        "Laje (Montagem e Batida)": {"un": "m²", "p": 115.0},
        "Alvenaria (Tijolo/Bloco)": {"un": "m²", "p": 65.0},
        "Escada Estrutural": {"un": "un", "p": 1500.0},
    },
    "🚿 ETAPA 3: INSTALAÇÕES E COBERTURA": {
        "Pontos de Hidráulica/Esgoto": {"un": "ponto", "p": 160.0},
        "Quadro de Distribuição Elétrica": {"un": "un", "p": 450.0},
        "Estrutura de Telhado": {"un": "m²", "p": 120.0},
        "Telhamento (Zinco/Sanduíche)": {"un": "m²", "p": 90.0},
        "Calhas e Rufos": {"un": "m", "p": 60.0},
    },
    "💎 ETAPA 4: ACABAMENTO E PINTURA": {
        "Reboco Técnico": {"un": "m²", "p": 45.0},
        "Porcelanato (Chão/Parede)": {"un": "m²", "p": 95.0},
        "Bancada em Porcelanato Esculpido": {"un": "m", "p": 550.0},
        "Massa Corrida e Pintura Final": {"un": "m²", "p": 80.0},
        "Instalação de Louças e Metais": {"un": "un", "p": 130.0},
    }
}

# --- SIDEBAR (PAINEL DE CONTROLE FINANCEIRO) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4320/4320350.png", width=80)
st.sidebar.title("CONTROLE OPERACIONAL")
st.sidebar.divider()
margem_lucro = st.sidebar.slider("Margem de Lucro (%)", 0, 200, 40)
custo_operacional_km = st.sidebar.number_input("Custo Logístico (R$/KM)", value=3.50)
meta_m2_dia = st.sidebar.number_input("Rendimento da Equipe (m²/dia)", value=10.0)

# --- CORPO PRINCIPAL ---
st.title("🏛️ Engineering Pro System")
st.subheader("Gestão de Orçamentos de Alto Padrão")

# Seção de Dados do Cliente
with st.container():
    c1, c2, c3 = st.columns([2, 2, 1])
    cliente = c1.text_input("👤 Nome do Cliente / Proprietário")
    local = c2.text_input("📍 Localização da Obra")
    distancia = c3.number_input("🚗 Distância (KM)", min_value=0.0)

st.divider()

# Colunas para Seleção e Resultados
col_dados, col_resumo = st.columns([3, 2])

with col_dados:
    st.markdown("### 📋 Seleção de Serviços")
    selecionados = []
    total_base = 0.0
    total_area_m2 = 0.0
    idx = 0

    for etapa, servicos in DB_MESTRE.items():
        with st.expander(f"**{etapa}**", expanded=False):
            for s, info in servicos.items():
                st.markdown(f"**{s}**") # Nome do serviço em destaque
                c_q, c_p = st.columns(2)
                qtd = c_q.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{idx}")
                p_unit = c_p.number_input(f"Preço Base unit.", value=float(info['p']), key=f"p_{idx}")
                
                if qtd > 0:
                    total_base += (qtd * p_unit)
                    if info['un'] == "m²": total_area_m2 += qtd
                    selecionados.append({"n": s, "q": qtd, "u": info['un'], "p": p_unit})
                idx += 1

with col_resumo:
    st.markdown("### 📊 Monitor de Lucratividade")
    if not selecionados:
        st.info("Aguardando seleção de serviços...")
    else:
        # Cálculos de Engenharia
        custo_viagem = distancia * custo_operacional_km
        valor_final = (total_base + custo_viagem) * (1 + margem_lucro/100)
        fator_venda = valor_final / total_base if total_base > 0 else 1
        prazo_obra = math.ceil(total_area_m2 / meta_m2_dia) if total_area_m2 > 0 else 1
        lucro_limpo = valor_final - total_base - custo_viagem

        # Cards de Métricas
        st.metric("FAT
