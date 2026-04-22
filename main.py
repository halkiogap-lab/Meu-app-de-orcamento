import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Orçamento de Obras", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento de Obras")
st.caption("Calcule o orçamento da sua obra e gere um resumo pronto para o WhatsApp.")

# Sua lista completa de serviços (SEM CORTES)
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
    "Colocação de box de banheiro": {"unidade": "un", "preco_medio_es": 180.00, "materiais": [("Silicone", 1.0, "un")]}
}

# Funções de ajuda
def moeda(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Lógica da Barra Lateral
with st.sidebar:
    st.header("Dados do Cliente")
    nome_c = st.text_input("Nome")
    obra_c = st.text_input("Obra")
    dist = st.number_input("Distância (KM)", min_value=0.0)
    valor_viagem = dist * 2.50
    st.metric("Deslocamento", moeda(valor_viagem))

# Lógica dos Serviços
st.subheader("Serviços Executados")
selecionados = []
total_serv = 0.0

# O segredo está no 'key' único dentro do loop
for s_nome, s_info in SERVICOS.items():
    with st.expander(f"➕ {s_nome}"):
        col1, col2 = st.columns(2)
        # Chaves dinâmicas para o Streamlit não bugar (ex: q_Alvenaria)
        qtd = col1.number_input(f"Quantidade ({s_info['unidade']})", min_value=0.0, key=f"q_{s_nome}")
        prc = col2.number_input(f"Preço Unitário (R$)", value=float(s_info['preco_medio_es']), key=f"p_{s_nome}")
        
        if qtd > 0:
            sub = qtd * prc
            total_serv += sub
            selecionados.append({"nome": s_nome, "q": qtd, "un": s_info['unidade'], "p": prc, "t": sub})

# Totais
total_geral = total_serv + valor_viagem
st.divider()
st.subheader(f"Total Geral: {moeda(total_geral)}")

# Gerador de Texto para WhatsApp
if selecionados:
    resumo = f"*ORÇAMENTO: {nome_c.upper() or 'CLIENTE'}*\n📍 {obra_c or 'Obra'}\n"
    resumo += f"📅 {datetime.now().strftime('%d/%m/%Y')}\n\n"
    for item in selecionados:
        resumo += f"✅ *{item['nome']}*: {item['q']} {item['un']} x {moeda(item['p'])} = *{moeda(item['t'])}*\n"
    resumo += f"\n🚚 Deslocamento: {moeda(valor_viagem)}"
    resumo += f"\n💰 *TOTAL: {moeda(total_geral)}*"
    
    st.text_area("Copie para o WhatsApp:", value=resumo, height=300)
