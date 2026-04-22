import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Orçamento de Obras", page_icon="🏗️", layout="wide")

st.title("🏗️ Orçamento de Obras")
st.caption("Calcule o orçamento e gere o resumo para o WhatsApp.")

# Lista de serviços revisada (Linhas 11 até 39 aproximadamente)
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
    "Colocação de pia de fibra": {"unidade": "un", "preco_medio_es": 150.00, "materiais": [("Sifão",
