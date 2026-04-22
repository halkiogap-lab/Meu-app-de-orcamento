import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="PRO-OBRA | Engenharia de Elite", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE DADOS INTEGRAL (DA FUNDAÇÃO À CHAVE NA PORTA) ---
DB_MESTRE = {
    "🏗️ 1. INFRAESTRUTURA & FUNDAÇÃO": {
        "Locação e Gabarito": {"un": "m²", "p": 15.0},
        "Escavação de Valas/Sapatas": {"un": "m³", "p": 120.0},
        "Sapata / Fundação (Mão de Obra)": {"un": "un", "p": 280.0},
        "Viga Baldrame": {"un": "m", "p": 85.0},
        "Impermeabilização de Fundação": {"un": "m²", "p": 35.0},
    },
    "🧱 2. ESTRUTURA & ALVENARIA": {
        "Colunas / Pilares": {"un": "m", "p": 165.0},
        "Vigas de Cintamento": {"un": "m", "p": 140.0},
        "Laje (Montagem e Batida)": {"un": "m²", "p": 115.0},
        "Alvenaria de Vedação (Tijolo/Bloco)": {"un": "m²", "p": 65.0},
        "Escada Estrutural": {"un": "un", "p": 1500.0},
    },
    "🚿 3. INSTALAÇÕES BRUTAS": {
        "Pontos de Esgoto / Ralo": {"un": "ponto", "p": 160.0},
        "Rede de Água Fria/Quente": {"un": "m", "p": 45.0},
        "Passagem de Conduítes/Caixas Luz": {"un": "un", "p": 35.0},
        "Quadro de Distribuição": {"un": "un", "p": 450.0},
    },
    "🏠 4. COBERTURA": {
        "Estrutura de Telhado (Metalon/Madeira)": {"un": "m²", "p": 120.0},
        "Telha (Zinco/Sanduíche/Cerâmica)": {"un": "m²", "p": 90.0},
        "Instalação de Calhas e Rufos": {"un": "m", "p": 60.0},
    },
    "✨ 5. ACABAMENTO BRUTO": {
        "Chapisco e Emboço": {"un": "m²", "p": 25.0},
        "Reboco Técnico (Parede/Teto)": {"un": "m²", "p": 45.0},
        "Contra-piso Nivelado": {"un": "m²", "p": 40.0},
        "Gesso Liso / Rebaixamento": {"un": "m²", "p": 55.0},
    },
    "💎 6. ACABAMENTO FINO": {
        "Porcelanato (Chão/Parede)": {"un": "m²", "p": 95.0},
        "Bancada em Porcelanato Esculpido": {"un": "m", "p": 550.0},
        "Rodapé Embutido / Sobreposto": {"un": "m", "p": 28.0},
        "Revestimento Cerâmico": {"un": "m²", "p": 65.0},
        "Soleiras e Pingadeiras": {"un": "un", "p": 45.0},
    },
    "🎨 7. PINTURA & CHAVE NA PORTA": {
        "Massa Corrida e Lixamento": {"un": "m²", "p": 45.0},
        "Pintura Final (Interna/Externa)": {"un": "m²", "p": 35.0},
        "Textura / Grafiato / Projetado": {"un": "m²", "p": 55.0},
        "Instalação de Louças e Metais": {"un": "un", "p": 130.0},
        "Limpeza Pós-Obra": {"un": "m²", "p": 25.0},
    },
    "🔧 8. MANUTENÇÃO & DESENTUPIDORA": {
        "Desentupimento Vaso/Pia (K50)": {"un": "un", "p": 320.0},
        "Limpeza de Caixa de Gordura": {"un": "un", "p": 250.0},
        "Limpeza de Caixa d'água": {"un": "un", "p": 220.0},
    }
}

st.sidebar.title("🚀 CONTROLE DE MARGEM")
margem_lucro = st.sidebar.slider("Margem de Lucro Bruta (%)", 0, 200, 40)
custo_operacional_km = st.sidebar.number_input("Custo por KM (Combustível/Tempo)", value=3.50)
meta_m2_dia = st.sidebar.number_input("Rendimento Médio (m²/dia)", value=10.0)

st.title("🏗️ Gestão Integrada: Da Fundação à Entrega")

tab_orc, tab_analise = st.tabs(["📝 GERADOR TÉCNICO", "📊 DASHBOARD DO PATRÃO"])

