import streamlit as st
from datetime import datetime
from fpdf import FPDF
import math

st.set_page_config(page_title="Gestão de Obras", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- BANCO DE SERVIÇOS COMPLETO ---
DB = {
    "ESTRUTURA": {
        "Sapata / Fundação": {"un": "un", "p": 250.0},
        "Vigamento / Colunas": {"un": "m", "p": 150.0},
        "Laje (Batida)": {"un": "m²", "p": 95.0},
        "Escada em Metalon": {"un": "un", "p": 1200.0},
        "Alvenaria": {"un": "m²", "p": 60.0},
    },
    "ACABAMENTO": {
        "Reboco": {"un": "m²", "p": 40.0},
        "Piso Cerâmico": {"un": "m²", "p": 50.0},
        "Porcelanato": {"un": "m²", "p": 85.0},
        "Bancada Porcelanato": {"un": "m", "p": 450.0},
        "Rodapé": {"un": "m", "p": 15.0},
    },
    "HIDRÁULICA/DESENTUPIDORA": {
        "Desentupimento Vaso": {"un": "un", "p": 280.0},
        "Desentupimento Esgoto": {"un": "m", "p": 130.0},
        "Limpeza Caixa Gordura": {"un": "un", "p": 220.0},
        "Ponto Hidráulico": {"un": "ponto", "p": 150.0},
    },
    "COBERTURA/PINTURA": {
        "Telhado Zinco": {"un": "m²", "p": 190.0},
        "Calhas": {"un": "m", "p": 50.0},
        "Pintura Simples": {"un": "m²", "p": 35.0},
        "Pintura com Massa": {"un": "m²", "p": 70.0},
    }
}

st.title("🏗️ Painel Corporativo de Engenharia")

t1, t2, t3 = st.tabs(["📊 MONITOR DO PATRÃO", "📝 GERADOR", "⚙️ AJUSTE"])

with t3:
    margem = st.slider("Margem de Lucro (%)", 0, 150, 30)
    c_km = st.number_input("R$ por KM", value=3.20)
    rendimento = st.number_input("Rendimento (m²/dia)", value=10.0)

with t2:
    col_a, col_b = st.columns(2)
    cli = col_a.text_input("Cliente")
    end = col_b.text_input("Local")
    dist = st.number_input("Distância (KM)", min_value=0.0)

    selecionados = []
    total_base = 0.0
    total_m2 = 0.0

    idx = 0
    for cat, servs in DB.items():
        with st.expander(f"📂 {cat}"):
            for s, info in servs.items():
                st.write(f"**{s}**") # NOME DO SERVIÇO VISÍVEL
                c1, c2 = st.columns(2)
                qtd = c1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q{idx}")
                prc = c2.number_input(f"Preço Base", value=float(info['p']), key=f"p{idx}")
                if qtd > 0:
                    total_base += (qtd * prc)
                    if info['un'] == "m²": total_m2 += qtd
                    selecionados.append({"n": s, "q": qtd, "u": info['un'], "p": prc})
                idx += 1

with t1:
    if not selecionados:
        st.info("Selecione os serviços no Gerador.")
    else:
        custo_log = dist * c_km
        v_final = (total_base + custo_log) * (1 + margem/100)
        fator = v_final / total_base if total_base > 0 else 1
        dias = math.ceil(total_m2 / rendimento) if total_m2 > 0 else 1

        st.metric("Total p/ Cliente", moeda(v_final))
        st.metric("Seu Lucro Real", moeda(v_final - total_base - custo_log))
        
        nota = "⚠️ *Nota técnica: Os valores apresentados compreendem exclusivamente a prestação de serviços de mão de obra especializada e a utilização de maquinário próprio (ferramentas e EPIs). O fornecimento de todo e qualquer material necessário para a execução integral do projeto é de responsabilidade exclusiva do contratante.*"
        
        resumo = f"🏠 *PROPOSTA - {cli.upper()}*\n📍 *LOCAL:* {end}\n" + "─"*15 + "\n"
        for i in selecionados:
            resumo += f"✅ *{i['n']}*: {i['q']} {i['u']} | Total: {moeda(i['q'] * i['p'] * fator)}\n"
        resumo += "─"*15 + f"\n⏱️ *PRAZO:* {dias} dias úteis\n💰 *TOTAL: {moeda(v_final)}*\n\n{nota}"
        
        st.text_area("WhatsApp", resumo, height=250)

        # GERAÇÃO DE PDF CORRIGIDA
        if st.button("📥 Gerar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "PROPOSTA DE SERVICOS", 0, 1, "C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 11)
            pdf.cell(190, 7, f"CLIENTE: {cli.upper()}", 0, 1)
            pdf.cell(190, 7, f"LOCAL: {end}", 0, 1)
            pdf.ln(5)
            for i in selecionados:
                pdf.cell(190, 7, f"- {i['n']} ({i['q']} {i['u']}): {moeda(i['q'] * i['p'] * fator)}", 0, 1)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(190, 10, f"VALOR TOTAL: {moeda(v_final)}", 0, 1, "R")
            pdf.ln(10)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(190, 7, "NOTA TECNICA:", 0, 1)
            pdf.set_font("Arial", "", 9)
            nota_pdf = nota.replace("⚠️ ", "").replace("*", "")
            pdf.multi_cell(190, 5, nota_pdf)
            
            # O SEGREDO DO DOWNLOAD SEM ERRO:
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="Clique para baixar", data=pdf_bytes, file_name=f"orcamento_{cli}.pdf", mime="application/pdf")
