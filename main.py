import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="PRO-OBRA | Gestão de Elite", layout="wide", initial_sidebar_state="expanded")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS ESTRUTURADO (TODA A OBRA) ---
DB_MESTRE = {
    "🏗️ INFRAESTRUTURA & ALVENARIA": {
        "Sapata / Fundação (Mão de obra)": {"un": "un", "p": 280.0},
        "Vigamento / Colunas": {"un": "m", "p": 165.0},
        "Alvenaria (Tijolo à vista/Bloco)": {"un": "m²", "p": 65.0},
        "Laje (Montagem e Concretagem)": {"un": "m²", "p": 110.0},
        "Contra-piso técnico": {"un": "m²", "p": 38.0},
        "Reboco Interno/Externo": {"un": "m²", "p": 45.0},
    },
    "💎 ACABAMENTO DE ALTO PADRÃO": {
        "Porcelanato Grande Formato": {"un": "m²", "p": 95.0},
        "Piso Cerâmico Padrão": {"un": "m²", "p": 55.0},
        "Revestimento de Parede (Cozinha/Banho)": {"un": "m²", "p": 70.0},
        "Bancada Esculpida em Porcelanato": {"un": "m", "p": 480.0},
        "Instalação de Rodapé Embutido": {"un": "m", "p": 25.0},
        "Escada (Revestimento em Porcelanato)": {"un": "degrau", "p": 120.0},
    },
    "🔧 HIDRÁULICA & DESENTUPIDORA": {
        "Desentupimento Vaso (Máquina K50)": {"un": "un", "p": 300.0},
        "Desentupimento Rede de Esgoto": {"un": "m", "p": 140.0},
        "Limpeza de Caixa de Gordura": {"un": "un", "p": 250.0},
        "Instalação de Vaso / Torneira": {"un": "un", "p": 120.0},
        "Ponto de Água/Esgoto (Instalação)": {"un": "ponto", "p": 180.0},
    },
    "🎨 PINTURA & TELHADO": {
        "Pintura Massa Corrida + Lixamento": {"un": "m²", "p": 75.0},
        "Pintura Simples (Látex/Acrílica)": {"un": "m²", "p": 40.0},
        "Textura / Grafiato": {"un": "m²", "p": 50.0},
        "Telhado Zinco / Sanduíche": {"un": "m²", "p": 210.0},
        "Impermeabilização de Calhas": {"un": "m", "p": 60.0},
    }
}

st.sidebar.title("🛠️ PAINEL DE CONTROLE")
margem_lucro = st.sidebar.slider("Margem de Lucro Bruta (%)", 0, 150, 35)
custo_combustivel = st.sidebar.number_input("Custo Logístico (R$/KM)", value=3.50)
produtividade = st.sidebar.number_input("Meta de Produção (m²/dia)", value=8.0)

st.title("🚀 Sistema Integrado de Orçamentos Profissionais")

aba1, aba2 = st.tabs(["📝 NOVO ORÇAMENTO", "📊 ANÁLISE DO PATRÃO"])

with aba1:
    col_cli, col_loc = st.columns(2)
    cliente = col_cli.text_input("Nome do Cliente / Obra")
    local = col_loc.text_input("Localização do Serviço")
    distancia = st.number_input("Distância para Deslocamento (KM Total)", min_value=0.0)

    selecionados = []
    total_mao_obra = 0.0
    total_area_m2 = 0.0

    idx = 0
    for categoria, servicos in DB_MESTRE.items():
        with st.expander(f"{categoria}"):
            for s_nome, s_info in servicos.items():
                st.markdown(f"**{s_nome}**") # Nome visível
                c_qtd, c_val = st.columns([1, 1])
                qtd = c_qtd.number_input(f"Quantidade ({s_info['un']})", min_value=0.0, key=f"q_{idx}")
                val_unit = c_val.number_input(f"Valor Base Unitário (R$)", value=float(s_info['p']), key=f"p_{idx}")
                
                if qtd > 0:
                    subtotal = qtd * val_unit
                    total_mao_obra += subtotal
                    if s_info['un'] == "m²": total_area_m2 += qtd
                    selecionados.append({"nome": s_nome, "qtd": qtd, "un": s_info['un'], "p_unit": val_unit})
                idx += 1

