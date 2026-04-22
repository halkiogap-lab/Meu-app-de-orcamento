import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF
import math

# Configuração Profissional
st.set_page_config(page_title="ERP - Gestão de Obras", layout="wide", initial_sidebar_state="expanded")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS DE SERVIÇOS ---
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

st.title("🏢 Painel Corporativo de Engenharia")

tab1, tab2, tab3 = st.tabs(["📊 MONITOR DO PATRÃO", "📝 GERADOR DE ORÇAMENTO", "⚙️ AJUSTE DE TABELA"])

with tab3:
    st.header("Configurações Globais")
    margem_global = st.slider("Margem de Lucro (%)", 0, 150, 30)
    custo_km = st.number_input("Custo Operacional por KM", value=3.20)
    prod_diaria = st.number_input("Rendimento Diário (m²)", value=10.0)

with tab2:
    st.header("Entrada de Dados")
    c1, c2 = st.columns(2)
    cliente = c1.text_input("Nome do Cliente")
    endereco = c2.text_input("Local da Obra")
    distancia = st.number_input("Distância para Logística (KM)", min_value=0.0)

    itens_selecionados = []
    total_base_pura = 0.0
    total_m2_obra = 0.0

    idx = 0
    for cat, servs in DB_SERVICOS.items():
        with st.expander(f"📂 CATEGORIA: {cat}"):
            for s_nome, s_info in servs.items():
                st.markdown(f"**🔹 {s_nome}**")
                col_s1, col_s2 = st.columns(2)
                qtd = col_s1.number_input(f"Quantidade ({s_info['un']})", min_value=0.0, key=f"q_{idx}")
                p_base = col_s2.number_input(f"Valor Unitário Base (R$)", value=float(s_info['p']), key=f"p_{idx}")
                
                if qtd > 0:
                    total_base_pura += (qtd * p_base)
                    if s_info['un'] == "m²": total_m2_obra += qtd
                    itens_selecionados.append({"nome": s_nome, "qtd": qtd, "un": s_info['un'], "p_unit": p_base})
                idx += 1
                st.divider()

with tab1:
    if not itens_selecionados:
        st.warning("Selecione os serviços na aba ao lado.")
    else:
        custo_log = distancia * custo_km
        valor_final = (total_base_pura + custo_log) * (1 + margem_global/100)
        fator = valor_final / total_base_pura if total_base_pura > 0 else 1
        prazo = math.ceil(total_m2_obra / prod_diaria) if total_m2_obra > 0 else 1

        st.header("Dashboard de Gestão")
        m1, m2 = st.columns(2)
        m1.metric("Valor p/ Cliente", moeda(valor_final))
        m2.metric("Seu Lucro Real", moeda(valor_final - total_base_pura - custo_log))
        
        st.divider()
        st.subheader("Visualização para o Cliente")
        
        nota_tecnica = "⚠️ *Nota técnica: Os valores apresentados compreendem exclusivamente a prestação de serviços de mão de obra especializada e a utilização de maquinário próprio (ferramentas e EPIs). O fornecimento de todo e qualquer material necessário para a execução integral do projeto é de responsabilidade exclusiva do contratante.*"
        
        txt_zap = f"🏠 *PROPOSTA TÉCNICA - {cliente.upper()}*\n📍 *LOCAL:* {endereco}\n📅 *DATA:* {datetime.now().strftime('%d/%m/%Y')}\n" + "─"*20 + "\n"
        for i in itens_selecionados:
            p_venda = i['p_unit'] * fator
            txt_zap += f"✅ *{i['nome']}*: {i['qtd']} {i['un']} | Total: {moeda(i['qtd'] * p_venda)}\n"
        
        txt_zap += "─"*20 + "\n"
        txt_zap += f"⏱️ *PRAZO:* {prazo} dias úteis\n💰 *INVESTIMENTO TOTAL: {moeda(valor_final)}*\n\n"
        txt_zap += nota_tecnica

        st.text_area("Copia pro Zap", value=txt_zap, height=300)

        # CORREÇÃO DEFINITIVA DO PDF
        if st.button("📥 Gerar PDF Oficial"):
            try:
                pdf = FPDF()
                pdf.add_page()
                # Título
                pdf.set_font("Arial", "B", 16)
                pdf.cell(190, 10, "PROPOSTA DE SERVICOS", ln=True, align="C")
                pdf.ln(10)
                
                # Dados do Cliente
                pdf.set_font("Arial", "B", 11)
                pdf.cell(190, 8, f"CLIENTE: {cliente.upper()}", ln=True)
                pdf.cell(190, 8, f"LOCAL DA OBRA: {endereco}", ln=True)
                pdf.cell(190, 8, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
                pdf.ln(5)
                
                # Tabela de Itens
                pdf.set_fill_color(230, 230, 230)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(110, 10, " DESCRICAO", 1, 0, "L", True)
                pdf.cell(25, 10, " QTD", 1, 0, "C", True)
                pdf.cell(55, 10, " TOTAL", 1, 1, "C", True)
                
                pdf.set_font("Arial", "", 10)
                for i in itens_selecionados:
                    p_venda = i['p_unit'] * fator
                    pdf.cell(110, 8, f" {i['nome']}", 1)
                    pdf.cell(25, 8, f" {i['qtd']} {i['un']}", 1, 0, "C")
                    pdf.cell(55, 8, f" {moeda(i['qtd'] * p_venda)}", 1, 1, "R")
                
                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(190, 10, f"INVESTIMENTO TOTAL: {moeda(valor_final)}", ln=True, align="R")
                pdf.set_font("Arial", "I", 10)
                pdf.cell(190, 8, f"Prazo de execucao: {prazo} dias uteis.", ln=True, align="R")
                
                pdf.ln(10)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(190, 8, "NOTA TECNICA:", ln=True)
                pdf.set_font("Arial", "", 9)
                # Removendo caracteres especiais que travam o PDF
                nota_limpa = "Os valores apresentados compreendem exclusivamente a prestacao de servicos de mao de obra especializada e a utilizacao de maquinario proprio (ferramentas e EPIs). O fornecimento de todo e qualquer material necessario para a execucao integral do projeto e de responsabilidade exclusiva do contratante."
                pdf.multi_cell(190, 6, nota_limpa)
                
                # O PULO DO GATO: pdf.output(dest='S') já retorna o bytearray correto
                pdf_output = pdf.output(dest='S')
                st.download_button(
                    label="Clique aqui para baixar o PDF",
                    data=pdf_output,
                    file_name=f"Orcamento_{cliente}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
