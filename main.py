import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Orçamento de Obras", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento de Obras")
st.caption("Calcule o orçamento da sua obra e gere um resumo pronto para o WhatsApp.")

# Lista completa de serviços sem erros de fechamento
SERVICOS = {
    "Alvenaria": {
        "unidade": "m²",
        "preco_medio_es": 55.00,
        "materiais": [("Tijolos / Blocos", 25, "un"), ("Cimento", 0.35, "saco 50kg"), ("Areia", 0.05, "m³")],
    },
    "Reboco": {
        "unidade": "m²",
        "preco_medio_es": 35.00,
        "materiais": [("Cimento", 0.20, "saco 50kg"), ("Areia", 0.03, "m³"), ("Cal", 0.15, "kg")],
    },
    "Piso": {
        "unidade": "m²",
        "preco_medio_es": 45.00,
        "materiais": [("Piso cerâmico", 1.10, "m²"), ("Argamassa AC-II", 0.08, "saco 20kg"), ("Rejunte", 0.30, "kg")],
    },
    "Porcelanato": {
        "unidade": "m²",
        "preco_medio_es": 65.00,
        "materiais": [("Porcelanato", 1.10, "m²"), ("Argamassa AC-III", 0.10, "saco 20kg"), ("Rejunte", 0.30, "kg"), ("Espaçadores", 5.0, "un")],
    },
    "Gesso": {
        "unidade": "m²",
        "preco_medio_es": 40.00,
        "materiais": [("Gesso em pó", 8.0, "kg"), ("Cantoneiras / fitas", 0.10, "un")],
    },
    "Pintura Simples": {
        "unidade": "m²",
        "preco_medio_es": 35.00,
        "materiais": [("Tinta látex", 0.10, "L"), ("Lixa", 0.05, "un")],
    },
    "Pintura com Emassamento": {
        "unidade": "m²",
        "preco_medio_es": 60.00,
        "materiais": [("Massa corrida", 0.50, "kg"), ("Tinta látex", 0.12, "L"), ("Lixa", 0.10, "un"), ("Selador", 0.08, "L")],
    },
    "Serralheria": {
        "unidade": "m²",
        "preco_medio_es": 180.00,
        "materiais": [("Perfil metálico", 2.5, "kg"), ("Solda / eletrodo", 0.10, "kg"), ("Tinta antiferrugem", 0.08, "L")],
    },
    "Hidráulica": {
        "unidade": "ponto",
        "preco_medio_es": 120.00,
        "materiais": [("Tubo PVC", 3.0, "m"), ("Conexões", 4.0, "un"), ("Cola / veda-rosca", 0.10, "un")],
    },
    "Elétrica": {
        "unidade": "ponto",
        "preco_medio_es": 120.00,
        "materiais": [("Fio 2,5mm", 8.0, "m"), ("Eletroduto", 3.0, "m"), ("Caixa 4x2", 1.0, "un"), ("Tomada / interruptor", 1.0, "un")],
    },
    "Laje": {
        "unidade": "m²",
        "preco_medio_es": 90.00,
        "materiais": [("Cimento", 0.40, "saco 50kg"), ("Areia", 0.04, "m³"), ("Brita", 0.05, "m³"), ("Ferro CA-50", 7.0, "kg"), ("Lajota / EPS", 6.0, "un")],
    },
    "Contra piso": {
        "unidade": "m²",
        "preco_medio_es": 30.00,
        "materiais": [("Cimento", 0.25, "saco 50kg"), ("Areia", 0.04, "m³")],
    },
    "Vigamento / Colunas": {
        "unidade": "m",
        "preco_medio_es": 150.00,
        "materiais": [("Ferro CA-50", 9.0, "kg"), ("Estribos", 1.5, "kg"), ("Cimento", 0.20, "saco 50kg"), ("Areia", 0.02, "m³"), ("Brita", 0.03, "m³"), ("Madeira para forma", 1.5, "m²")],
    },
    "Sapata": {
        "unidade": "un",
        "preco_medio_es": 200.00,
        "materiais": [("Ferro CA-50", 12.0, "kg"), ("Cimento", 1.0, "saco 50kg"), ("Areia", 0.10, "m³"), ("Brita", 0.15, "m³")],
    },
    "Rejunte": {
        "unidade": "m²",
        "preco_medio_es": 12.00,
        "materiais": [("Rejunte", 0.30, "kg")],
    },
    "Colocação de porta / marco": {
        "unidade": "un",
        "preco_medio_es": 180.00,
        "materiais": [("Porta com marco", 1.0, "un"), ("Dobradiças", 3.0, "un"), ("Fechadura", 1.0, "un"), ("Espuma de poliuretano", 0.5, "un")],
    },
    "Telhado de zinco + estrutura de ferro": {
        "unidade": "m²",
        "preco_medio_es": 180.00,
        "materiais": [("Telha de zinco", 1.10, "m²"), ("Perfil de ferro", 4.0, "kg"), ("Parafusos / ganchos", 6.0, "un"), ("Tinta antiferrugem", 0.10, "L")],
    },
    "Instalação de caixa d'água": {
        "unidade": "un",
        "preco_medio_es": 250.00,
        "materiais": [("Torneira boia", 1.0, "un"), ("Registros", 2.0, "un"), ("Conexões", 6.0, "un"), ("Tubo PVC", 6.0, "m")],
    },
    "Desentupimento de esgoto": {
        "unidade": "serviço",
        "preco_medio_es": 250.00,
        "materiais": [],
    },
    "Limpeza de caixa de gordura": {
        "unidade": "serviço",
        "preco_medio_es": 150.00,
        "materiais": [],
    },
    "Desentupimento de pia": {
        "unidade": "serviço",
        "preco_medio_es": 120.00,
        "materiais": [],
    },
    "Limpeza de caixa d'água": {
        "unidade": "un",
        "preco_medio_es": 200.00,
        "materiais": [("Cloro / desinfetante", 1.0, "L")],
    },
    "Instalação de forro PVC": {
        "unidade": "m²",
        "preco_medio_es": 45.00,
        "mater
