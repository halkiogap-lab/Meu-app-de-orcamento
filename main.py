import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

st.set_page_config(page_title="Orçamento Mestre", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- A LISTA COMPLETA QUE VOCÊ QUER (NÃO TIROU NADA AGORA) ---
SERVICOS = {
    "--- ESTRUTURA E BASE ---": {"un": "-", "p": 0.0},
    "Sapata / Fundação": {"un": "un", "p": 250.0},
    "Vigamento / Colunas": {"un": "m", "p": 150.0},
    "Laje (Batida)": {"un": "m²", "p": 95.0},
    "Escada em Metalon": {"un": "un", "p": 1200.0},
    "Alvenaria (Tijolo/Bloco)": {"un": "m²", "p": 60.0},
    "Contra-piso": {"un": "m²", "p": 35.0},
    
    "--- ACABAMENTO FINO ---": {"un": "-", "p": 0.0},
    "Reboco": {"un": "m²", "p": 40.0},
    "Piso Cerâmico": {"un": "m²", "p": 50.0},
    "Porcelanato (Chão/Parede)": {"un": "m²", "p": 75.0},
    "Bancada em Porcelanato (Corte/Inst)": {"un": "m", "p": 350.0},
    "Rejunte": {"un": "m²", "p": 15.0},
    "Gesso Liso": {"un": "m²", "p": 45.0},
    "Forro PVC / Gesso": {"un": "m²", "p": 55.0},
    
    "--- ELÉTRICA E HIDRÁULICA ---": {"un": "-", "p": 0.0},
    "Ponto de Elétrica": {"un": "ponto", "p": 130.0},
    "Ponto de Hidráulica": {"un": "ponto", "p": 140.0},
    "Instalação de Caixa d'água": {"un": "un", "p": 300.0},
    "Instalação de Vaso / Pia": {"un": "un", "p": 180.0},
    
    "--- SERVIÇOS DE DESENTUPIDORA ---": {"un": "-", "p": 0.0},
    "Desentupimento de Vaso Sanitário": {"un": "un", "p": 250.0},
    "Desentupimento de Esgoto (Rede)": {"un": "m", "p": 120.0},
    "Desentupimento de Pia / Ralo": {"un": "un", "p": 150.0},
    "Limpeza de Caixa de Gordura": {"un": "un", "p": 200.0},
    "Limpeza de Caixa d'água": {"un": "un", "p": 250.0},
    "Hidrojateamento": {"un": "serv", "p": 400.0},
    
    "--- PINTURA E TELHADO ---": {"un": "-", "p": 0.0},
    "Pintura Simples": {"un": "m²", "p": 35.0},
    "Pintura com Massa": {"un": "m²", "p": 65.0},
    "Telhado Zinco / Telha": {"un": "m²", "p": 185.0},
    "Calhas / Rufos": {"un": "m", "p": 45.0},
}

st.title("🏗️ Orçamento Profissional OMNI")

# --- PAINEL PRIVADO NO SIDEBAR ---
st.sidebar.header("⚒️ PAINEL DE CUSTOS (SÓ VOCÊ)")
dist = st.sidebar.number_input("Distância Total (KM)", min_value=0.0, step=1.0)
p_km = st.sidebar.number_input("Preço do KM", value=2.50)
margem = st.sidebar.slider("Sua Margem de Lucro (%)", 0, 100, 20)
produtividade = st.sidebar.number_input("Seu Rendimento (m²/dia)", value=10.0)

custo_viagem = dist * p_km

# --- DADOS DO CLIENTE ---
c1, c2 = st.columns(2)
nome_c = c1.text_input("Nome do Cliente")
local_s = c2.text_input("Local da Obra/Serviço")

st.divider()

# --- SELEÇÃO DE SERVIÇOS ---
st.subheader("🛠️ Selecione os Serviços")
selecionados = []
total_maodobra_base = 0.0
total_m2_prod = 0.0

idx = 0
for nome, info in SERVICOS.items():
    if info["un"] == "-":
        st.markdown(f"#### {nome}")
        continue
    
    with st.expander(f"➕ {nome}"):
        col1, col2 = st.columns(2)
        qtd = col1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{idx}")
        prc = col2.number_input(f"Valor Base R$", value=float(info['p']), key=f"p_{idx}")
        
        if qtd > 0:
            sub = qtd * prc
            total_maodobra_base += sub
            if info["un"] == "m²": total_m2_prod += qtd
            selecionados.append({"n": nome, "q": qtd, "u": info['un'], "p_base": prc})
    idx += 1

# --- CÁLCULO DE DILUIÇÃO (MÁGICA PRA ESCONDER CUSTO) ---
valor_total_real = (total_maodobra_base + custo_viagem) * (1 + margem/100)
fator = valor_total_real / total_maodobra_base if total_maodobra_base > 0 else 1
dias_trampo = math.ceil(total_m2_prod / produtividade) if total_m2_prod > 0 else 1

# --- RESUMO PRIVADO ---
if selecionados:
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("SEU LUCRO ESTIMADO", moeda(valor_total_real - total_maodobra_base - custo_viagem))
    res2.metric("TOTAL PARA O CLIENTE", moeda(valor_total_real))

    # --- O QUE VAI PRO CLIENTE (SEM VIAGEM, SEM MARGEM) ---
    st.subheader("📋 Resumo para o Cliente (Tudo Diluído)")
    
    txt_cliente = f"*ORÇAMENTO: {nome_c.upper()}*\n📍 Local: {local_s}\n"
    txt_cliente += f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
    txt_cliente += "-"*25 + "\n"
    
    for s in selecionados:
        p_venda = s['p_base'] * fator
        txt_cliente += f"✅ *{s['n']}*: {s['q']} {s['u']} | Unit: {moeda(p_venda)} = {moeda(s['q'] * p_venda)}\n"
    
    txt_cliente += "-"*25 + "\n"
    txt_cliente += f"⏱️ *Prazo Estimado:* {dias_trampo} dias úteis\n"
    txt_cliente += f"💰 *VALOR TOTAL: {moeda(valor_total_real)}*"
    
    st.text_area("Copie para o WhatsApp:", value=txt_cliente, height=300)

    # PDF PROFISSIONAL
    if st.button("📥 Gerar PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(190, 10, "ORCAMENTO DE SERVICOS", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12); pdf.ln(10)
            pdf.cell(190, 8, f"Cliente: {nome_c}", ln=True)
            pdf.cell(190, 8, f"Prazo: {dias_trampo} dias uteis", ln=True)
            pdf.ln(5); pdf.cell(190, 0, "", "T", ln=True); pdf.ln(5)
            for s in selecionados:
                p_venda = s['p_base'] * fator
                pdf.cell(190, 8, f"- {s['n']} ({s['q']} {s['u']}) | Subtotal: {moeda(s['q'] * p_venda)}", ln=True)
            pdf.ln(5); pdf.set_font("Helvetica", "B", 14)
            pdf.cell(190, 10, f"TOTAL: {moeda(valor_total_real)}", ln=True)
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("Baixar PDF", pdf_bytes, f"orcamento_{nome_c}.pdf", "application/pdf")
        except: st.error("Erro no PDF. Checou o fpdf2?")
