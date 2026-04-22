import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO DE INTERFACE LIMPA ---
st.set_page_config(page_title="PRO-OBRA | GESTÃO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE SERVIÇOS SEM ERRO ---
SERVICOS = {
    "🏗️ 1. BASE E ESTRUTURA": {
        "Locação/Gabarito": 15.0,
        "Sapata/Fundação": 280.0,
        "Viga Baldrame": 85.0,
        "Laje (Montagem/Batida)": 115.0,
        "Alvenaria de Vedação": 65.0
    },
    "💎 2. ACABAMENTO": {
        "Reboco Técnico": 45.0,
        "Porcelanato": 95.0,
        "Bancada Esculpida": 550.0,
        "Rodapé Embutido": 28.0,
        "Pintura (Massa + Tinta)": 80.0
    },
    "🔧 3. UTILIDADES": {
        "Ponto Hidráulico": 160.0,
        "Telhado Zinco/Sanduíche": 195.0,
        "Desentupimento K50": 320.0,
        "Limpeza Caixa Gordura": 250.0
    }
}

# --- PAINEL DE CONTROLE ---
st.sidebar.title("💰 AJUSTES FINANCEIROS")
margem = st.sidebar.slider("Margem de Lucro (%)", 0, 150, 40)
frete_km = st.sidebar.number_input("Custo KM", value=3.50)

st.title("🏛
