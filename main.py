import streamlit as st
from datetime import datetime
from fpdf import FPDF

# --- INTERFACE LIMPA E SEM ERROS ---
st.set_page_config(page_title="PRO-OBRA FINAL", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- LISTA DIRETA DE SERVIÇOS ---
SERVICOS = {
    "🏗️ ESTRUTURA": {"Sapata": 280.0, "Viga": 85.0, "Laje": 115.0, "Alvenaria": 65.0},
    "💎 ACABAMENTO": {"Reboco": 45.0, "Porcelanato": 95.0, "Pintura": 80.0, "Bancada": 550.0},
    "🔧 OUTROS": {"Hidráulica": 160.0, "Telhado": 195.0, "Limpeza": 25.0}
}

st.sidebar.title("💰 AJUSTES")
margem = st.sidebar.slider("Lucro (%)", 0, 100, 40)
frete = st.sidebar.number_input("Custo KM", value=3.50)

st.title("🏛️ Sistema de Orçamentos Profissional")

# Campos de texto
cli = st.text_input("Nome do Cliente")
loc = st.text_input("Local da Obra")
dist = st.number_input("Distância KM", min_value=0.0)

st.divider()

sel = []
total_base = 0.0

# Seleção de serviços
for cat, itens in SERVICOS.items():
    with st.expander(cat):
        for nome, preco in itens.items():
            qtd = st.number_input(f"{nome} (Qtd)", min_value=0.0, key=nome)
            if qtd > 0:
                total_base += (qtd * preco)
                sel.append({"n": nome, "q": qtd, "p": preco})

if sel:
    st.divider()
    # Cálculos
    valor_final = (total_base + (dist * frete)) * (1 + margem/100)
    fator = valor_final / total_base if total_base > 0 else 1
    
    st.metric("VALOR TOTAL PARA O CLIENTE", moeda(valor_final))
    
    # Zap
    txt_zap = f"*ORÇAMENTO: {cli}*\n"
    for i in sel:
        txt_zap += f"- {i['n']}: {moeda((i['q']*i['p'])*fator)}\n"
    txt_zap += f"\n*TOTAL: {moeda(valor_final)}*"
    st.text_area("Copia pro WhatsApp", txt_zap)

    # PDF
    if st.button("📄 Gerar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "ORCAMENTO", 0, 1, "C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(190, 10, f"CLIENTE: {cli}", 0, 1)
        for i in sel:
            pdf.cell(190, 8, f"- {i['n']}: {moeda((i['q']*i['p'])*fator)}", 0, 1)
        pdf.ln(10)
        pdf.cell(190, 10, f"TOTAL: {moeda(valor_final)}", 0, 1, "R")
        
        out = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("📥 Baixar PDF", out, "Orcamento.pdf", "application/pdf")
