import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF
import math
import pandas as pd

# Configuração de Alta Performance
st.set_page_config(page_title="ERP - Gestão de Obras & Manutenção", layout="wide", initial_sidebar_state="expanded")

# --- FUNÇÕES DE UTILITÁRIO ---
def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS DE SERVIÇOS (TOTALMENTE COMPLETO) ---
DB_SERVICOS = {
    "ESTRUTURA": {
        "Sapata / Fundação": {"un": "un", "p": 250.0},
        "Vigamento / Colunas": {"un": "m", "p": 150.0},
        "Laje (Batida)": {"un": "m²", "p": 95.0},
        "Escada em Metalon": {"un": "un", "p": 1200.0},
        "Alvenaria (Tijolo/Bloco)": {"un": "m²", "p": 60.0},
        "Contra-piso": {"un": "m²", "p": 35.0},
    },
    "ACABAMENTO FINO": {
        "Reboco": {"un": "m²", "p": 40.0},
        "Piso Cerâmico": {"un": "m²", "p": 50.0},
        "Porcelanato (Chão/Parede)": {"un": "m²", "p": 85.0},
        "Bancada em Porcelanato (Corte/Inst)": {"un": "m", "p": 450.0},
        "Rejunte Epóxi/Comum": {"un": "m²", "p": 20.0},
        "Gesso Liso / Forro PVC": {"un": "m²", "p": 55.0},
        "Instalação de Rodapé": {"un": "m", "p": 15.0},
    },
    "DESENTUPIDORA & HIDRÁULICA": {
        "Desentupimento Vaso Sanitário": {"un": "un", "p": 280.0},
        "Desentupimento Esgoto (Rede Principal)": {"un": "m", "p": 130.0},
        "Desentupimento Pia / Ralo": {"un": "un", "p": 160.0},
        "Limpeza de Caixa de Gordura": {"un": "un", "p": 220.0},
        "Limpeza de Caixa d'água": {"un": "un", "p": 300.0},
        "Hidrojateamento Técnico": {"un": "serv", "p": 500.0},
        "Ponto de Hidráulica / Esgoto": {"un": "ponto", "p": 150.0},
    },
    "ELÉTRICA & PINTURA": {
        "Ponto de Elétrica": {"un": "ponto", "p": 135.0},
        "Instalação de Quadro Geral": {"un": "un", "p": 450.0},
        "Pintura Simples (Rolo)": {"un": "m²", "p": 35.0},
        "Pintura com Massa Corrida": {"un": "m²", "p": 70.0},
        "Aplicação de Textura / Grafiato": {"un": "m²", "p": 45.0},
    },
    "COBERTURA": {
        "Telhado Zinco / Telha": {"un": "m²", "p": 190.0},
        "Instalação de Calhas": {"un": "m", "p": 50.0},
        "Impermeabilização de Laje": {"un": "m²", "p": 65.0},
    }
}

# --- INTERFACE PRINCIPAL ---
st.title("🏢 Painel Corporativo de Engenharia e Manutenção")
st.markdown("---")

# Múltiplos Monitores (Abas)
tab1, tab2, tab3 = st.tabs(["📊 MONITOR DO PATRÃO", "📝 GERADOR DE ORÇAMENTO", "⚙️ AJUSTE DE TABELA"])

# --- MONITOR 3: AJUSTE DE TABELA (Configuração) ---
with tab3:
    st.header("Configurações Globais da Empresa")
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        margem_global = st.slider("Margem de Lucro Desejada (%)", 0, 150, 30)
        custo_km = st.number_input("Custo Operacional por KM (R$)", value=3.20)
    with col_cfg2:
        prod_diaria = st.number_input("Capacidade de Execução (m²/dia)", value=8.0)
        dias_semana = st.selectbox("Dias de Trabalho por Semana", [5, 6, 7])

# --- MONITOR 2: GERADOR DE ORÇAMENTO ---
with tab2:
    st.header("Novo Orçamento")
    c1, c2 = st.columns(2)
    cliente = c1.text_input("Nome Completo do Cliente / Empresa")
    endereco = c2.text_input("Endereço da Obra")
    distancia = st.number_input("Distância Total para Logística (KM)", min_value=0.0)

    st.subheader("Seleção de Itens da Obra")
    itens_selecionados = []
    total_base_obra = 0.0
    total_m2_obra = 0.0

    for cat, servs in DB_SERVICOS.items():
        with st.expander(f"📂 CATEGORIA: {cat}"):
            for s_nome, s_info in servs.items():
                col_s1, col_s2, col_s3 = st.columns([3, 1, 1])
                col_s1.write(f"**{s_nome}**")
                qtd = col_s2.number_input(f"Qtd ({s_info['un']})", min_value=0.0, key=f"inp_{s_nome}")
                preco_manual = col_s3.number_input(f"Preço Base (R$)", value=s_info['p'], key=f"prc_{s_nome}")
                
                if qtd > 0:
                    sub_base = qtd * preco_manual
                    total_base_obra += sub_base
                    if s_info['un'] == "m²": total_m2_obra += qtd
                    itens_selecionados.append({"nome": s_nome, "qtd": qtd, "un": s_info['un'], "p_base": preco_manual})

