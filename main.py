import streamlit as st
from datetime import datetime
from fpdf import FPDF

# Configuração de Profissional
st.set_page_config(page_title="Orçamento Completo de Obras", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- LISTA COMPLETA: DA BASE AO ACABAMENTO ---
SERVICOS = {
    "--- ESTRUTURA E BASE ---": {"un": "-", "p": 0.0},
    "Sapata / Fundação": {"un": "un", "p": 250.0},
    "Vigamento / Colunas": {"un": "m", "p": 150.0},
    "Laje (Batida)": {"un": "m²", "p": 95.0},
    "Escada em Metalon": {"un": "un", "p": 1200.0},
    "Alvenaria (Tijolo à vista/bloco)": {"un": "m²", "p": 60.0},
    "Contra-piso": {"un": "m²", "p": 35.0},
    "--- ACABAMENTO E REVESTIMENTO ---": {"un": "-", "p": 0.0},
    "Reboco": {"un": "m²", "p": 40.0},
    "Piso Cerâmico": {"un": "m²", "p": 50.0},
    "Porcelanato (Chão/Parede)": {"un": "m²", "p": 75.0},
    "Bancada em Porcelanato (Corte/Inst)": {"un": "m", "p": 350.0},
    "Rejunte": {"un": "m²", "p": 15.0},
    "Gesso Liso": {"un": "m²", "p": 45.0},
    "Forro PVC / Gesso": {"un": "m²", "p": 55.0},
    "--- ELÉTRICA E HIDRÁULICA ---": {"un": "-", "p": 0.0},
    "Ponto de Elétrica (Fiação/Tomada)": {"un": "ponto", "p": 130.0},
    "Ponto de Hidráulica (Água/Esgoto)": {"un": "ponto", "p": 140.0},
    "Instalação de Caixa d'água": {"un": "un", "p": 300.0},
    "Instalação de Vaso / Pia": {"un": "un", "p": 180.0},
    "Caixa de Gordura (Construção)": {"un": "un", "p": 250.0},
    "--- PINTURA E TELHADO ---": {"un": "-", "p": 0.0},
    "Pintura Simples": {"un": "m²", "p": 35.0},
    "Pintura com Emassamento": {"un": "m²", "p": 65.0},
    "Telhado Zinco / Telha": {"un": "m²", "p": 185.0},
    "Calhas / Rufos (Instalação)": {"un": "m", "p": 45.0},
}

st.title("🏗️ Orçamento Completo: Da Base ao Acabamento")

# --- DADOS DO CLIENTE ---
with st.container():
    c1, c2 = st.columns(2)
    nome_cliente = c1.text_input("Nome do Cliente")
    local_obra = c2.text_input("Local da Obra")

# --- FRETE E MARGEM ---
st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
distancia = col_f1.number_input("Distância (KM)", min_value=0.0)
valor_km = col_f2.number_input("R$ por KM", value=2.50)
margem_lucro = col_f3.slider("Margem de Segurança/Lucro (%)", 0, 100, 0)

custo_viagem = distancia * valor_km

# --- SELEÇÃO DE SERVIÇOS ---
st.subheader("🛠️ Detalhamento dos Serviços")
selecionados = []
total_maodobra = 0.0

# Organizando em abas ou expanders
for nome, info in SERVICOS.items():
    if info["un"] == "-":
        st.markdown(f"### {nome}")
        continue
        
    with st.expander(f"➕ {nome}"):
        col_s1, col_s2 = st.columns(2)
        quantidade = col_s1.number_input(f"Qtd ({info['un']})", min_value=0.0, key=f"q_{nome}")
        preco_unit = col_s2.number_input(f"Preço Unitário R$", value=float(info['p']), key=f"p_{nome}")
        
        if quantidade > 0:
            subtotal = quantidade * preco_unit
            total_maodobra += subtotal
            selecionados.append({"n": nome, "q": quantidade, "u": info['un'], "t": subtotal})

# --- RESUMO FINANCEIRO ---
st.divider()
valor_base = total_maodobra + custo_viagem
total_final = valor_base * (1 + margem_lucro/100)

res1, res2, res3 = st.columns(3)
res1.metric("Mão de Obra", moeda(total_maodobra))
res2.metric("Deslocamento", moeda(custo_viagem))
res3.metric("TOTAL COM MARGEM", moeda(total_final))

# --- GERAÇÃO DE SAÍDA ---
if selecionados:
    st.subheader("📱 WhatsApp e PDF")
    
    # Texto para Zap
    texto_zap = f"*ORÇAMENTO DE OBRA - {nome_cliente.upper()}*\n📍 {local_obra}\n"
    texto_zap += f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
    texto_zap += "-"*20 + "\n"
    for s in selecionados:
        texto_zap += f"✅ *{s['n']}*: {s['q']} {s['u']} = {moeda(s['t'])}\n"
    texto_zap += "-"*20 + "\n"
    texto_zap += f"🚚 Viagem: {moeda(custo_viagem)}\n"
    if margem_lucro > 0: texto_zap += f"📈 Acréscimo: {margem_lucro}%\n"
    texto_zap += f"💰 *VALOR FINAL: {moeda(total_final)}*"
    
    st.text_area("Copie para o WhatsApp:", value=texto_zap, height=250)

    # Função PDF
    if st.button("📥 Gerar PDF Profissional"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(190, 10, "ORCAMENTO DE PRESTACAO DE SERVICOS", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 12)
            pdf.cell(190, 8, f"Cliente: {nome_cliente}", ln=True)
            pdf.cell(190, 8, f"Local: {local_obra}", ln=True)
            pdf.cell(190, 8, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
            pdf.ln(5)
            pdf.cell(190, 0, "", "T", ln=True)
            pdf.ln(5)
            
            for s in selecionados:
                pdf.cell(190, 8, f"- {s['n']} ({s['q']} {s['u']}): {moeda(s['t'])}", ln=True)
            
            pdf.ln(5)
            pdf.cell(190, 8, f"Custo de Viagem/Logistica: {moeda(custo_viagem)}", ln=True)
            pdf.set_font("Arial", "B", 14)
            pdf.ln(5)
            pdf.cell(190, 10, f"TOTAL DO ORCAMENTO: {moeda(total_final)}", ln=True)
            pdf.set_font("Arial", "I", 10)
            pdf.ln(10)
            pdf.multi_cell(190, 8, "Observacao: Mao de obra especializada. Material de construcao por conta do contratante.")
            
            pdf_data = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button(label="Clique para baixar o PDF", data=pdf_data, file_name=f"orcamento_{nome_cliente}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: Verifique se o 'fpdf2' está no seu requirements.txt")
