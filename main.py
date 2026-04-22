import streamlit as st
from datetime import datetime

# Configuração básica
st.set_page_config(page_title="Orçamento de Obras", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento de Obras")
st.caption("Calcule o orçamento e gere o resumo para o WhatsApp.")

# LISTA DE SERVIÇOS BLINDADA (Sem erros de fechamento)
SERVICOS = {
    "Alvenaria": {"un": "m²", "p": 55.0, "mat": [("Tijolos", 25), ("Cimento", 0.35)]},
    "Reboco": {"un": "m²", "p": 35.0, "mat": [("Cimento", 0.20), ("Areia", 0.03)]},
    "Piso": {"un": "m²", "p": 45.0, "mat": [("Piso", 1.1), ("Argamassa", 0.08)]},
    "Porcelanato": {"un": "m²", "p": 65.0, "mat": [("Porcelanato", 1.1), ("Argamassa AC-III", 0.1)]},
    "Gesso": {"un": "m²", "p": 40.0, "mat": [("Gesso pó", 8.0)]},
    "Pintura Simples": {"un": "m²", "p": 35.0, "mat": [("Tinta", 0.1)]},
    "Pintura + Massa": {"un": "m²", "p": 60.0, "mat": [("Massa", 0.5), ("Tinta", 0.12)]},
    "Serralheria": {"un": "m²", "p": 180.0, "mat": [("Perfil", 2.5)]},
    "Hidráulica": {"un": "ponto", "p": 120.0, "mat": [("Tubo PVC", 3.0)]},
    "Elétrica": {"un": "ponto", "p": 120.0, "mat": [("Fio 2,5mm", 8.0)]},
    "Laje": {"un": "m²", "p": 90.0, "mat": [("Cimento", 0.4), ("Ferro", 7.0)]},
    "Contra piso": {"un": "m²", "p": 30.0, "mat": [("Cimento", 0.25)]},
    "Vigamento/Colunas": {"un": "m", "p": 150.0, "mat": [("Ferro CA-50", 9.0)]},
    "Sapata": {"un": "un", "p": 200.0, "mat": [("Cimento", 1.0), ("Ferro", 12.0)]},
    "Rejunte": {"un": "m²", "p": 12.0, "mat": [("Rejunte", 0.3)]},
    "Porta/Marco": {"un": "un", "p": 180.0, "mat": [("Espuma", 0.5)]},
    "Telhado Zinco": {"un": "m²", "p": 180.0, "mat": [("Telha zinco", 1.1)]},
    "Caixa d'água (Inst)": {"un": "un", "p": 250.0, "mat": [("Boia", 1.0)]},
    "Esgoto (Desentupir)": {"un": "serv", "p": 250.0, "mat": []},
    "Caixa Gordura (Limpar)": {"un": "serv", "p": 150.0, "mat": []},
    "Caixa d'água (Limpar)": {"un": "un", "p": 200.0, "mat": [("Cloro", 1.0)]},
    "Forro PVC": {"un": "m²", "p": 45.0, "mat": [("Régua PVC", 1.1)]},
    "Forro Gesso": {"un": "m²", "p": 55.0, "mat": [("Placa gesso", 1.1)]},
    "Pia Mármore": {"un": "un", "p": 250.0, "mat": [("Silicone", 1.0)]},
    "Pia Fibra": {"un": "un", "p": 150.0, "mat": [("Sifão", 1.0)]},
    "Box Banheiro": {"un": "un", "p": 180.0, "mat": [("Silicone", 1.0)]}
}

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CABEÇALHO ---
st.subheader("📋 Dados da Obra")
c1, c2 = st.columns(2)
nome_c = c1.text_input("Cliente")
obra_c = c2.text_input("Local")

# --- DISTÂNCIA E GASOLINA ---
st.divider()
st.subheader("⛽ Deslocamento")
g1, g2 = st.columns(2)
dist = g1.number_input("Distância Total (KM)", min_value=0.0, step=1.0, key="km_box")
p_km = g2.number_input("Valor por KM (R$)", min_value=0.0, value=2.50, key="val_km_box")
custo_viagem = dist * p_km
st.info(f"Custo de Viagem: {moeda(custo_viagem)}")

# --- SERVIÇOS ---
st.divider()
st.subheader("🛠️ Serviços")
final = []
total_mo = 0.0

for nome, info in SERVICOS.items():
    with st.expander(f"➕ {nome}"):
        col1, col2 = st.columns(2)
        qtd = col1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{nome}")
        prc = col2.number_input(f"Preço Unit. (R$)", value=info['p'], key=f"p_{nome}")
        
        if qtd > 0:
            sub = qtd * prc
            total_mo += sub
            mats = [f"{mn}: {(qtd * mf):.1f}" for mn, mf in info['mat']]
            final.append({"n": nome, "q": qtd, "u": info['un'], "t": sub, "m": mats})

# --- TOTAL ---
st.divider()
total_geral = total_mo + custo_viagem
st.header(f"Total: {moeda(total_geral)}")

# --- WHATSAPP ---
if final:
    txt = f"*ORÇAMENTO: {nome_c.upper() or 'CLIENTE'}*\n📍 {obra_c or 'Obra'}\n"
    txt += f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
    txt += "-"*15 + "\n"
    for s in final:
        txt += f"✅ *{s['n']}*: {s['q']} {s['u']} = {moeda(s['t'])}\n"
    txt += "-"*15 + "\n"
    if custo_viagem > 0:
        txt += f"🚚 Viagem: {moeda(custo_viagem)}\n"
    txt += f"💰 *TOTAL: {moeda(total_geral)}*"
    st.text_area("Copiar para WhatsApp:", value=txt, height=300)
    "Colocação de pia de fibra": {"unidade": "un", "preco_medio_es": 150.00, "materiais": [("Sifão",
