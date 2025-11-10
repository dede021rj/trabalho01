import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1️⃣ Título e upload
# ==============================
st.set_page_config(page_title="Comparador de Indicadores Econômicos", layout="wide")
st.title("📊 Comparador de Indicadores Econômicos por Estado")

uploaded_file = st.file_uploader("⬆️ Faça o upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    # ==============================
    # 2️⃣ Leitura dos dados
    # ==============================
    df = pd.read_csv(uploaded_file)
    st.success("✅ Arquivo carregado com sucesso!")
    st.write("### 🧾 Colunas disponíveis no arquivo:")
    st.write(list(df.columns))

    # ==============================
    # 3️⃣ Identificação automática das colunas principais
    # ==============================
    if "ano" in df.columns and "sigla_uf" in df.columns:
        anos = sorted(df["ano"].unique())
        estados = sorted(df["sigla_uf"].unique())

        # Seleciona apenas colunas numéricas (para o tipo de dado)
        colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

        st.sidebar.header("⚙️ Filtros de Comparação")
        tipo_dado = st.sidebar.selectbox("Selecione o tipo de dado:", colunas_numericas)
        ano = st.sidebar.selectbox("Selecione o ano:", anos, index=len(anos)-1)
        estado1 = st.sidebar.selectbox("Primeiro estado:", estados, index=0)
        estado2 = st.sidebar.selectbox("Segundo estado:", estados, index=1)

        # ==============================
        # 4️⃣ Filtragem dos dados
        # ==============================
        df_filtrado = df[(df["ano"] == ano) & (df["sigla_uf"].isin([estado1, estado2]))]

        if df_filtrado.empty:
            st.warning("⚠️ Não há dados disponíveis para essa combinação de filtros.")
        else:
            # ==============================
            # 5️⃣ Geração do gráfico
            # ==============================
            fig, ax = plt.subplots(figsize=(7, 4))
            cores = ["#1f77b4", "#ff7f0e"]

            barras = ax.bar(df_filtrado["sigla_uf"], df_filtrado[tipo_dado], color=cores)

            # Adiciona rótulos dentro das barras
            for i, v in enumerate(df_filtrado[tipo_dado]):
                ax.text(i, v / 2, f"{v:.4f}", ha="center", va="center", color="white", fontweight="bold")

            ax.set_title(f"{tipo_dado.replace('_', ' ').title()} ({ano})", fontsize=14, pad=15)
            ax.set_xlabel("Estado")
            ax.set_ylabel(tipo_dado.replace('_', ' ').title())
            ax.set_ylim(0, df_filtrado[tipo_dado].max() * 1.2)

            st.pyplot(fig)

            # ==============================
            # 6️⃣ Exibição da tabela filtrada
            # ==============================
            st.write("### 🔢 Dados utilizados na comparação")
            st.dataframe(df_filtrado[["ano", "sigla_uf", tipo_dado]])

    else:
        st.error("❌ O arquivo precisa conter as colunas 'ano' e 'sigla_uf'. Verifique seu CSV.")
else:
    st.info("📂 Faça o upload do arquivo CSV para começar.")