with aba2:
    if not selecionados:
        st.warning("Adicione serviços na aba 'GERADOR' para ver a análise.")
    else:
        # CÁLCULOS TÉCNICOS
        custo_viagem = distancia * custo_combustivel
        preco_venda_total = (total_mao_obra + custo_viagem) * (1 + margem_lucro/100)
        fator_venda = preco_venda_total / total_mao_obra if total_mao_obra > 0 else 1
        prazo_obra = math.ceil(total_area_m2 / produtividade) if total_area_m2 > 0 else 1
        lucro_liquido = preco_venda_total - total_mao_obra - custo_viagem

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Valor p/ Cliente", moeda(preco_venda_total))
        col_m2.metric("Seu Lucro Real", moeda(lucro_liquido))
        col_m3.metric("Prazo Estimado", f"{prazo_obra} dias")

        st.divider()
        
        # VISUALIZAÇÃO PARA WHATSAPP
        nota_oficial = "⚠️ *Nota: Valores incluem mão de obra especializada e ferramentas. Materiais de construção por conta do contratante.*"
        
        zap_msg = f"🏛️ *PROPOSTA TÉCNICA - {cliente.upper()}*\n📍 *OBRA:* {local}\n" + "─"*15 + "\n"
        for item in selecionados:
            v_item = (item['qtd'] * item['p_unit']) * fator_venda
            zap_msg += f"🔹 *{item['nome']}*: {item['qtd']} {item['un']} | {moeda(v_item)}\n"
        
        zap_msg += "─"*15 + f"\n⏱️ *PRAZO:* {prazo_obra} dias úteis\n💰 *INVESTIMENTO:* {moeda(preco_venda_total)}\n\n{nota_oficial}"
        
        st.subheader("Visualização para o Cliente")
        st.text_area("Copia pro WhatsApp", zap_msg, height=300)

        # GERAÇÃO DE PDF PROFISSIONAL (CORRIGIDO)
        if st.button("📄 Gerar Orçamento Oficial (PDF)"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(190, 15, "ORCAMENTO DE SERVICOS DE ENGENHARIA", 0, 1, "C")
                pdf.ln(5)
                
                pdf.set_font("Arial", "", 11)
                pdf.cell(190, 8, f"CLIENTE: {cliente.upper()}", 0, 1)
                pdf.cell(190, 8, f"LOCAL DA OBRA: {local}", 0, 1)
                pdf.cell(190, 8, f"DATA DE EMISSAO: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
                pdf.ln(10)
                
                # Cabeçalho da Tabela
                pdf.set_fill_color(240, 240, 240)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(100, 10, " DESCRICAO DO SERVICO", 1, 0, "L", True)
                pdf.cell(30, 10, " QUANT.", 1, 0, "C", True)
                pdf.cell(60, 10, " TOTAL", 1, 1, "C", True)
                
                pdf.set_font("Arial", "", 10)
                for item in selecionados:
                    v_item = (item['qtd'] * item['p_unit']) * fator_venda
                    pdf.cell(100, 8, f" {item['nome']}", 1)
                    pdf.cell(30, 8, f" {item['qtd']} {item['un']}", 1, 0, "C")
                    pdf.cell(60, 8, f" {moeda(v_item)}", 1, 1, "R")
                
                pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(190, 10, f"VALOR TOTAL DO INVESTIMENTO: {moeda(preco_venda_total)}", 0, 1, "R")
                pdf.ln(5)
                pdf.set_font("Arial", "I", 10)
                pdf.multi_cell(190, 6, nota_oficial.replace("*", "").replace("⚠️ ", ""))
                
                # DOWNLOAD SEGURO
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button(label="📥 Baixar Orçamento PDF", data=pdf_bytes, file_name=f"Orcamento_{cliente}.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"Erro ao gerar documento: {e}")
