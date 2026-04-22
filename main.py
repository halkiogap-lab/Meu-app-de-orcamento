import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Orçamento de Obras", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento de Obras")
st.caption("Calcule o orçamento da sua obra e gere um resumo pronto para o WhatsApp.")

# Lista de serviços completa e original
SERVICOS = {
    "Alvenaria": {"unidade": "m²", "preco_medio_es": 55.00, "materiais": [("Tijolos", 25, "un"), ("Cimento", 0.35, "saco"), ("Areia", 0.05, "m³")]},
    "Reboco": {"unidade": "m²", "preco_medio_es": 35.00, "materiais": [("Cimento", 0.20, "saco"), ("Areia", 0.03, "m³")]},
    "Piso": {"unidade": "m²", "preco_medio_es": 45.00, "materiais": [("Piso", 1.10, "m²"), ("Argamassa", 0.08, "saco")]},
    "Porcelanato": {"unidade": "m²", "preco_medio_es": 65.00, "materiais": [("Porcelanato", 1.10, "m²"), ("Argamassa AC-III", 0.10, "saco")]},
    "Gesso": {"unidade": "m²", "preco_medio_es": 40.00, "materiais": [("Gesso pó", 8.0, "kg")]},
    "Pintura Simples": {"unidade": "m²", "preco_medio_es": 35.00, "materiais": [("Tinta", 0.10, "L")]},
    "Pintura com Emassamento": {"unidade": "m²", "preco_medio_es": 60.00, "materiais": [("Massa", 0.50, "kg"), ("Tinta", 0.12, "L")]},
    "Serralheria": {"unidade": "m²", "preco_medio_es": 180.00, "materiais": [("Perfil", 2.5, "kg")]},
    "Hidráulica": {"unidade": "ponto", "preco_medio_es": 120.00, "materiais": [("Tubo PVC", 3.0, "m")]},
    "Elétrica": {"unidade": "ponto", "preco_medio_es": 120.00, "materiais": [("Fio 2,5mm", 8.0, "m")]},
    "Laje": {"unidade": "m²", "preco_medio_es": 90.00, "materiais": [("Cimento", 0.40, "saco"), ("Ferro", 7.0, "kg")]},
    "Contra piso": {"unidade": "m²", "preco_medio_es": 30.00, "materiais": [("Cimento", 0.25, "saco")]},
    "Vigamento / Colunas": {"unidade": "m", "preco_medio_es": 150.00, "materiais": [("Ferro CA-50", 9.0, "kg")]},
    "Sapata": {"unidade": "un", "preco_medio_es": 200.00, "materiais": [("Cimento", 1.0, "saco"), ("Ferro", 12.0, "kg")]},
    "Rejunte": {"unidade": "m²", "preco_medio_es": 12.00, "materiais": [("Rejunte", 0.30, "kg")]},
    "Colocação de porta / marco": {"unidade": "un", "preco_medio_es": 180.00, "materiais": [("Espuma", 0.5, "un")]},
    "Telhado zinco + estrutura ferro": {"unidade": "m²", "preco_medio_es": 180.00, "materiais": [("Telha zinco", 1.10, "m²")]},
    "Instalação de caixa d'água": {"unidade": "un", "preco_medio_es": 250.00, "materiais": [("Boia", 1.0, "un")]},
    "Desentupimento de esgoto": {"unidade": "serviço", "preco_medio_es": 250.00, "materiais": []},
    "Limpeza de caixa de gordura": {"unidade": "serviço", "preco_medio_es": 150.00, "materiais": []},
    "Desentupimento de pia": {"unidade": "serviço", "preco_medio_es": 120.00, "materiais": []},
    "Limpeza de caixa d'água": {"unidade": "un", "preco_medio_es": 200.00, "materiais": [("Cloro", 1.0, "L")]},
    "Instalação de forro PVC": {"unidade": "m²", "preco_medio_es": 45.00, "materiais": [("Régua PVC", 1.10, "m²")]},
    "Instalação de forro de gesso": {"unidade": "m²", "preco_medio_es": 55.00, "materiais": [("Placa gesso", 1.10, "m²")]},
    "Colocação de pia de mármore": {"unidade": "un", "preco_medio_es": 250.00, "materiais": [("Silicone", 1.0, "un")]},
    "Colocação de pia de fibra": {"unidade": "un", "preco_medio_es": 150.00, "materiais": [("Sifão", 1.0, "un")]},
    "Colocação de box de banheiro": {"unidade": "un", "preco_medio_es": 180.00, "materiais": [("Silicone", 1.0, "un")]},
}

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# BARRA LATERAL
with st.sidebar:
    st.header("📋 Dados do Cliente")
    nome_c = st.text_input("Nome do Cliente", key="nome_cliente")
    obra_c = st.text_input("Endereço da Obra", key="endereco_obra")
    
    st.divider()
    st.header("🚚 Deslocamento")
    # Agora você pode definir a distância e o valor do KM
    km_total = st.number_input("Distância Total (KM)", min_value=0.0, step=1.0, key="km_input")
    valor_por_km = st.number_input("Valor por KM (R$)", min_value=0.0, value=2.50, step=0.10, key="val_km_input")
    
    custo_viagem = km_total * valor_por_km
    st.metric("Total Deslocamento", moeda(custo_viagem))

