import streamlit as st
from datetime import datetime

# Essa porra configura a página pra ficar larga e bonita
st.set_page_config(page_title="Orçamento de Obras", layout="wide")

st.title("🏗️ Orçamento de Obras")

# --- DADOS DO CLIENTE E VIAGEM ---
st.subheader("📋 Informações Básicas")
c1, c2 = st.columns(2)
nome_c = c1.text_input("Nome do Cliente", key="n_cliente")
obra_c = c2.text_input("Local da Obra", key="l_obra")

st.divider()

st.subheader("⛽ Deslocamento e Combustível")
g1, g2 = st.columns(2)
distancia = g1.number_input("Distância Total (Ida/Volta KM)", min_value=0.0, step=1.0, key="km_input")
valor_km = g2.number_input("Valor por KM (R$)", min_value=0.0, value=2.50, step=0.10, key="val_km_input")

custo_viagem = distancia * valor_km
st.warning(f"Custo total de deslocamento: R$ {custo_viagem:,.2f}")

st.divider()

# --- LISTA DE SERVIÇOS (REVISADA E TESTADA) ---
SERVICOS = {
    "Alvenaria": {"un": "m²", "p": 55.0},
    "Reboco": {"un": "m²", "p": 35.0},
    "Piso": {"un": "m²", "p": 45.0},
    "Porcelanato": {"un": "m²", "p": 65.0},
    "Gesso": {"un": "m²", "p": 40.0},
    "Pintura Simples": {"un": "m²", "p": 35.0},
    "Pintura + Massa": {"un": "m²", "p": 60.0},
    "Serralheria": {"un": "m²", "p": 180.0},
    "Hidráulica": {"un": "ponto", "p": 120.0},
    "Elétrica": {"un": "ponto", "p": 120.0},
    "Laje": {"un": "m²", "p": 90.0},
    "Contra piso": {"un": "m²", "p": 30.0},
    "Vigamento/Colunas": {"un": "m", "p": 150.0},
    "Sapata": {"un": "un", "p": 200.0},
    "Rejunte": {"un": "m²", "p": 12.0},
    "Porta/Marco": {"un": "un", "p": 180.0},
    "Telhado Zinco": {"un": "m²", "p": 180.0},
    "Caixa d'água (Inst)": {"un": "un", "p": 250.0},
    "Esgoto (Desentupir)": {"un": "serv", "p": 250.0},
    "Caixa Gordura (Limpar)": {"un": "serv", "p": 150.0},
    "Caixa d'água (Limpar)": {"un": "un", "p": 200.0},
    "Forro PVC": {"un": "m²", "p": 45.0},
    "Forro Gesso": {"un": "m²", "p": 55.0},
    "Pia Mármore": {"un": "un", "p": 250.0},
    "Pia Fibra": {"un": "un", "p": 150.0},
    "Box Banheiro": {"un": "un", "p": 180.0}
}

st.subheader("🛠️ Serviços e Mão de Obra")
itens_selecionados = []
total_servicos = 0.0

for nome, info in SERVICOS.items():
    with st.expander(f"➕ {nome}"):
        col1, col2 = st.columns(2)
        q = col1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{nome}")
        p = col2.number_input(f"Preço Unitário R$", value=float(info['p']), key=f"p_{nome}")
        
        if q > 0:
            sub = q * p
            total_servicos += sub
            itens_selecionados.append({"n": nome, "q": q, "u": info['un'], "t": sub})

# --- RESUMO FINAL ---
st.divider()
total_geral = total_servicos + custo_viagem

st.header(f"💰 TOTAL DO ORÇAMENTO: R$ {total_geral:,.2f}")

if itens_selecionados:
    st.subheader("📱 Resumo para WhatsApp")
    res = f"*ORÇAMENTO: {nome_c.upper() or 'CLIENTE'}*\n📍 Local: {obra_c or 'Obra'}\n📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
    res += "-"*25 + "\n"
    for i in itens_selecionados:
        res += f"✅ *{i['n']}*: {i['q']} {i['u']} = R$ {i['t']:,.2f}\n"
    res += "-"*25 + "\n"
    if custo_viagem > 0:
        res += f"🚚 Deslocamento: R$ {custo_viagem:,.2f}\n"
    res += f"💰 *TOTAL GERAL: R$ {total_geral:,.2f}*"
    
    st.text_area("Copia o texto abaixo:", value=res, height=300)