# --- MONITOR 1: MONITOR DO PATRÃO (RESULTADOS) ---
with tab1:
    if not itens_selecionados:
        st.warning("Selecione serviços no 'Gerador de Orçamento' para ver a análise.")
    else:
        # Cálculos de Inteligência de Negócio
        custo_logistica = distancia * custo_km
        valor_com_margem = (total_base_obra + custo_logistica) * (1 + margem_global/100)
        lucro_liquido = valor_com_margem - total_base_obra - custo_logistica
        
        # Tempo
        dias_uteis = math.ceil(total_m2_obra / prod_diaria) if total_m2_obra > 0 else 1
        data_final = datetime.now() + timedelta(days=math.ceil(dias_uteis * (7/dias_semana)))

        st.header("Dashboard de Lucratividade")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Faturamento Bruto", moeda(valor_com_margem))
        m2.metric("Lucro Estimado", moeda(lucro_liquido), f"{margem_global}%")
        m3.metric("Custo Logística", moeda(custo_logistica))
        m4.metric("Prazo de Entrega", f"{dias_uteis} dias")

        st.divider()
        st.subheader("Visualização para o Cliente (O que ele recebe)")
        
        # Gerar o texto diluído
        fator_diluicao = valor_com_margem / total_base_obra if total_base_obra > 0 else 1
        
        txt_zap = f"🏠 *PROPOSTA TÉCNICA - {cliente.upper()}*\n"
        txt_zap += f"📍 *LOCAL:* {endereco}\n"
        txt_zap += f"📅 *DATA:* {datetime.now().strftime('%d/%m/%Y')}\n"
        txt_zap += "─"*20 + "\n"
        
        for item in itens_selecionados:
            p_venda = item['p_base'] * fator_diluicao
            txt_zap += f"🔹 *{item['nome']}*\n   {item['qtd']} {item['un']} | Unit: {moeda(p_venda)} | Total: {moeda(item['qtd'] * p_venda)}\n\n"
        
        txt_zap += "─"*20 + "\n"
        txt_zap += f"⏱️ *PRAZO DE EXECUÇÃO:* {dias_uteis} dias úteis\n"
        txt_zap += f"💰 *INVESTIMENTO TOTAL: {moeda(valor_com_margem)}*\n"
        txt_zap += "─"*20 + "\n"
        txt_zap += "⚠️ _Nota: Valores incluem mão de obra e equipamentos. Materiais básicos por conta do contratante._"

        st.text_area("Texto para WhatsApp (Profissional e Diluído)", value=txt_zap, height=350)

        if st.button("📄 Gerar PDF de Alta Qualidade"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", "B", 18)
                pdf.cell(190, 15, "ORCAMENTO DE PRESTACAO DE SERVICOS", ln=True, align="C")
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(190, 10, f"CLIENTE: {cliente} | DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align="C")
                pdf.ln(10)
                
                # Tabela no PDF
                pdf.set_fill_color(240, 240, 240)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(100, 10, " DESCRICAO DO SERVICO", 1, 0, "L", True)
                pdf.cell(30, 10, " QTD", 1, 0, "C", True)
                pdf.cell(60, 10, " TOTAL ITEM", 1, 1, "C", True)
                
                pdf.set_font("Helvetica", "", 10)
                for item in itens_selecionados:
                    p_venda = item['p_base'] * fator_diluicao
                    pdf.cell(100, 8, f" {item['nome']}", 1)
                    pdf.cell(30, 8, f" {item['qtd']} {item['un']}", 1, 0, "C")
                    pdf.cell(60, 8, f" {moeda(item['qtd'] * p_venda)}", 1, 1, "R")
                
                pdf.ln(10)
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(190, 10, f"VALOR TOTAL DO INVESTIMENTO: {moeda(valor_com_margem)}", ln=True, align="R")
                pdf.set_font("Helvetica", "I", 10)
                pdf.cell(190, 10, f"Prazo estimado de entrega: {dias_uteis} dias uteis.", ln=True, align="R")
                
                st.download_button("Baixar Proposta em PDF", pdf.output(dest='S').encode('latin-1', 'ignore'), f"Proposta_{cliente}.pdf", "application/pdf")
            except Exception as e:
                st.error(f"Erro ao processar PDF: {e}")
