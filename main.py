import streamlit as st
from datetime import datetime
from fpdf import FPDF

# Configuração de Profissional
st.set_page_config(page_title="Orçamento Completo", layout="wide")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- LISTA COMPLETA REVISADA ---
SERVICOS = {
    "--- ESTRUTURA E BASE ---": {"un": "-", "p": 0.0},
    "Sapata / Fundação": {"un": "un", "p": 250.0},
    "Vigamento / Colunas": {"un": "m", "p": 150.0},
    "Laje (Batida)": {"un": "m²", "p": 95.0},
    "Escada em Metalon": {"un": "un", "p": 1200.0},
    "Alvenaria (Tijolo/Bloco)": {"un": "m²", "p": 60.0},
    "Contra-piso": {"un": "m²", "p": 35.0},
    
    "--- ACABAMENTO FINO ---": {"un": "-", "p": 0.0},
    "Reboco": {"un": "m²", "p": 40.0},
    "Piso Cerâmico": {"un": "m²", "p": 50.0},
    "Porcelanato (Chão/Parede)": {"un": "m²", "p": 75.0},
    "Bancada em Porcelanato (Corte/Inst)": {"un": "m", "p": 350.0},
    "Rejunte": {"un": "m²", "p": 15.0},
    "Forro PVC / Gesso": {"un": "m²", "p": 55.0},
    
    "--- ELÉTRICA E HIDRÁULICA ---": {"un": "-", "p": 0.0},
    "Ponto de Elétrica": {"un": "ponto", "p": 130.0},
    "Ponto de Hidráulica": {"un": "ponto", "p": 140.0},
    "Instalação de Caixa d'água": {"un": "un", "p": 300.0},
    "Instalação de Vaso / Pia": {"un": "un", "p": 180.0},
    
    "--- SERVIÇOS DE DESENTUPIDORA ---": {"un": "-", "p": 0.0},
    "Desentupimento de Vaso": {"un": "un", "p": 250.0},
    "Desentupimento de Esgoto": {"un": "m", "p": 120.0},
    "Desentupimento de Pia": {"un": "un", "p": 150.0},
    "Limpeza de Caixa de Gordura": {"un": "un", "p": 200.0},
    "Limpeza de Caixa d'água": {"un": "un", "p": 250.0},
    
    "--- PINTURA E TELHADO ---": {"un": "-", "p": 0.0},
    "Pintura Simples": {"un": "m²", "p": 35.0},
    "Pintura com Massa": {"un": "m²", "p": 65.0},
    "Telhado Zinco / Telha": {"un": "m²", "p": 185.0},
}

st.title("🏗️ Orçamento Completo: Obra & Desentupidora")

# --- DADOS DO CLIENTE ---
c1, c2 = st.columns(2)
nome_cliente = c1.text_input("Nome do Cliente", value="")
local_obra = c2.text_input("Local do Serviço", value="")

# --- FRETE E MARGEM ---
st.divider()
f1, f2, f3 = st.columns(3)
distancia = f1.number_input("Distância (KM)", min_value=0.0, step=1.0)
valor_km = f2.number_input("R$ por KM", value=2.50)
margem_lucro = f3.slider("Margem de Lucro (%)", 0, 100, 0)

custo_viagem = distancia * valor_km

# --- SELEÇÃO DE SERVIÇOS ---
st.subheader("🛠️ Detalhamento")
selecionados = []
total_maodobra = 0.0

# Usando um contador pra garantir que a key seja única
idx = 0
for nome, info in SERVICOS.items():
    if info["un"] == "-":
        st.markdown(f"#### {nome}")
        continue
        
    with st.expander(f"➕ {nome}"):
        sc1, sc2 = st.columns(2)
        # Chaves (keys) dinâmicas pra não dar erro de duplicidade
        quantidade = sc1.number_input(f"Qtd", min_value=0.0, key=f"q_{idx}")
        preco_unit = sc2.number_input(f"R$ Unit.", value=float(info['p']), key=f"p_{idx}")
        
        if quantidade > 0:
            subtotal = quantidade * preco_unit
            total_maodobra += subtotal
            selecionados.append({"n": nome, "q": quantidade, "u": info['un'], "t": subtotal})
    idx += 1

# --- CÁLCULOS ---
valor_base = total_maodobra + custo_viagem
total_final = valor_base * (1 + margem_lucro/100)

st.divider()
st.header(f"TOTAL FINAL: {moeda(total_final)}")

# --- SAÍDA ---
if selecionados:
    # Texto Zap
    zap = f"*ORÇAMENTO - {nome_cliente.upper()}*\n📍 {local_obra}\n"
    for s in selecionados:
        zap += f"✅ {s['n']}: {s['q']} {s['u']} = {moeda(s['t'])}\n"
    zap += f"🚚 Viagem: {moeda(custo_viagem)}\n"
    if margem_lucro > 0: zap += f"📈 Margem: {margem_lucro}%\n"
    zap += f"💰 *TOTAL: {moeda(total_final)}*"
    
    st.text_area("Copiar para WhatsApp", value=zap, height=200)

    # Botão PDF
    if st.button("📥 Baixar PDF"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(190, 10, "ORCAMENTO DE SERVICOS", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12)
            pdf.ln(10)
            pdf.cell(190, 8, f"Cliente: {nome_cliente}", ln=True)
            pdf.cell(190, 8, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
            pdf.ln(5)
            for s in selecionados:
                pdf.cell(190, 8, f"- {s['n']} ({s['q']} {s['u']}): {moeda(s['t'])}", ln=True)
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(190, 10, f"TOTAL: {moeda(total_final)}", ln=True)
            
            pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button("Clique aqui para baixar", pdf_bytes, f"orcamento_{nome_cliente}.pdf", "application/pdf")
        except:
            st.error("Erro no PDF. Checou o requirements.txt?")
