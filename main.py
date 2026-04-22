import streamlit as st
from fpdf import FPDF

# Título da Aba
st.set_page_config(page_title="OT Construções - Propostas", layout="centered")

def moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("🏛️ Gerador de Proposta - OT Construções")

# 1. ENTRADA DE DADOS
with st.container():
    cliente = st.text_input("Nome do Cliente", placeholder="Ex: Sr. Osmar")
    local = st.text_input("Local da Obra", placeholder="Ex: Guandu")
    servico_nome = st.text_input("Serviço Principal", placeholder="Ex: Reforma de Cozinha em Porcelanato")
    valor_total = st.number_input("Valor Final para o Cliente (R$)", min_value=0.0)
    prazo = st.text_input("Prazo Estimado", placeholder="Ex: 15 dias úteis")

st.divider()

# 2. PRÉVIA PARA WHATSAPP
if valor_total > 0:
    st.subheader("📲 Prévia para o WhatsApp")
    
    texto_zap = (
        f"🏠 *PROPOSTA TÉCNICA - OT CONSTRUÇÕES*\n"
        f"📍 *LOCAL:* {local}\n"
        f"─" * 15 + "\n"
        f"✅ *SERVIÇO:* {servico_nome}\n"
        f"⏱️ *PRAZO:* {prazo}\n"
        f"💰 *INVESTIMENTO:* {moeda(valor_total)}\n\n"
        f"⚠️ *Nota:* Valores referentes exclusivamente à mão de obra e ferramentas. "
        f"Todo o material é de responsabilidade do contratante."
    )
    
    st.text_area("Copia e Cola no Zap:", texto_zap, height=200)

    # 3. GERADOR DE PDF (MÉTODO SEGURO)
    if st.button("📄 Baixar Orçamento Oficial"):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Cabeçalho
            pdf.set_font("Arial", "B", 18)
            pdf.cell(190, 15, "OT CONSTRUCOES", 0, 1, "C")
            pdf.set_font("Arial", "B", 12)
            pdf.cell(190, 10, "PROPOSTA TECNICA DE PRESTACAO DE SERVICOS", 0, 1, "C")
            pdf.ln(10)

            # Dados
            pdf.set_font("Arial", "", 12)
            pdf.cell(190, 8, f"CLIENTE: {cliente.upper()}", 0, 1)
            pdf.cell(190, 8, f"LOCAL: {local.upper()}", 0, 1)
            pdf.cell(190, 8, f"DATA: 22/04/2026", 0, 1)
            pdf.ln(10)

            # Conteúdo
            pdf.set_font("Arial", "B", 12)
            pdf.cell(190, 10, "DESCRITIVO DO SERVICO:", "B", 1)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(190, 10, f"- {servico_nome}")
            pdf.ln(10)

            # Rodapé Financeiro
            pdf.set_font("Arial", "B", 14)
            pdf.cell(190, 10, f"TOTAL DO INVESTIMENTO: {moeda(valor_total)}", 0, 1, "R")
            
            # Exportação Binária Segura
            pdf_out = pdf.output(dest='S').encode('latin-1', 'ignore')
            st.download_button(
                label="📥 Clique para Salvar o PDF",
                data=pdf_out,
                file_name=f"Proposta_{cliente}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar documento: {e}")
        "Pilar / Viga (Mão de Obra)": {"un": "m", "p": 155.0},
        "Laje Maciça (Montagem/Batida)": {"un": "m²", "p": 98.0},
        "Escada Estrutural (Mão de Obra)": {"un": "un", "p": 4500.0},
    },
    "03. ACABAMENTO ALTO PADRÃO": {
        "Reboco Técnico (Nivelado)": {"un": "m²", "p": 45.0},
        "Porcelanato Grande Formato": {"un": "m²", "p": 125.0},
        "Bancada Esculpida em Porcelanato": {"un": "m", "p": 680.0},
        "Rodapé Embutido": {"un": "m", "p": 38.0},
        "Gesso Liso / Drywall": {"un": "m²", "p": 65.0},
    },
    "04. ELÉTRICA & HIDRÁULICA": {
        "Ponto de Elétrica": {"un": "pt", "p": 145.0},
        "Quadro Geral de Energia": {"un": "un", "p": 550.0},
        "Ponto de Hidráulica/Esgoto": {"un": "pt", "p": 160.0},
        "Instalação de Louças/Metais": {"un": "un", "p": 120.0},
    },
    "05. PINTURA & FINALIZAÇÃO": {
        "Massa Corrida & Lixamento": {"un": "m²", "p": 42.0},
        "Pintura Premium (Interna/Externa)": {"un": "m²", "p": 35.0},
        "Aplicação de Textura/Grafiato": {"un": "m²", "p": 48.0},
        "Limpeza Pós-Obra Técnica": {"un": "m²", "p": 25.0},
    }
}

