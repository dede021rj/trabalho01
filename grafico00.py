import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Comparativo de Indicadores Econômicos por Estado")

# ==============================
# 1️⃣ Upload do arquivo CSV
# ==============================
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ==============================
    # 2️⃣ Seletores dinâmicos
    # ==============================
    estados = sorted(df["sigla_uf"].unique())
    anos = sorted(df["ano"].unique())

    # Apenas colunas numéricas (excluindo 'ano' e 'sigla_uf')
    colunas_disponiveis = [col for col in df.columns if df[col].dtype != 'object' and col not in ["ano"]]

    tipo_dado = st.selectbox("Selecione o tipo de dado que deseja comparar:", colunas_disponiveis)
    estado1 = st.selectbox("Selecione o primeiro estado:", estados, index=0)
    estado2 = st.selectbox("Selecione o segundo estado:", estados, index=1)
    ano = st.selectbox("Selecione o ano:", anos, index=len(anos)-1)

    # ==============================
    # 3️⃣ Filtro de dados
    # ==============================
    df_filtrado = df[(df["sigla_uf"].isin([estado1, estado2])) & (df["ano"] == ano)]

    if df_filtrado.empty:
        st.warning("⚠️ Não há dados disponíveis para essa combinação de estados e ano.")
    else:
        # ==============================
        # 4️⃣ Gráfico
        # ==============================
        fig, ax = plt.subplots(figsize=(8, 4))
        cores = ["#1f77b4", "#ff7f0e"]

        barras = ax.bar(df_filtrado["sigla_uf"], df_filtrado[tipo_dado] * 100, color=cores)

        # Adiciona rótulo dentro das barras
        for i, v in enumerate(df_filtrado[tipo_dado]):
            ax.text(i, (v * 100) / 2, f"{v * 100:.2f}%", ha="center", color="white", fontweight="bold")

        ax.set_title(f"{tipo_dado.replace('_', ' ').title()} por Estado ({ano})", fontsize=14, pad=15)
        ax.set_xlabel("Estado")
        ax.set_ylabel(f"{tipo_dado.replace('_', ' ').title()} (%)")

        st.pyplot(fig)

        # ==============================
        # 5️⃣ Tabela de apoio
        # ==============================
        st.write("### 🔢 Dados utilizados")
        st.dataframe(df_filtrado[["sigla_uf", "ano", tipo_dado]])

else:
    st.info("⬆️ Faça o upload do arquivo CSV para começar.")
