import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparador de Indicadores Econômicos", layout="wide")
st.title("📊 Comparador de Indicadores Econômicos por Estado")

# ==============================
# 1️⃣ Upload do arquivo
# ==============================
uploaded_file = st.file_uploader("⬆️ Faça o upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Remove espaços e deixa os nomes das colunas em minúsculas
    df.columns = df.columns.str.strip().str.lower()

    st.success("✅ Arquivo carregado com sucesso!")
    st.write("### 🧾 Colunas detectadas:")
    st.write(list(df.columns))

    # ==============================
    # 2️⃣ Identifica automaticamente colunas principais
    # ==============================
    col_ano = next((c for c in df.columns if "ano" in c), None)
    col_estado = next((c for c in df.columns if "sigla" in c and "uf" in c), None)

    if col_ano and col_estado:
        anos = sorted(df[col_ano].dropna().unique())
        estados = sorted(df[col_estado].dropna().unique())

        # Pega apenas colunas numéricas
        colunas_numericas = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

        st.sidebar.header("⚙️ Filtros de Comparação")
        tipo_dado = st.sidebar.selectbox("Selecione o tipo de dado:", colunas_numericas)
        ano = st.sidebar.selectbox("Selecione o ano:", anos, index=len(anos)-1)
        estado1 = st.sidebar.selectbox("Primeiro estado:", estados, index=0)
        estado2 = st.sidebar.selectbox("Segundo estado:", estados, index=1)

        # ==============================
        # 3️⃣ Filtragem
        # ==============================
        df_filtrado = df[(df[col_ano] == ano) & (df[col_estado].isin([estado1, estado2]))]

        if df_filtrado.empty:
            st.warning("⚠️ Não há dados disponíveis para essa combinação de filtros.")
        else:
            # ==============================
            # 4️⃣ Gráfico
            # ==============================
            fig, ax = plt.subplots(figsize=(7, 4))
            cores = ["#1f77b4", "#ff7f0e"]

            barras = ax.bar(df_filtrado[col_estado], df_filtrado[tipo_dado], color=cores)

            for i, v in enumerate(df_filtrado[tipo_dado]):
                ax.text(i, v / 2, f"{v:.4f}", ha="center", va="center", color="white", fontweight="bold")

            ax.set_title(f"{tipo_dado.replace('_', ' ').title()} ({ano})", fontsize=14, pad=15)
            ax.set_xlabel("Estado")
            ax.set_ylabel(tipo_dado.replace('_', ' ').title())
            ax.set_ylim(0, df_filtrado[tipo_dado].max() * 1.2)

            st.pyplot(fig)

            # ==============================
            # 5️⃣ Exibição dos dados
            # ==============================
            st.write("### 🔢 Dados utilizados na comparação")
            st.dataframe(df_filtrado[[col_ano, col_estado, tipo_dado]])

    else:
        st.error("❌ O arquivo precisa conter colunas com nomes parecidos com 'ano' e 'sigla_uf'.")
else:
    st.info("📂 Faça o upload do arquivo CSV para começar.")