# --- HEADER ---
st.title("🏗️ OT CONSTRUÇÕES - Intelligence ERP")
st.caption("Gestão de Orçamentos e Lucratividade para Alto Padrão")

tab1, tab2, tab3 = st.tabs(["📊 MONITOR DO PATRÃO", "📝 GERADOR DE ORÇAMENTO", "⚙️ CONFIGURAÇÕES"])

# --- TAB3: CONFIGURAÇÕES ---
with tab3:
    st.header("Parâmetros de Negócio")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        margem_global = st.slider("Margem de Lucro OT (%)", 0, 200, 40)
        custo_km = st.number_input("Custo Logístico por KM (R$)", value=4.50)
    with col_c2:
        prod_diaria = st.number_input("Capacidade de Execução (m²/dia)", value=5.0)
        dias_trabalho = st.selectbox("Dias de Trabalho por Semana", [5, 6, 7])

# --- TAB2: GERADOR DE ORÇAMENTO ---
with tab2:
    st.header("Dados do Projeto")
    c1, c2, c3 = st.columns(3)
    nome_cliente = c1.text_input("Cliente", placeholder="Nome ou Empresa")
    endereco = c2.text_input("Endereço / Obra")
    distancia = c3.number_input("Distância Logística (KM)", min_value=0.0)

    st.subheader("Seleção Técnica de Serviços")
    itens_selecionados = []
    total_base_mao_obra = 0.0
    total_m2_obra = 0.0

    for cat, servs in DB_SERVICOS.items():
        with st.expander(f"📂 {cat}"):
            for s_nome, s_info in servs.items():
                col_1, col_2, col_3 = st.columns([3, 1, 1])
                col_1.write(f"**{s_nome}**")
                qtd = col_2.number_input(f"Qtd ({s_info['un']})", min_value=0.0, key=f"q_{s_nome}")
                # Preço base editável por obra
                preco_base = col_3.number_input(f"Preço Unitário", value=s_info['p'], key=f"p_{s_nome}")
                
                if qtd > 0:
                    total_base_mao_obra += (qtd * preco_base)
                    if s_info['un'] == "m²": total_m2_obra += qtd
                    itens_selecionados.append({"nome": s_nome, "qtd": qtd, "un": s_info['un'], "p_base": preco_base})

