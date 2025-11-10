import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Comparativo de Despesas da Justiça", layout="wide")
st.title("📊 Comparativo de Despesas da Justiça Estadual")

# --- UPLOAD DO ARQUIVO ---
arquivo_csv = st.file_uploader("Envie o arquivo CSV com os dados", type=["csv"])

if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)

    # Normaliza os nomes das colunas (minúsculas e sem espaços)
    df.columns = df.columns.str.strip().str.lower()

    st.subheader("🧩 Colunas encontradas no arquivo:")
    st.write(df.columns.tolist())

    # Identifica automaticamente as colunas principais
    col_ano = next((col for col in df.columns if "ano" in col), None)
    col_estado = next((col for col in df.columns if "sigla_uf" in col or "estado" in col), None)

    if not col_ano:
        st.error("❌ Não foi encontrada uma coluna relacionada a 'ano'.")
    elif not col_estado:
        st.error("❌ Não foi encontrada uma coluna relacionada a 'sigla_uf' ou 'estado'.")
    else:
        # --- SELEÇÃO DE ANO ---
        anos_disponiveis = sorted(df[col_ano].unique())
        ano_escolhido = st.selectbox("Selecione o ano", anos_disponiveis)

        df_ano = df[df[col_ano] == ano_escolhido]

        # --- SELEÇÃO DE ESTADOS ---
        estados_disponiveis = sorted(df_ano[col_estado].unique())
        estados_escolhidos = st.multiselect(
            "Selecione os estados que deseja comparar",
            estados_disponiveis,
            default=estados_disponiveis[:2]
        )

        # --- OPÇÕES DE DADOS ---
        opcoes_dados = {
            "Despesa Total / PIB (%)": "despesa_total_pib",
            "Despesa Média por Magistrado": "despesa_media_magistrado",
            "Despesa Total da Justiça Estadual": "despesa_total_justica_estadual"
        }

        tipo_dado = st.selectbox("Selecione o tipo de dado para comparação", list(opcoes_dados.keys()))
        coluna_escolhida = opcoes_dados[tipo_dado]

        if coluna_escolhida not in df.columns:
            st.error(f"❌ A coluna '{coluna_escolhida}' não foi encontrada no arquivo CSV.")
        else:
            df_filtrado = df_ano[df_ano[col_estado].isin(estados_escolhidos)]

            # --- GRÁFICO ---
            if not df_filtrado.empty:
                fig, ax = plt.subplots(figsize=(8, 4))
                cores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b"]

                barras = ax.bar(
                    df_filtrado[col_estado],
                    df_filtrado[coluna_escolhida],
                    color=cores[:len(df_filtrado)]
                )

                # Adiciona os valores dentro das barras
                for barra in barras:
                    altura = barra.get_height()
                    ax.text(
                        barra.get_x() + barra.get_width() / 2,
                        altura * 0.02,
                        f"{altura:,.2f}",
                        ha="center", va="bottom", fontweight="bold"
                    )

                ax.set_title(f"{tipo_dado} ({ano_escolhido})", fontsize=14, fontweight="bold")
                ax.set_xlabel("Estado")
                ax.set_ylabel(tipo_dado)
                st.pyplot(fig)
            else:
                st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
else:
    st.info("⬆️ Envie um arquivo CSV para começar a análise.")
