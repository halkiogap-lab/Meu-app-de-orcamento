import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="OT Construções ERP", layout="wide")

# Estilização Dark Modern
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #111; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS DE ETAPAS ---
ESTRUTURA_OBRA = {
    "Fundação & Infra": ["Locação/gabarito", "Escavação", "Sapatas", "Blocos", "Viga baldrame", "Impermeabilização"],
    "Estrutura & Alvenaria": ["Colunas", "Pilares", "Vigas", "Lajes", "Escadas estruturais"],
    "Instalações Brutas": ["Rede de esgoto", "Pontos de água", "Conduítes", "Quadros de energia"],
    "Cobertura": ["Telhados (Zinco/Sanduíche)", "Metalon", "Calhas/Rufos"],
    "Revestimento & Acabamento": ["Reboco técnico", "Contra-piso", "Gesso", "Porcelanatos", "Bancadas", "Rodapés"],
    "Finalização & Pintura": ["Massa corrida", "Pintura", "Texturas", "Louças", "Limpeza pós-obra"]
}

# --- LÓGICA DE PDF (CORREÇÃO DE BUGS DE SAÍDA) ---
def gerar_pdf_binario(cliente, preco_final, etapas_ativas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "OT CONSTRUÇÕES - PROPOSTA COMERCIAL", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Cliente: {cliente}", ln=True)
    pdf.cell(0, 10, f"Valor Total do Investimento: R$ {preco_final:,.2f}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Serviços Inclusos:", ln=True)
    pdf.set_font("Arial", size=10)
    for etapa in etapas_ativas:
        pdf.multi_cell(0, 7, f"- {etapa}")
        
    # Método seguro para evitar AttributeError em bytes
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE PRINCIPAL ---
st.title("🏗️ ERP OT Construções | Alto Padrão")

with st.sidebar:
    st.header("⚙️ Inteligência Financeira")
    margem = st.slider("Margem de Lucro (%)", 10, 100, 30) / 100
    st.divider()
    st.header("🚚 Logística")
    km = st.number_input("Distância (KM)", 0.0, 500.0, 20.0)
    combustivel = st.number_input("Custo KM (R$)", 0.0, 10.0, 2.80)
    custo_logistica = km * combustivel

tab1, tab2, tab3 = st.tabs(["📊 Monitor do Patrão", "📝 Gerador de Orçamento", "📲 Saída WhatsApp"])

with tab2:
    col_c1, col_c2 = st.columns(2)
    nome_cliente = col_c1.text_input("Nome do Cliente", "Residência de Alto Padrão")
    m2_obra = col_c2.number_input("Metragem da Obra (m²)", 50, 5000, 200)
    
    custos_etapas = {}
    etapas_selecionadas = []
    
    for etapa, itens in ESTRUTURA_OBRA.items():
        with st.expander(f"🛠️ {etapa}"):
            ativo = st.checkbox("Incluir esta etapa", key=f"check_{etapa}")
            if ativo:
                valor = st.number_input(f"Custo Mão de Obra ({etapa})", 0.0, 1000000.0, key=f"val_{etapa}")
                custos_etapas[etapa] = valor
                etapas_selecionadas.append(etapa)

    # Cálculos Internos
    custo_total_obra = sum(custos_etapas.values()) + custo_logistica
    preco_final_cliente = custo_total_obra * (1 + margem)
    lucro_liquido = preco_final_cliente - custo_total_obra
    # Estimativa: 0.6 dias por m2 para alto padrão
    dias_estimados = int(m2_obra * 0.6)

with tab1:
    st.subheader("Painel de Performance (Visão Gestor)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Faturamento Bruto", f"R$ {preco_final_cliente:,.2f}")
    m2.metric("Lucro Líquido (Livre)", f"R$ {lucro_liquido:,.2f}", delta=f"{margem*100:.0f}%")
    m3.metric("Prazo de Entrega", f"{dias_estimados} dias")

with tab3:
    st.subheader("Formatação para Cliente")
    texto_whatsapp = f"🏠 *ORÇAMENTO: OT CONSTRUÇÕES*\n\n"
    texto_whatsapp += f"Olá {nome_cliente}, segue proposta para sua obra:\n\n"
    for e in etapas_selecionadas:
        texto_whatsapp += f"✅ *{e}*\n"
    texto_whatsapp += f"\n💰 *Investimento Total:* R$ {preco_final_cliente:,.2f}\n"
    texto_whatsapp += f"⏳ *Prazo de Conclusão:* {dias_estimados} dias úteis\n\n_Qualidade e excelência em cada detalhe._"
    
    st.text_area("Copie para o WhatsApp", texto_whatsapp, height=300)
    
    # Botão de Exportação com correção de bug de bytes
    pdf_output = gerar_pdf_binario(nome_cliente, preco_final_cliente, etapas_selecionadas)
    st.download_button(
        label="📥 Baixar Orçamento PDF Profissional",
        data=pdf_output,
        file_name=f"Orcamento_OT_{nome_cliente}.pdf",
        mime="application/pdf"
    )