# --- TAB1: MONITOR DO PATRÃO (VISÃO GESTOR) ---
with tab1:
    if not itens_selecionados:
        st.info("Utilize a aba 'GERADOR DE ORÇAMENTO' para selecionar os itens da obra.")
    else:
        # Cálculos de Inteligência
        custo_logistica = distancia * custo_km
        valor_final_cliente = (total_base_mao_obra + custo_logistica) * (1 + margem_global/100)
        lucro_liquido = valor_final_cliente - total_base_mao_obra - custo_logistica
        
        # Cronograma
        dias_uteis = math.ceil(total_m2_obra / prod_diaria) if total_m2_obra > 0 else 7
        prazo_final_data = datetime.now() + timedelta(days=math.ceil(dias_uteis * (7/dias_trabalho)))

        st.subheader("Painel de Lucratividade")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("FATURAMENTO BRUTO", moeda(valor_final_cliente))
        m2.metric("LUCRO REAL (LÍQUIDO)", moeda(lucro_liquido), f"{margem_global}%")
        m3.metric("CUSTO OPERACIONAL", moeda(total_base_mao_obra + custo_logistica))
        m4.metric("PRAZO ESTIMADO", f"{dias_uteis} DIAS")

        st.divider()

        # Fator de Diluição (Oculta lucro e logística no preço unitário dos itens)
        fator = valor_final_cliente / total_base_mao_obra if total_base_mao_obra > 0 else 1
        
        col_out1, col_out2 = st.columns(2)
        
        with col_out1:
            st.subheader("📲 Texto para WhatsApp")
            zap_texto = f"🏗️ *ORÇAMENTO: OT CONSTRUÇÕES*\n"
            zap_texto += f"👤 *CLIENTE:* {nome_cliente.upper()}\n"
            zap_texto += f"📍 *LOCAL:* {endereco}\n"
            zap_texto += "─" * 20 + "\n\n"
            
            for item in itens_selecionados:
                p_venda = item['p_base'] * fator
                zap_texto += f"✅ *{item['nome']}*\n   {item['qtd']} {item['un']} — {moeda(item['qtd'] * p_venda)}\n\n"
            
            zap_texto += "─" * 20 + "\n"
            zap_texto += f"⏱️ *PRAZO DE ENTREGA:* {dias_uteis} dias úteis\n"
            zap_texto += f"💰 *INVESTIMENTO TOTAL: {moeda(valor_final_cliente)}*\n\n"
            zap_texto += "_Qualidade e compromisso com o alto padrão._"
            
            st.text_area("Copie e cole no WhatsApp", value=zap_texto, height=350)

        with col_out2:
            st.subheader("📄 Documento PDF")
            if st.button("GERAR PROPOSTA PROFISSIONAL"):
                pdf = FPDF()
                pdf.add_page()
                # Header Dark Simulado no PDF
                pdf.set_fill_color(30, 30, 30)
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", 'B', 20)
                pdf.cell(190, 15, "OT CONSTRUCOES", ln=True, align='C')
                pdf.set_font("Arial", '', 10)
                pdf.cell(190, 10, "PROPOSTA TECNICA DE PRESTACAO DE SERVICOS", ln=True, align='C')
                
                pdf.set_text_color(0, 0, 0)
                pdf.ln(15)
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(190, 10, f"CLIENTE: {nome_cliente.upper()}", ln=True)
                pdf.cell(190, 10, f"LOCAL: {endereco.upper()}", ln=True)
                pdf.cell(190, 10, f"DATA: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
                pdf.ln(5)
                
                # Tabela de Itens
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(110, 10, " DESCRICAO DO SERVICO", 1, 0, 'L', True)
                pdf.cell(30, 10, " QTD", 1, 0, 'C', True)
                pdf.cell(50, 10, " TOTAL ITEM", 1, 1, 'C', True)
                
                pdf.set_font("Arial", '', 10)
                for item in itens_selecionados:
                    p_venda = item['p_base'] * fator
                    pdf.cell(110, 8, f" {item['nome']}", 1)
                    pdf.cell(30, 8, f" {item['qtd']} {item['un']}", 1, 0, 'C')
                    pdf.cell(50, 8, f" {moeda(item['qtd'] * p_venda)}", 1, 1, 'R')
                
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"VALOR TOTAL DO INVESTIMENTO: {moeda(valor_final_cliente)}", ln=True, align='R')
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(190, 10, f"Prazo estimado de execucao: {dias_uteis} dias uteis.", ln=True, align='R')

                # Saída segura em bytes para evitar erro de download
                pdf_output = pdf.output(dest='S').encode('latin-1', errors='replace')
                st.download_button(
                    label="⬇️ BAIXAR PDF AGORA",
                    data=pdf_output,
                    file_name=f"Orcamento_OT_{nome_cliente.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
