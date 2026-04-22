import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

st.set_page_config(page_title="Gestão de Obras PRO", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

SERVICOS = {
    "--- ESTRUTURA E BASE ---": {"un": "-", "p": 0.0},
    "Sapata / Fundação": {"un": "un", "p": 250.0},
    "Vigamento / Colunas": {"un": "m", "p": 150.0},
    "Laje (Batida)": {"un": "m²", "p": 95.0},
    "Escada em Metalon": {"un": "un", "p": 1200.0},
    "Alvenaria (Tijolo/Bloco)": {"un": "m²", "p": 60.0},
    "--- ACABAMENTO FINO ---": {"un": "-", "p": 0.0},
    "Reboco": {"un": "m²", "p": 40.0},
    "Piso Cerâmico": {"un": "m²", "p": 50.0},
    "Porcelanato (Chão/Parede)": {"un": "m²", "p": 75.0},
    "Bancada em Porcelanato": {"un": "m", "p": 350.0},
    "--- DESENTUPIDORA / HIDRÁULICA ---": {"un": "-", "p": 0.0},
    "Desentupimento Vaso/Pia": {"un": "un", "p": 200.0},
    "Limpeza Caixa de Gordura": {"un": "un", "p": 200.0},
    "Ponto de Hidráulica": {"un": "ponto", "p": 140.0},
}

st.title("🏗️ Orçamento Profissional")

# --- PAINEL PRIVADO (Lado Esquerdo) ---
st.sidebar.header("⚒️ SEUS CUSTOS OCULTOS")
dist = st.sidebar.number_input("KM Total (Ida/Volta)", min_value=0.0)
p_km = st.sidebar.number_input("Preço do KM", value=2.50)
margem = st.sidebar.slider("Margem de Lucro (%)", 0, 100, 20)
produtividade = st.sidebar.number_input("Produção (m² por dia)", value=10.0)

custo_viagem = dist * p_km

# --- DADOS DO CLIENTE ---
c1, c2 = st.columns(2)
nome_c = c1.text_input("Nome do Cliente")
local_s = c2.text_input("Local do Serviço")

# --- SELEÇÃO DE SERVIÇOS ---
selecionados = []
total_maodobra_pura = 0.0
total_m2 = 0.0

idx = 0
for nome, info in SERVICOS.items():
    if info["un"] == "-":
        st.markdown(f"#### {nome}")
        continue
    with st.expander(f"➕ {nome}"):
        col1, col2 = st.columns(2)
        qtd = col1.number_input(f"Qtd", min_value=0.0, key=f"q_{idx}")
        prc = col2.number_input(f"Seu Preço Base", value=float(info['p']), key=f"p_{idx}")
        if qtd > 0:
            sub = qtd * prc
            total_maodobra_pura += sub
            if info["un"] == "m²": total_m2 += qtd
            selecionados.append({"n": nome, "q": qtd, "u": info['un'], "p_original": prc})
    idx += 1

# --- CÁLCULO DA DILUIÇÃO ---
valor_base_com_frete = total_maodobra_pura + custo_viagem
valor_final_total = valor_base_com_frete * (1 + margem/100)

# Fator que vai "engordar" cada item
fator = valor_final_total / total_maodobra_pura if total_maodobra_pura > 0 else 1

dias_trampo = math.ceil(total_m2 / produtividade) if total_m2 > 0 else 1

# --- ÁREA DO CLIENTE (O QUE ELE VÊ) ---
if selecionados:
    st.divider()
    st.header(f"💰 Valor para o Cliente: {moeda(valor_final_total)}")
    
    # WHATSAPP SEM MARGEM E SEM VIAGEM APARECENDO
    txt_cliente = f"*ORÇAMENTO: {nome_c.upper()}*\n📍 Local: {local_s}\n"
    txt_cliente += f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
    txt_cliente += "-"*25 + "\n"
    
    for s in selecionados:
        # Aqui a mágica acontece: o preço unitário já vai com lucro e frete embutidos
        p_final_item = s['p_original'] * fator
        sub_final_item = s['q'] * p_final_item
        txt_cliente += f"✅ *{s['n']}*: {s['q']} {s['u']} | Unit: {moeda(p_final_item)} = {moeda(sub_final_item)}\n"
    
    txt_cliente += "-"*25 + "\n"
    txt_cliente += f"⏱️ *Prazo Estimado:* {dias_trampo} dias úteis\n"
    txt_cliente += f"💰 *VALOR TOTAL: {moeda(valor_final_total)}*"
    txt_cliente += "\n\n_Obs: Mão de obra especializada. Material por conta do cliente._"

    st.subheader("📋 Resumo para o WhatsApp")
    st.text_area("Copia aqui (Tudo diluído):", value=txt_cliente, height=250)

    # PDF TAMBÉM LIMPO
    if st.button("📥 Gerar PDF Profissional"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(190, 10, "PROPOSTA DE PRESTACAO DE SERVICOS", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12); pdf.ln(10)
            pdf.cell(190, 8, f"Cliente: {nome_c}", ln=True)
            pdf.cell(190, 8, f"Prazo: {dias_trampo} dias uteis", ln=True)
            pdf.ln(5); pdf.cell(190, 0, "", "T", ln=True); pdf.ln(5)
            for s in selecionados:
                p_ajust = s['p_original'] * fator
                pdf.cell(190, 8, f"- {s['n']} ({s['q']} {s['u']}) | Valor: {moeda(p_ajust * s['q'])}", ln=True)
            pdf.ln(5); pdf.set_font("Helvetica", "B", 14)
            pdf.cell(190, 10, f"TOTAL: {moeda(valor_final_total)}", ln=True)
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("Baixar PDF", pdf_bytes, f"orcamento_{nome_c}.pdf", "application/pdf")
        except: st.error("Erro no PDF.")
