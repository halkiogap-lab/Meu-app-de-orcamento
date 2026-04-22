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
", 'B', 12)
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
