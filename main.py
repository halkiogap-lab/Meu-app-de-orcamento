import streamlit as st
from datetime import datetime
from fpdf import FPDF

# Configuração de Patrão
st.set_page_config(page_title="Orçamento PRO", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- LISTA DE SERVIÇOS ---
SERVICOS = {
    "Alvenaria": {"un": "m²", "p": 55.0},
    "Reboco": {"un": "m²", "p": 35.0},
    "Piso": {"un": "m²", "p": 45.0},
    "Porcelanato": {"un": "m²", "p": 65.0},
    "Pintura + Massa": {"un": "m²", "p": 60.0},
    "Hidráulica": {"un": "ponto", "p": 120.0},
    "Elétrica": {"un": "ponto", "p": 120.0},
    "Laje": {"un": "m²", "p": 90.0},
    "Telhado Zinco": {"un": "m²", "p": 180.0},
    "Pia Mármore": {"un": "un", "p": 250.0},
    "Box Banheiro": {"un": "un", "p": 180.0}
}

st.title("🏗️ Sistema de Orçamentos Profissional")

# --- DADOS DO CLIENTE ---
with st.expander("👤 Dados do Cliente", expanded=True):
    c1, c2 = st.columns(2)
    nome_c = c1.text_input("Nome do Cliente")
    obra_c = c2.text_input("Local da Obra")

# --- CUSTOS E LUCRO ---
with st.expander("💰 Custos e Margem de Lucro", expanded=True):
    col1, col2, col3 = st.columns(3)
    dist = col1.number_input("Distância (KM)", min_value=0.0)
    p_km = col2.number_input("R$ por KM", value=2.50)
    lucro = col3.slider("Margem de Lucro Extra (%)", 0, 50, 0)

custo_viagem = dist * p_km

# --- SERVIÇOS ---
st.subheader("🛠️ Serviços Selecionados")
selecionados = []
total_mo = 0.0

for nome, info in SERVICOS.items():
    with st.expander(f"➕ {nome}"):
        sc1, sc2 = st.columns(2)
        q = sc1.number_input(f"Quantidade ({info['un']})", min_value=0.0, key=f"q_{nome}")
        p = sc2.number_input(f"Preço Base R$", value=float(info['p']), key=f"p_{nome}")
        
        if q > 0:
            sub = q * p
            total_mo += sub
            selecionados.append({"n": nome, "q": q, "u": info['un'], "t": sub})

# --- CÁLCULO FINAL ---
total_com_lucro = (total_mo + custo_viagem) * (1 + lucro/100)
st.divider()
st.header(f"TOTAL GERAL: {moeda(total_com_lucro)}")

# --- GERAÇÃO DE PDF E WHATSAPP ---
if selecionados:
    # Texto Zap
    zap_txt = f"*ORÇAMENTO PROFISSIONAL*\nCliente: {nome_c}\nLocal: {obra_c}\n"
    for s in selecionados:
        zap_txt += f"✅ {s['n']}: {s['q']} {s['u']} = {moeda(s['t'])}\n"
    zap_txt += f"🚚 Viagem: {moeda(custo_viagem)}\n"
    if lucro > 0: zap_txt += f"📈 Margem Aplicada: {lucro}%\n"
    zap_txt += f"💰 *TOTAL: {moeda(total_com_lucro)}*"

    st.text_area("Texto para WhatsApp", value=zap_txt, height=200)

    # Função PDF (Simples)
    if st.button("Gerar PDF do Orçamento"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "ORCAMENTO DE OBRA", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(190, 10, f"Cliente: {nome_c}", ln=True)
        pdf.cell(190, 10, f"Obra: {obra_c}", ln=True)
        pdf.cell(190, 10, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(5)
        pdf.cell(190, 10, "-"*60, ln=True)
        for s in selecionados:
            pdf.cell(190, 10, f"{s['n']}: {s['q']} {s['u']} - {moeda(s['t'])}", ln=True)
        pdf.cell(190, 10, f"Deslocamento: {moeda(custo_viagem)}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, f"TOTAL GERAL: {moeda(total_com_lucro)}", ln=True)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="📥 Baixar Orçamento em PDF", data=pdf_output, file_name=f"orcamento_{nome_c}.pdf", mime="application/pdf")
