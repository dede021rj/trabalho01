import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1️⃣ Título do app
# ==============================
st.title("📊 Comparativo de Despesa Total / PIB por Estado")
st.write("Envie o arquivo CSV com os dados orçamentários para começar a análise.")

# ==============================
# 2️⃣ Upload do arquivo
# ==============================
arquivo = st.file_uploader("📂 Envie o arquivo CSV", type=["csv"])

if arquivo is not None:
    try:
        # Lê o arquivo enviado
        df = pd.read_csv(arquivo)

        # Mostra algumas informações
        st.success("✅ Arquivo carregado com sucesso!")
        st.write("### 🔍 Visualização inicial dos dados")
        st.dataframe(df.head())

        # Confirma se as colunas necessárias existem
        colunas_necessarias = {"sigla_uf", "ano", "despesa_total_pib"}
        if not colunas_necessarias.issubset(df.columns):
            st.error("❌ O arquivo CSV não contém as colunas necessárias: 'sigla_uf', 'ano', 'despesa_total_pib'.")
        else:
            # ==============================
            # 3️⃣ Seleção de filtros
            # ==============================
            estados = sorted(df["sigla_uf"].dropna().unique())
            anos = sorted(df["ano"].dropna().unique())

            col1, col2 = st.columns(2)
            with col1:
                estado1 = st.selectbox("Selecione o primeiro estado:", estados)
            with col2:
                estado2 = st.selectbox("Selecione o segundo estado:", estados, index=min(1, len(estados)-1))

            ano = st.selectbox("Selecione o ano:", anos, index=len(anos)-1)

            # Filtra os dados
            df_filtrado = df[(df["sigla_uf"].isin([estado1, estado2])) & (df["ano"] == ano)]

            if df_filtrado.empty:
                st.warning("⚠️ Não há dados disponíveis para essa combinação de estados e ano.")
            else:
                # ==============================
                # 4️⃣ Criação do gráfico
                # ==============================
                fig, ax = plt.subplots(figsize=(8, 4))
                cores = ["#1f77b4", "#ff7f0e"]

                barras = ax.bar(df_filtrado["sigla_uf"], df_filtrado["despesa_total_pib"] * 100, color=cores)

                for i, v in enumerate(df_filtrado["despesa_total_pib"]):
                    ax.text(i, v / 2, f"{v * 100:.2f}%", ha="center", color="black", fontweight="bold")


                ax.set_title(f"Percentual da Despesa Total em relação ao PIB ({ano})", fontsize=14, pad=15)
                ax.set_xlabel("Estado")
                ax.set_ylabel("Despesa Total / PIB (%)")

                st.pyplot(fig)

                # ==============================
                # 5️⃣ Dados utilizados
                # ==============================
                st.write("### 📄 Dados utilizados")
                st.dataframe(df_filtrado[["sigla_uf", "ano", "despesa_total_pib"]])

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")

else:
    st.info("⬆️ Por favor, envie um arquivo CSV para começar.")
