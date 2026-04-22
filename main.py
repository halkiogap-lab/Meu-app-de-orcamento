import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO DE INTERFACE PREMIUM ---
st.set_page_config(page_title="ENGINEERING PRO | ERP", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    .stExpander { border: 1px solid #374151; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS COMPLETO (DA FUNDAÇÃO À CHAVE) ---
DB_OBRA = {
    "🏗️ 1. INFRAESTRUTURA": {
        "Locação e Gabarito": {"un": "m²", "p": 15.0},
        "Sapata / Fundação": {"un": "un", "p": 280.0},
        "Viga Baldrame": {"un": "m", "p": 85.0},
        "Impermeabilização": {"un": "m²", "p": 35.0},
    },
    "🧱 2. ESTRUTURA E ALVENARIA": {
        "Colunas / Pilares": {"un": "m", "p": 165.0},
        "Laje (Montagem/Batida)": {"un": "m²", "p": 115.0},
        "Alvenaria (Vedação)": {"un": "m²", "p": 65.0},
        "Escada Estrutural": {"un": "un", "p": 1500.0},
    },
    "🚿 3. HIDRÁULICA E TELHADO": {
        "Pontos de Esgoto/Água": {"un": "ponto", "p": 160.0},
        "Telhado (Zinco/Sanduíche)": {"un": "m²", "p": 195.0},
        "Calhas e Rufos": {"un": "m", "p": 60.0},
    },
    "💎 4. ACABAMENTO FINO": {
        "Porcelanato (Chão/Parede)": {"un": "m²", "p": 95.0},
        "Bancada em Porcelanato": {"un": "m", "p": 550.0},
        "Rodapé Embutido": {"un": "m", "p": 28.0},
        "Pintura (Massa + Tinta)": {"un": "m²", "p": 80.0},
        "Limpeza Pós-Obra": {"un": "m²", "p": 25.0},
    }
}

# --- PAINEL LATERAL ---
st.sidebar.title("🎮 PAINEL DE CONTROLE")
margem = st.sidebar.slider("Margem de Lucro (%)", 0, 200, 40)
custo_km = st.sidebar.number_input("R$ por KM", value=3.50)
rendimento = st.sidebar.number_input("Rendimento (m²/dia)", value=10.0)

st.title("🏛️ Engineering Pro System")

# Dados Iniciais
c1, c2, c3 = st.columns([2, 2, 1])
cliente = c1.text_input("Cliente")
local = c2.text_input("Local da Obra")
distancia = c3.number_input("KM (Ida/Volta)", min_value=0.0)

st.divider()

col_serv, col_dash = st.columns([3, 2])

with col_serv:
    st.subheader("📋 Seleção de Serviços")
    selecionados = []
    total_base = 0.0
    area_m2 = 0