with tab_orc:
    col_a, col_b = st.columns(2)
    cliente = col_a.text_input("Nome do Cliente")
    local = col_b.text_input("Endereço da Obra")
    distancia = st.number_input("Distância Total para Deslocamento (KM)", min_value=0.0)

    selecionados = []
    total_mao_obra = 0.0
    total_m2_obra = 0.0

    idx = 0
    for etapa, servicos in DB_MESTRE.items():
        with st.expander(f"{etapa}"):
            for s, info in servicos.items():
                st.markdown(f"**{s}**")
                c_q, c_p = st.columns(2)
                qtd = c_q.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"qtd_{idx}")
                p_unit = c_p.number_input(f"Preço Base (R$)", value=float(info['p']), key=f"val_{idx}")
                
                if qtd > 0:
                    total_mao_obra += (qtd * p_unit)
                    if info['un'] == "m²": total_m2_obra += qtd
                    selecionados.append({"n": s, "q": qtd, "u": info['un'], "p": p_unit})
                idx += 1

with tab_analise:
    if not selecionados:
        st.info("Selecione os serviços na aba 'GERADOR TÉCNICO' para realizar o fechamento.")
    else:
        custo_viagem = distancia * custo_operacional_km
        valor_final_cliente = (total_mao_obra + custo_viagem) * (1 + margem_lucro/100)
        fator_ajuste = valor_final_cliente / total_mao_obra if total_mao_obra > 0 else 1
        prazo_estimado = math.ceil(total_m2_obra / meta_m2_dia) if total_m2_obra > 0 else 1
        lucro_real_limpo = valor_final_cliente - total_mao_obra - custo_viagem

        m_cli, m_luc, m_pz = st.columns(3)
        m_cli.metric("Total Cliente", moeda(valor_final_cliente))
        m_luc.metric("Lucro Líquido", moeda(lucro_real_limpo))
        m_pz.metric("Prazo de Entrega", f"{prazo_estimado} dias úteis")

        st.divider()
        
        nota_padrao = "⚠️ *Nota Técnica: Valores referentes a mão de obra especializada e ferramentas próprias. Fornecimento de materiais por conta do cliente.*"
        
        resumo_zap = f"🏛️ *ORÇAMENTO PROFISSIONAL - {cliente.upper()}*\n📍 *LOCAL:* {local}\n" + "─"*15 + "\n"
        for item in selecionados:
            v_final_item = (item['q'] * item['p']) * fator_ajuste
            resumo_zap += f"🔹 *{item['n']}*: {item['q']} {item['u']} | {moeda(v_final_item)}\n"
        resumo_zap += "─"*15 + f"\n⏱️ *PRAZO:* {prazo_estimado} dias\n💰 *INVESTIMENTO:* {moeda(valor_final_cliente)}\n\n{nota_padrao}"
        
        st.subheader("Prévia WhatsApp")
        st.text_area("Copia aqui", resumo_zap, height=250)

        if st.button("📄 Gerar Orçamento Oficial (PDF)"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(190, 10, "PROPOSTA TECNICA DE ENGENHARIA", 0, 1, "C")
                pdf.ln(10)
                pdf.set_font("Arial", "", 12)
                pdf.cell(190, 8, f"CLIENTE: {cliente.upper()}", 0, 1)
                pdf.cell(190, 8, f"LOCAL: {local}", 0, 1)
                pdf.cell(190, 8, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
                pdf.ln(10)
                
                for item in selecionados:
                    v_item = (item['q'] * item['p']) * fator_ajuste
                    pdf.cell(190, 8, f"- {item['n']} ({item['q']} {item['u']}): {moeda(v_item)}", 0, 1)
                
                pdf.ln(10)
                pdf.set_font("Arial", "B", 13)
                pdf.cell(190, 10, f"VALOR TOTAL DO INVESTIMENTO: {moeda(valor_final_cliente)}", 0, 1, "R")
                pdf.ln(10)
                pdf.set_font("Arial", "I", 10)
                pdf.multi_cell(190, 6, nota_padrao.replace("*", "").replace("⚠️ ", ""))
                
                pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
                st.download_button(label="📥 Baixar Orçamento PDF", data=pdf_bytes, file_name=f"Orcamento_{cliente}.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
