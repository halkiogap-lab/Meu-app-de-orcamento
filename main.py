import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# Configuração de Profissional
st.set_page_config(page_title="Gestão de Obras PRO", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- LISTA DE SERVIÇOS ---
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
    "Bancada em Porcelanato": {"un": "m", "p": 350.0},
    "Rejunte": {"un": "m²", "p": 15.0},
    "--- DESENTUPIDORA / HIDRÁULICA ---": {"un": "-", "p": 0.0},
    "Desentupimento Vaso/Pia": {"un": "un", "p": 200.0},
    "Limpeza Caixa de Gordura": {"un": "un", "p": 200.0},
    "Ponto de Hidráulica": {"un": "ponto", "p": 140.0},
    "Ponto de Elétrica": {"un": "ponto", "p": 130.0},
}

st.title("🏗️ Sistema de Orçamento Estratégico")

# --- ABA 1: PAINEL DE CONTROLE (SÓ VOCÊ VÊ) ---
st.sidebar.header("⚒️ SEU PAINEL (PRIVADO)")
with st.sidebar:
    st.subheader("Custos de Logística")
    dist = st.number_input("Distância Total (KM)", min_value=0.0, step=1.0)
    p_km = st.number_input("R$ por KM (Combustível)", value=2.50)
    custo_viagem = dist * p_km
    
    st.divider()
    st.subheader("Sua Margem")
    margem = st.slider("Margem de Lucro (%)", 0, 100, 20)
    
    st.divider()
    st.subheader("Planejamento de Tempo")
    produtividade = st.number_input("Média de m² por dia", value=10.0)
    st.info("Cálculo baseado em 5 dias de trabalho por semana.")

# --- DADOS DO CLIENTE ---
c1, c2 = st.columns(2)
nome_c = c1.text_input("Nome do Cliente")
local_s = c2.text_input("Local do Serviço")

st.divider()

# --- SELEÇÃO DE SERVIÇOS ---
st.subheader("🛠️ Serviços Realizados")
selecionados = []
total_maodobra_liquida = 0.0
total_m2 = 0.0

idx = 0
for nome, info in SERVICOS.items():
    if info["un"] == "-":
        st.markdown(f"#### {nome}")
        continue
    
    with st.expander(f"➕ {nome}"):
        col1, col2 = st.columns(2)
        qtd = col1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{idx}")
        prc = col2.number_input(f"Preço p/ Cliente ({info['un']})", value=float(info['p']), key=f"p_{idx}")
        
        if qtd > 0:
            sub = qtd * prc
            total_maodobra_liquida += sub
            if info["un"] == "m²": total_m2 += qtd
            selecionados.append({"n": nome, "q": qtd, "u": info['un'], "p": prc, "t": sub})
    idx += 1

# --- CÁLCULOS INTERNOS ---
valor_bruto = total_maodobra_liquida + custo_viagem
valor_final_cliente = valor_bruto * (1 + margem/100)

# Cálculo de tempo
dias_necessarios = math.ceil(total_m2 / produtividade) if total_m2 > 0 else 1
semanas = math.ceil(dias_necessarios / 5)

# --- TELA DE RESUMO PRIVADA ---
st.divider()
col_res1, col_res2 = st.columns(2)

with col_res1:
    st.subheader("📊 Resumo para Você")
    st.write(f"**Custo Gasolina:** {moeda(custo_viagem)}")
    st.write(f"**Tempo Estimado:** {dias_necessarios} dias úteis")
    st.write(f"**Prazo em Semanas:** {semanas} semana(s) (5 dias/sem)")
    st.write(f"**Seu Lucro Real Est.:** {moeda(valor_final_cliente - total_maodobra_liquida - custo_viagem)}")

with col_res2:
    st.subheader("💰 Total para o Cliente")
    st.success(f"### {moeda(valor_final_cliente)}")

# --- O QUE VAI PARA O CLIENTE ---
if selecionados:
    st.divider()
    st.subheader("📄 Área de Envio (O que o cliente vê)")
    
    # Texto limpo para WhatsApp
    txt_cliente = f"*ORÇAMENTO: {nome_c.upper()}*\n📍 Local: {local_s}\n"
    txt_cliente += f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
    txt_cliente += "-"*25 + "\n"
    for s in selecionados:
        # Aqui a gente dilui a margem e o frete no preço unitário pra ele não ver separado
        fator_ajuste = valor_final_cliente / total_maodobra_liquida if total_maodobra_liquida > 0 else 1
        preco_ajustado = s['p'] * fator_ajuste
        txt_cliente += f"✅ *{s['n']}*: {s['q']} {s['u']} | Unit: {moeda(preco_ajustado)} = {moeda(s['q'] * preco_ajustado)}\n"
    
    txt_cliente += "-"*25 + "\n"
    txt_cliente += f"⏱️ *Prazo Estimado:* {dias_necessarios} dias úteis\n"
    txt_cliente += f"💰 *VALOR TOTAL: {moeda(valor_final_cliente)}*"
    txt_cliente += "\n\n_Obs: Material por conta do contratante._"

    st.text_area("Copia esse texto pro Zap (O cliente não vê seus custos!):", value=txt_cliente, height=250)

    if st.button("📥 Gerar PDF para o Cliente"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(190, 10, "PROPOSTA DE PRESTACAO DE SERVICOS", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12)
            pdf.ln(10)
            pdf.cell(190, 8, f"Cliente: {nome_c}", ln=True)
            pdf.cell(190, 8, f"Local: {local_s}", ln=True)
            pdf.cell(190, 8, f"Prazo: {dias_necessarios} dias uteis", ln=True)
            pdf.ln(5)
            pdf.cell(190, 0, "", "T", ln=True)
            pdf.ln(5)
            fator = valor_final_cliente / total_maodobra_liquida if total_maodobra_liquida > 0 else 1
            for s in selecionados:
                p_ajust = s['p'] * fator
                pdf.cell(190, 8, f"- {s['n']}: {s['q']} {s['u']} x {moeda(p_ajust)} = {moeda(s['q'] * p_ajust)}", ln=True)
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(190, 10, f"TOTAL: {moeda(valor_final_cliente)}", ln=True)
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("Baixar PDF Profissional", pdf_bytes, f"orcamento_{nome_c}.pdf", "application/pdf")
        except:
            st.error("Erro no PDF. Checou o fpdf2?")