# ÁREA PRINCIPAL
st.subheader("🛠️ Seleção de Serviços")
selecionados = []
total_mo = 0.0

for s_nome, s_info in SERVICOS.items():
    with st.expander(f"➕ {s_nome} ({s_info['unidade']})"):
        col1, col2 = st.columns(2)
        q = col1.number_input(f"Qtd", min_value=0.0, key=f"q_{s_nome}")
        p = col2.number_input(f"Preço (R$)", value=float(s_info['preco_medio_es']), key=f"p_{s_nome}")
        
        if q > 0:
            subtotal = q * p
            total_mo += subtotal
            
            # Cálculo de materiais
            mats_lista = []
            for m_n, m_f, m_u in s_info['materiais']:
                mats_lista.append(f"{m_n}: {(q * m_f):.2f} {m_u}")
            
            selecionados.append({
                "nome": s_nome,
                "qtd": q,
                "un": s_info['unidade'],
                "preco": p,
                "total": subtotal,
                "materiais": mats_lista
            })

# RESUMO FINANCEIRO
st.divider()
total_geral = total_mo + custo_viagem

c1, c2, c3 = st.columns(3)
c1.metric("Mão de Obra", moeda(total_mo))
c2.metric("Viagem", moeda(custo_viagem))
c3.metric("TOTAL GERAL", moeda(total_geral))

# TEXTO WHATSAPP
if selecionados:
    st.subheader("📱 Resumo para WhatsApp")
    texto = f"*ORÇAMENTO: {nome_c.upper() or 'CLIENTE'}*\n"
    texto += f"📍 Obra: {obra_c or 'Não informada'}\n"
    texto += f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n"
    texto += "\n" + "-"*20 + "\n"
    
    for r in selecionados:
        texto += f"✅ *{r['nome']}*\n"
        texto += f"Qtd: {r['qtd']} {r['un']} | Total: {moeda(r['total'])}\n"
        if r['materiais']:
            texto += "_Material sugerido: " + ", ".join(r['materiais']) + "_\n\n"
    
    texto += "-"*20 + "\n"
    if custo_viagem > 0:
        texto += f"🚚 Deslocamento: {moeda(custo_viagem)}\n"
    texto += f"💰 *TOTAL DO ORÇAMENTO: {moeda(total_geral)}*"
    texto += "\n\n_Obs: Mão de obra. Material por conta do cliente._"
    
    st.text_area("Selecione e copie:", value=texto, height=400)
