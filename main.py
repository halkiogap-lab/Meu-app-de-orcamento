import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- SETUP ESTÉTICO ---
st.set_page_config(page_title="OT CONSTRUÇÕES | Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetricValue"] { color: #FFFFFF; font-size: 24px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #262730; color: white; border: 1px solid #444; }
    .stButton>button:hover { border-color: #FF4B4B; color: #FF4B4B; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --- ESTRUTURA DE DADOS ---
ETAPAS = {
    "01. Fundação & Infra": ["Locação/gabarito", "Escavação", "Sapatas", "Blocos", "Viga baldrame", "Impermeabilização"],
    "02. Estrutura & Alvenaria": ["Colunas", "Pilares", "Vigas", "Lajes", "Escadas"],
    "03. Instalações Brutas": ["Esgoto", "Pontos de água", "Conduítes", "Quadros de energia"],
    "04. Cobertura": ["Telhados Zinco/Sanduíche", "Estrutura Metalon", "Calhas/Rufos"],
    "05. Revestimento": ["Reboco", "Contra-piso", "Gesso", "Porcelanatos", "Bancadas"],
    "06. Pintura & Entrega": ["Massa corrida", "Pintura", "Texturas", "Limpeza pós-obra"]
}

# --- HEADER ---
col_logo, col_info = st.columns([3, 1])
with col_logo:
    st.title("OT CONSTRUÇÕES")
    st.caption("SISTEMA DE INTELIGÊNCIA EM ORÇAMENTOS DE ALTO PADRÃO")

# --- INPUTS LIMPOS ---
with st.container():
    c1, c2, c3 = st.columns(3)
    cliente = c1.text_input("NOME DO CLIENTE", placeholder="Ex: Residência Alphaville")
    endereco = c2.text_input("LOCALIZAÇÃO", placeholder="Cidade/UF")
    m2 = c3.number_input("METRAGEM TOTAL (M²)", min_value=0.0, step=1.0, value=0.0)

st.divider()

# --- ÁREA DE CÁLCULO ---
orcamento_dados = []

for etapa, itens in ETAPAS.items():
    with st.expander(etapa, expanded=False):
        cols = st.columns([3, 1, 1])
        for item in itens:
            check = cols[0].checkbox(item, key=f"ch_{item}")
            if check:
                valor_custo = cols[1].number_input("Custo Mão de Obra", key=f"v_{item}", min_value=0.0)
                prazo_item = cols[2].number_input("Dias Estimados", key=f"d_{item}", min_value=0)
                orcamento_dados.append({"Etapa": etapa, "Item": item, "Custo": valor_custo, "Dias": prazo_item})

st.sidebar.header("CONFIGURAÇÕES DE LUCRO")
margem = st.sidebar.slider("MARGEM DE LUCRO (%)", 0, 100, 30) / 100
km_obra = st.sidebar.number_input("DISTÂNCIA (KM)", 0.0)
custo_km = st.sidebar.number_input("VALOR POR KM (R$)", 2.50)
logistica = km_obra * custo_km

# --- PROCESSAMENTO ---
custo_bruto = sum(item['Custo'] for item in orcamento_dados) + logistica
preco_venda = custo_bruto * (1 + margem)
lucro_real = preco_venda - custo_bruto
total_dias = sum(item['Dias'] for item in orcamento_dados)

# --- DASHBOARD GESTOR ---
st.subheader("PAINEL DO GESTOR")
d1, d2, d3, d4 = st.columns(4)
d1.metric("CUSTO TOTAL", f"R$ {custo_bruto:,.2f}")
d2.metric("PREÇO FINAL (CLIENTE)", f"R$ {preco_venda:,.2f}")
d3.metric("LUCRO LÍQUIDO", f"R$ {lucro_real:,.2f}")
d4.metric("CRONOGRAMA", f"{total_dias} DIAS")

# --- EXPORTAÇÃO ---
if st.button("GERAR DOCUMENTO OFICIAL"):
    if not cliente:
        st.error("Insira o nome do cliente antes de gerar o PDF.")
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(30, 30, 30)
        pdf.rect(0, 0, 210, 40, 'F')
        
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 20, "OT CONSTRUCOES", ln=True, align='C')
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        pdf.ln(25)
        pdf.cell(0, 10, f"CLIENTE: {cliente.upper()}", ln=True)
        pdf.cell(0, 10, f"LOCAL: {endereco.upper()}", ln=True)
        pdf.cell(0, 10, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "RESUMO DOS SERVICOS", ln=True)
        pdf.set_font("Arial", '', 10)
        
        for item in orcamento_dados:
            pdf.cell(140, 8, f"- {item['Item']}", border='B')
            pdf.cell(50, 8, "INCLUSO", border='B', align='R', ln=True)
            
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"VALOR TOTAL DA OBRA: R$ {preco_venda:,.2f}", align='R')
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("CLIQUE AQUI PARA BAIXAR O PDF", pdf_bytes, f"Orcamento_{cliente}.pdf", "application/pdf")
