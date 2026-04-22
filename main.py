import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="OT Construções | ERP", layout="wide", initial_sidebar_state="expanded")

# Estilização Premium Dark
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stMetricValue"] { color: #00FFCC; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1E1E1E; border-radius: 5px; color: white; }
    .stExpander { background-color: #161B22; border: 1px solid #30363D; }
    </style>
""", unsafe_allow_html=True)

# --- UTILITÁRIOS ---
def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE PREÇOS (ALTO PADRÃO) ---
DB_SERVICOS = {
    "FUNDAÇÃO & INFRA": {
        "Locação e Gabarito": {"un": "m²", "p": 25.0},
        "Escavação Manual": {"un": "m³", "p": 180.0},
        "Viga Baldrame (Concretagem)": {"un": "m", "p": 120.0},
        "Impermeabilização Sika": {"un": "m²", "p": 45.0},
    },
    "ESTRUTURA & ALVENARIA": {
        "Alvenaria de Vedação": {"un": "m²", "p": 65.0},
        "Pilar / Viga (Mão de Obra)": {"un": "m", "p": 155.0},
        "Laje Maciça (Montagem)": {"un": "m²", "p": 95.0},
        "Escada Cascata (Estrutural)": {"un": "un", "p": 4500.0},
    },
    "REVESTIMENTO & ACABAMENTO": {
        "Reboco Técnico": {"un": "m²", "p": 45.0},
        "Porcelanato Grande Formato": {"un": "m²", "p": 120.0},
        "Bancada Esculpida": {"un": "m", "p": 650.0},
        "Rodapé Embutido": {"un": "m", "p": 35.0},
    },
    "PINTURA & FINALIZAÇÃO": {
        "Massa Corrida & Lixamento": {"un": "m²", "p": 40.0},
        "Pintura Premium (Toque de Seda)": {"un": "m²", "p": 35.0},
        "Limpeza Pós-Obra Técnica": {"un": "m²", "p": 25.0},
    }
}

# --- INTERFACE PRINCIPAL ---
st.title("🏗️ OT CONSTRUÇÕES - Intelligence ERP")

tab1, tab2, tab3 = st.tabs(["📊 MONITOR DO PATRÃO", "📝 GERADOR DE ORÇAMENTO", "⚙️ TABELA DE PREÇOS"])

# --- TABELA DE PREÇOS (CONFIGURAÇÃO) ---
with tab3:
    st.header("Configurações de Margem e Logística")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        margem_global = st.slider("Margem de Lucro OT (%)", 0, 200, 40)
        custo_km = st.number_input("Custo Logístico por KM (R$)", value=4.50)
    with col_c2:
        prod_diaria = st.number_input("Rendimento Equipe (m²/dia)", value=5.0)

# --- GERADOR DE ORÇAMENTO ---
with tab2:
    st.header("Dados do Cliente")
    c1, c2, c3 = st.columns([2, 2, 1])
    nome_cliente = c1.text_input("Nome do Cliente", placeholder="Ex: Dr. Roberto Silva")
    endereco = c2.text_input("Local da Obra")
    distancia = c3.number_input("Distância (KM)", min_value=0.0)

    st.subheader("Seleção de Serviços")
    itens_selecionados = []
    total_base_mao_obra = 0.0
    total_m2_obra = 0.0

    for cat, servs in DB_SERVICOS.items():
        with st.expander(f"📂 {cat}"):
            for s_nome, s_info in servs.items():
                col_1, col_2, col_3 = st.columns([3, 1, 1])
                col_1.write(f"**{s_nome}**")
                qtd = col_2.number_input(f"Qtd ({s_info['un']})", min_value=0.0, key=f"q_{s_nome}")
                # Preço base vem do DB mas pode ser editado
                preco_base = col_3.number_input(f"Preço Unitário", value=s_info['p'], key=f"p_{s_nome}")
                
                if qtd > 0:
                    total_base_mao_obra += (qtd * preco_base)
                    if s_info['un'] == "m²": total_m2_obra += qtd
                    itens_selecionados.append({"nome": s_nome, "qtd": qtd, "un": s_info['un'], "p_base": preco_base})

# --- MONITOR DO PATRÃO ---
with tab1:
    if not itens_selecionados:
        st.info("Aguardando seleção de itens no Gerador...")
    else:
        custo_logistica = distancia * custo_km
        valor_final_cliente = (total_base_mao_obra + custo_logistica) * (1 + margem_global/100)
        lucro_liquido = valor_final_cliente - total_base_mao_obra - custo_logistica
        dias_obra = math.ceil(total_m2_obra / prod_diaria) if total_m2_obra > 0 else 7

        st.subheader("Análise de Lucratividade")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("FATURAMENTO", moeda(valor_final_cliente))
        m2.metric("LUCRO OT", moeda(lucro_liquido), f"{margem_global}%")
        m3.metric("LOGÍSTICA", moeda(custo_logistica))
        m4.metric("CRONOGRAMA", f"{dias_obra} DIAS")

        st.divider()

        # Fator de diluição: Transforma custos internos em preço de venda por item
        fator = valor_final_cliente / total_base_mao_obra if total_base_mao_obra > 0 else 1
        
        # Formatação WhatsApp
        zap_texto = f"🏗️ *PROPOSTA OT CONSTRUÇÕES*\n"
        zap_texto += f"👤 *CLIENTE:* {nome_cliente.upper()}\n"
        zap_texto += f"📍 *LOCAL:* {endereco}\n\n"
        for item in itens_selecionados:
            p_venda = item['p_base'] * fator
            zap_texto += f"✅ *{item['nome']}*\n{item['qtd']} {item['un']} — {moeda(item['qtd']*p_venda)}\n\n"
        zap_texto += f"⏱️ *PRAZO:* {dias_obra} dias úteis\n"
        zap_texto += f"💰 *TOTAL:* {moeda(valor_final_cliente)}"
        
        st.text_area("Cópia para WhatsApp (Valores Diluídos)", value=zap_texto, height=300)

        # Geração de PDF (Correção de Bug de Saída)
        if st.button("📄 Exportar PDF Profissional"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(190, 10, "OT CONSTRUCOES - ORCAMENTO", ln=True, align='C')
            pdf.set_font("Arial", '', 10)
            pdf.cell(190, 10, f"Cliente: {nome_cliente} | Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(110, 10, " DESCRICAO", 1, 0, 'L', True)
            pdf.cell(30, 10, " QTD", 1, 0, 'C', True)
            pdf.cell(50, 10, " TOTAL", 1, 1, 'C', True)
            
            for item in itens_selecionados:
                p_venda = item['p_base'] * fator
                pdf.cell(110, 8, f" {item['nome']}", 1)
                pdf.cell(30, 8, f" {item['qtd']} {item['un']}", 1, 0, 'C')
                pdf.cell(50, 8, f" {moeda(item['qtd']*p_venda)}", 1, 1, 'R')
            
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, f"TOTAL: {moeda(valor_final_cliente)}", align='R')
            
            # Saída segura em bytes
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("Clique para Baixar", pdf_bytes, "Orcamento_OT.pdf", "application/pdf")
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
