import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Orçamento de Obras ES", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento Profissional - Mestre das Obras")
st.caption("Cálculo de mão de obra e estimativa de materiais (Padrão Espírito Santo)")

# Banco de dados de serviços e materiais
SERVICOS = {
    "Alvenaria": {"un": "m²", "preco": 55.0, "mat": "🧱 25 tijolos, 0.35 sacos cimento, 0.05m³ areia por m²"},
    "Reboco": {"un": "m²", "preco": 35.0, "mat": "⚪ 0.20 sacos cimento, 0.03m³ areia por m²"},
    "Piso": {"un": "m²", "preco": 45.0, "mat": "📐 1.1m² piso, 0.25 sacos argamassa por m²"},
    "Porcelanato": {"un": "m²", "preco": 65.0, "mat": "💎 1.1m² porcelanato, 0.30 sacos argamassa AC3 por m²"},
    "Gesso": {"un": "m²", "preco": 40.0, "mat": "⬜ 3 placas (60x60), 1kg gesso pó por m²"},
    "Pintura Simples": {"un": "m²", "preco": 35.0, "mat": "🎨 0.1L tinta, lixa por m²"},
    "Pintura c/ Emassamento": {"un": "m²", "preco": 60.0, "mat": "🎨 0.5kg massa, 0.12L tinta por m²"},
    "Serralheria": {"un": "m²", "preco": 180.0, "mat": "🛠️ Perfil metálico e eletrodo conforme projeto"},
    "Hidráulica": {"un": "ponto", "preco": 120.0, "mat": "🚰 Tubos e conexões por ponto"},
    "Elétrica": {"un": "ponto", "preco": 120.0, "mat": "⚡ Fios, conduítes e caixinhas por ponto"},
    "Laje": {"un": "m²", "preco": 90.0, "mat": "🏗️ Cimento, areia, brita, ferro e lajota/EPS"},
    "Contra piso": {"un": "m²", "preco": 30.0, "mat": "📏 0.25 sacos cimento, 0.04m³ areia por m²"},
    "Vigamento / Colunas": {"un": "m", "preco": 150.0, "mat": "⛓️ Ferro CA-50, estribos e concreto"},
    "Sapata": {"un": "un", "preco": 200.0, "mat": "🧱 Ferro, 1 saco cimento, areia e brita por unidade"},
    "Rejunte": {"un": "m²", "preco": 12.0, "mat": "🧴 0.3kg rejunte por m²"},
    "Porta/Marco": {"un": "un", "preco": 150.0, "mat": "🚪 Espuma expansiva e parafusos"}
}

with st.sidebar:
    st.header("Dados do Cliente")
    nome = st.text_input("Nome do Cliente")
    distancia = st.number_input("Distância da Obra (KM)", min_value=0.0)

st.subheader("Selecione os Serviços")
selecionados = []

for serv, dados in SERVICOS.items():
    with st.expander(f"➕ {serv} (R$ {dados['preco']}/{dados['un']})"):
        col1, col2 = st.columns(2)
        with col1:
            qtd = st.number_input(f"Quantidade ({dados['un']})", min_value=0.0, key=f"q_{serv}")
        with col2:
            pr = st.number_input(f"Preço Unitário R$", value=dados['preco'], key=f"p_{serv}")
        if qtd > 0:
            selecionados.append({"nome": serv, "qtd": qtd, "valor": pr, "total": qtd * pr, "mat": dados['mat']})

if st.button("📊 GERAR ORÇAMENTO PARA WHATSAPP"):
    if not nome or not selecionados:
        st.error("Preencha o nome e selecione ao menos um serviço!")
    else:
        st.balloons()
        total_mo = sum(s['total'] for s in selecionados)
        custo_km = distancia * 3.0 
        total_geral = total_mo + custo_km
        
        texto = f"*ORÇAMENTO: {nome.upper()}*\n"
        texto += f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        
        for s in selecionados:
            texto += f"✅ *{s['nome']}*: {s['qtd']} {SERVICOS[s['nome']]['un']} x R${s['valor']:.2f} = *R${s['total']:.2f}*\n"
            texto += f"   _Est. Material: {s['mat']}_\n\n"
        
        if custo_km > 0:
            texto += f"🚚 *Deslocamento*: R${custo_km:.2f}\n"
        
        texto += f"\n💰 *TOTAL MÃO DE OBRA: R${total_geral:.2f}*"
        texto += "\n\n_Obs: Valores referentes apenas à execução._"
        
        st.success("Tudo pronto! Copie o texto abaixo:")
        st.text_area("Texto para copiar:", value=texto, height=400)
