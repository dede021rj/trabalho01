import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ============================
# 1️⃣ Configuração inicial
# ============================
st.set_page_config(page_title="Comparativo de Despesas da Justiça", layout="wide")
st.title("📊 Comparativo de Despesas da Justiça Estadual")

# ============================
# 2️⃣ Upload do arquivo CSV
# ============================
arquivo_csv = st.file_uploader("Envie o arquivo CSV com os dados", type=["csv"])

if arquivo_csv is not None:
    df = pd.read_csv(arquivo_csv)
    df.columns = df.columns.str.strip().str.lower()  # normaliza nomes

    if df.empty:
        st.error("❌ O arquivo CSV está vazio.")
    elif "sigla_uf" not in df.columns:
        st.error("❌ A coluna 'sigla_uf' (Estados) não foi encontrada no arquivo CSV.")
    elif "ano" not in df.columns:
        st.error("❌ A coluna 'ano' não foi encontrada no arquivo CSV.")
    else:
        # ============================
        # 3️⃣ Filtros interativos
        # ============================
        anos_disponiveis = sorted(df["ano"].dropna().unique())
        ano_escolhido = st.selectbox("Selecione o ano para análise:", anos_disponiveis)

        df_ano = df[df["ano"] == ano_escolhido]

        estados_disponiveis = sorted(df_ano["sigla_uf"].dropna().unique())
        estados_escolhidos = st.multiselect(
            "Selecione os estados para comparar:",
            estados_disponiveis,
            default=estados_disponiveis[:2] if len(estados_disponiveis) >= 2 else estados_disponiveis
        )

        # ============================
        # 4️⃣ Seleção do tipo de dado
        # ============================
        opcoes_dados = {
            "Despesa Total / PIB (%)": "despesa_total_pib",
            "Despesa Média por Magistrado": "despesa_media_magistrado",
            "Despesa Total da Justiça Estadual (Bilhões)": "despesa_total_justica_estadual"
        }

        tipo_dado = st.selectbox("Selecione o tipo de dado para comparar:", list(opcoes_dados.keys()))
        coluna_escolhida = opcoes_dados[tipo_dado]

        if coluna_escolhida not in df.columns:
            st.error(f"❌ A coluna '{coluna_escolhida}' não foi encontrada no arquivo CSV.")
        else:
            df_filtrado = df_ano[df_ano["sigla_uf"].isin(estados_escolhidos)]

            if df_filtrado.empty:
                st.warning("⚠️ Nenhum dado encontrado para os estados selecionados.")
            else:

                # ============================
                # 5️⃣ Tratamento especial para valores em bilhões
                # ============================
                if coluna_escolhida == "despesa_total_justica_estadual":
                    df_filtrado = df_filtrado.copy()
                    df_filtrado["valor_grafico"] = df_filtrado[coluna_escolhida] / 1e9
                    label_y = "Despesa (em bilhões de R$)"
                else:
                    df_filtrado["valor_grafico"] = df_filtrado[coluna_escolhida]
                    label_y = tipo_dado

                # ============================
                # 6️⃣ Gráfico
                # ============================
                fig, ax = plt.subplots(figsize=(9, 5))
                cores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b"]

                ax.bar(
                    df_filtrado["sigla_uf"],
                    df_filtrado["valor_grafico"],
                    color=cores[:len(df_filtrado)]
                )

                ax.set_title(f"{tipo_dado} ({ano_escolhido})", fontsize=16, fontweight="bold")
                ax.set_xlabel("Estado", fontsize=12)
                ax.set_ylabel(label_y, fontsize=12)

                # 🔥 Formatação do eixo Y sem pontos e sem notação científica
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"{int(x)}"))

                # ❌ NÃO colocar valores dentro das barras
                # (Removido conforme seu pedido)

                st.pyplot(fig)

                # ============================
                # 7️⃣ Dados usados
                # ============================
                st.write("### 🔢 Dados utilizados")
                st.dataframe(df_filtrado[["ano", "sigla_uf", coluna_escolhida]])

else:
    st.info("⬆️ Envie um arquivo CSV para começar a análise.")
