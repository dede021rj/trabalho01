import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES GERAIS ---
st.set_page_config(page_title="Comparativo de Despesas do Judiciário", layout="wide")
st.title("📊 Comparativo de Despesas da Justiça Estadual")

# --- LEITURA DO ARQUIVO CSV ---
arquivo_csv = st.file_uploader("Envie o arquivo CSV com os dados", type=["csv"])

if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)

    # Normaliza nomes de colunas (remove espaços e deixa tudo minúsculo)
    df.columns = df.columns.str.strip().str.lower()

    # --- SELEÇÃO DE ANO ---
    anos_disponiveis = sorted(df["ano"].unique())
    ano_escolhido = st.selectbox("Selecione o ano", anos_disponiveis)

    # Filtra o dataframe pelo ano
    df_ano = df[df["ano"] == ano_escolhido]

    # --- SELEÇÃO DE ESTADOS ---
    estados_disponiveis = sorted(df_ano["sigla_uf"].unique())
    estados_escolhidos = st.multiselect(
        "Selecione os estados que deseja comparar",
        estados_disponiveis,
        default=estados_disponiveis[:2]  # pré-seleciona os dois primeiros
    )

    # --- SELEÇÃO DO TIPO DE DADO ---
    opcoes_dados = {
        "Despesa Total / PIB (%)": "despesa_total_pib",
        "Despesa Média por Magistrado": "despesa_media_magistrado",
        "Despesa Total da Justiça Estadual": "despesa_total_justica_estadual"
    }

    tipo_dado = st.selectbox("Selecione o tipo de dado para comparação", list(opcoes_dados.keys()))
    coluna_escolhida = opcoes_dados[tipo_dado]

    # --- FILTRAGEM FINAL ---
    df_filtrado = df_ano[df_ano["sigla_uf"].isin(estados_escolhidos)]

    # --- GRÁFICO ---
    if not df_filtrado.empty:
        fig, ax = plt.subplots(figsize=(8, 4))

        cores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b"]
        barras = ax.bar(
            df_filtrado["sigla_uf"],
            df_filtrado[coluna_escolhida],
            color=cores[:len(df_filtrado)]
        )

        # Rótulos de valor
        for barra in barras:
            altura = barra.get_height()
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                altura * 0.02,
                f"{altura:,.2f}",
                ha="center", va="bottom", fontweight="bold"
            )

        # --- TÍTULOS E EIXOS ---
        ax.set_title(f"{tipo_dado} ({ano_escolhido})", fontsize=14, fontweight="bold")
        ax.set_xlabel("Estado")
        ax.set_ylabel(tipo_dado)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados.")
else:
    st.info("⬆️ Envie um arquivo CSV para começar a análise.")
