from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PASTA_PROJETO = Path(__file__).resolve().parent
DADOS_TRATADOS = PASTA_PROJETO / "dados" / "diabetes_tratado.parquet"

COLUNAS_CATEGORICAS = [
    "PressaoAlta",
    "ColesterolAlto",
    "Fumante",
    "AVC",
    "ProblemaCardiaco",
    "AtividadeFisica",
    "ComeFrutas",
    "ComeLegumes",
    "ConsumoBebidaAlcoolica",
    "PlanoSaude",
    "SemDinheiroConsultas",
    "DificuldadeAndar",
    "Genero",
    "FaixaIdade",
    "Ensino",
    "FaixaRenda",
    "SaudeGeral",
]

COLUNAS_NUMERICAS = ["IMC", "DiasProblemasMentais", "DiasProblemasFisicos"]

DESCRICOES_NUMERICAS = {
    "IMC": "Índice de Massa Corporal. Ajuda a comparar a distribuição corporal entre pessoas com e sem diabetes.",
    "DiasProblemasMentais": "Quantidade de dias, nos últimos 30 dias, em que a saúde mental não esteve boa.",
    "DiasProblemasFisicos": "Quantidade de dias, nos últimos 30 dias, em que a saúde física não esteve boa.",
}

CORES_DIABETES = {
    "Não": "#2563eb",
    "Sim": "#dc2626",
}

MODOS_ANALISE = [
    "Dashboard executivo",
    "Explorador de fatores",
    "Comparação de grupos",
    "Tabela analítica",
]


@st.cache_data(show_spinner="Carregando dados tratados...")
def carregar_dados(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        st.error(
            "Arquivo de dados tratado não encontrado. "
            "Execute o notebook de tratamento ou adicione `dados/diabetes_tratado.parquet`."
        )
        st.stop()

    return pd.read_parquet(caminho)


def configurar_pagina():
    st.set_page_config(
        page_title="Análise de Diabetes",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.1rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(148, 163, 184, 0.45);
            border-radius: 8px;
            padding: 12px 16px;
        }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            color: inherit;
        }
        div[data-testid="stMetric"] label p {
            color: inherit;
            opacity: 0.75;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 2rem;
            line-height: 1.1;
        }
        .chart-description {
            margin: -0.45rem 0 1.15rem 0;
            padding: 0.55rem 0.7rem;
            border-left: 3px solid rgba(59, 130, 246, 0.85);
            color: inherit;
            opacity: 0.82;
            font-size: 0.92rem;
            line-height: 1.45;
        }
        .reading-block {
            margin: 0.25rem 0 1.4rem 0;
            padding: 0.95rem 1.05rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
            border-radius: 8px;
            color: inherit;
            line-height: 1.55;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def opcoes_ordenadas(serie: pd.Series) -> list:
    if hasattr(serie, "cat"):
        return list(serie.cat.categories)
    return sorted(serie.dropna().unique())


def filtrar_dados(dados: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    st.sidebar.title("Análise")
    modo = st.sidebar.radio("Modelo de visualização", options=MODOS_ANALISE)

    st.sidebar.divider()
    st.sidebar.header("Filtros")

    diabetes = st.sidebar.multiselect(
        "Diagnóstico",
        options=opcoes_ordenadas(dados["Diabetes"]),
        default=opcoes_ordenadas(dados["Diabetes"]),
    )
    genero = st.sidebar.multiselect(
        "Gênero",
        options=opcoes_ordenadas(dados["Genero"]),
        default=opcoes_ordenadas(dados["Genero"]),
    )
    faixa_idade = st.sidebar.multiselect(
        "Faixa de idade",
        options=opcoes_ordenadas(dados["FaixaIdade"]),
        default=opcoes_ordenadas(dados["FaixaIdade"]),
    )

    imc_minimo, imc_maximo = int(dados["IMC"].min()), int(dados["IMC"].max())
    intervalo_imc = st.sidebar.slider(
        "Intervalo de IMC",
        min_value=imc_minimo,
        max_value=imc_maximo,
        value=(imc_minimo, imc_maximo),
    )

    dados_filtrados = dados[
        dados["Diabetes"].isin(diabetes)
        & dados["Genero"].isin(genero)
        & dados["FaixaIdade"].isin(faixa_idade)
        & dados["IMC"].between(intervalo_imc[0], intervalo_imc[1])
    ]
    return dados_filtrados, modo


def formatar_percentual(valor: float) -> str:
    return f"{valor:.1%}".replace(".", ",")


def formatar_percentual_opcional(valor: float | None) -> str:
    if valor is None or pd.isna(valor):
        return "sem registros no filtro"
    return formatar_percentual(valor)


def formatar_decimal(valor: float) -> str:
    return f"{valor:.1f}".replace(".", ",")


def formatar_decimal_opcional(valor: float | None) -> str:
    if valor is None or pd.isna(valor):
        return "sem registros no filtro"
    return formatar_decimal(valor)


def formatar_pp(valor: float) -> str:
    return f"{valor * 100:.1f} p.p.".replace(".", ",")


def exibir_descricao(texto: str):
    st.markdown(f'<div class="chart-description">{texto}</div>', unsafe_allow_html=True)


def calcular_resumo(dados: pd.DataFrame) -> dict:
    total = len(dados)
    if total == 0:
        return {
            "total": 0,
            "taxa_diabetes": 0,
            "imc_medio": 0,
            "pressao_alta": 0,
            "colesterol_alto": 0,
        }

    return {
        "total": total,
        "taxa_diabetes": dados["Diabetes"].eq("Sim").mean(),
        "imc_medio": dados["IMC"].mean(),
        "pressao_alta": dados["PressaoAlta"].eq("Sim").mean(),
        "colesterol_alto": dados["ColesterolAlto"].eq("Sim").mean(),
    }


def exibir_cabecalho(modo: str):
    st.title("Indicadores de diabetes")
    st.caption(
        f"{modo} com base no dataset Diabetes Health Indicators tratado no projeto."
    )


def exibir_metricas(dados: pd.DataFrame):
    resumo = calcular_resumo(dados)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Registros", f"{resumo['total']:,}".replace(",", "."))
    col2.metric("Diabetes", formatar_percentual(resumo["taxa_diabetes"]))
    col3.metric("IMC médio", formatar_decimal(resumo["imc_medio"]))
    col4.metric("Pressão alta", formatar_percentual(resumo["pressao_alta"]))
    col5.metric("Colesterol alto", formatar_percentual(resumo["colesterol_alto"]))


def calcular_taxa_por_diagnostico(
    dados: pd.DataFrame,
    coluna: str,
    valor: str = "Sim",
) -> pd.DataFrame:
    return (
        dados.assign(PossuiIndicador=dados[coluna].eq(valor))
        .groupby("Diabetes", observed=False)
        .agg(Taxa=("PossuiIndicador", "mean"), Registros=("PossuiIndicador", "size"))
        .reset_index()
    )


def obter_taxa_por_diagnostico(
    dados: pd.DataFrame,
    coluna: str,
    diagnostico: str,
) -> float | None:
    resumo = calcular_taxa_por_diagnostico(dados, coluna)
    taxa = resumo.loc[resumo["Diabetes"].eq(diagnostico), "Taxa"]
    if taxa.empty:
        return None
    return taxa.iloc[0]


def resumir_taxa_por_categoria(dados: pd.DataFrame, coluna: str) -> pd.DataFrame:
    return (
        dados.assign(Diabetico=dados["Diabetes"].eq("Sim"))
        .groupby(coluna, observed=False)
        .agg(TaxaDiabetes=("Diabetico", "mean"), Registros=("Diabetico", "size"))
        .reset_index()
        .sort_values("TaxaDiabetes", ascending=False)
    )


def resumir_matriz_comparativa(
    dados: pd.DataFrame,
    linhas: str,
    colunas: str,
) -> pd.DataFrame:
    if linhas == colunas:
        return pd.DataFrame()

    return (
        dados.assign(Diabetico=dados["Diabetes"].eq("Sim"))
        .groupby([linhas, colunas], observed=False)
        .agg(TaxaDiabetes=("Diabetico", "mean"), Registros=("Diabetico", "size"))
        .reset_index()
    )


def exibir_analise_geral(dados: pd.DataFrame):
    resumo = calcular_resumo(dados)
    _, ranking = grafico_ranking_fatores(dados)

    taxa_pressao_diabetes = obter_taxa_por_diagnostico(dados, "PressaoAlta", "Sim")
    taxa_pressao_sem_diabetes = obter_taxa_por_diagnostico(dados, "PressaoAlta", "Não")
    taxa_colesterol_diabetes = obter_taxa_por_diagnostico(dados, "ColesterolAlto", "Sim")
    taxa_colesterol_sem_diabetes = obter_taxa_por_diagnostico(dados, "ColesterolAlto", "Não")

    imc_por_diagnostico = dados.groupby("Diabetes", observed=False)["IMC"].mean()
    imc_diabetes = imc_por_diagnostico.get("Sim")
    imc_sem_diabetes = imc_por_diagnostico.get("Não")

    principal_fator = ranking.iloc[0]
    st.subheader("Leitura geral da análise")
    st.markdown(
        f"""
        <div class="reading-block">
        Este painel resume <strong>{resumo["total"]:,} registros</strong> e mostra uma taxa de diabetes de
        <strong>{formatar_percentual(resumo["taxa_diabetes"])}</strong> no recorte atual. A leitura principal é
        comparar como os indicadores mudam entre grupos: quando a taxa sobe muito em uma categoria,
        há um sinal de associação com o diagnóstico.
        <br><br>
        Os pontos que mais pedem atenção são os indicadores clínicos e de condição geral de saúde.
        Entre pessoas com diabetes, <strong>{formatar_percentual_opcional(taxa_pressao_diabetes)}</strong>
        têm pressão alta, contra <strong>{formatar_percentual_opcional(taxa_pressao_sem_diabetes)}</strong>
        entre pessoas sem diabetes. Para colesterol alto, a comparação é
        <strong>{formatar_percentual_opcional(taxa_colesterol_diabetes)}</strong> contra
        <strong>{formatar_percentual_opcional(taxa_colesterol_sem_diabetes)}</strong>.
        O IMC médio também muda entre os grupos: <strong>{formatar_decimal_opcional(imc_diabetes)}</strong>
        no grupo com diabetes e <strong>{formatar_decimal_opcional(imc_sem_diabetes)}</strong> no grupo sem diabetes.
        <br><br>
        No ranking de associação, a variável que mais separa os grupos é
        <strong>{principal_fator["Variável"]}</strong>, com diferença de
        <strong>{formatar_pp(principal_fator["Diferença vs menor grupo"])}</strong> entre o grupo de maior
        e o de menor taxa. Isso indica correlação/associação nos dados observados, mas não prova causa:
        a base mostra padrões de coexistência entre indicadores, não o efeito isolado de cada fator.
        </div>
        """,
        unsafe_allow_html=True,
    )


def exibir_analise_fator(dados: pd.DataFrame, coluna_categoria: str, coluna_numerica: str):
    resumo_categoria = resumir_taxa_por_categoria(dados, coluna_categoria)
    maior = resumo_categoria.iloc[0]
    menor = resumo_categoria.iloc[-1]

    numerico = (
        dados.groupby("Diabetes", observed=False)[coluna_numerica]
        .agg(["mean", "median"])
        .rename(columns={"mean": "Média", "median": "Mediana"})
    )
    media_diabetes = numerico.loc["Sim", "Média"] if "Sim" in numerico.index else None
    media_sem_diabetes = numerico.loc["Não", "Média"] if "Não" in numerico.index else None

    st.subheader("Análise do fator selecionado")
    st.markdown(
        f"""
        - Em **{coluna_categoria}**, o grupo com maior taxa de diabetes é **{maior[coluna_categoria]}**, com **{formatar_percentual(maior["TaxaDiabetes"])}**.
        - O grupo com menor taxa é **{menor[coluna_categoria]}**, com **{formatar_percentual(menor["TaxaDiabetes"])}**.
        - A diferença entre esses extremos é de **{formatar_pp(maior["TaxaDiabetes"] - menor["TaxaDiabetes"])}**.
        - Para **{coluna_numerica}**, a média no grupo com diabetes é **{formatar_decimal_opcional(media_diabetes)}**; no grupo sem diabetes é **{formatar_decimal_opcional(media_sem_diabetes)}**.
        """
    )
    st.caption(
        "O indicador numérico é uma variável quantitativa. O boxplot compara mediana, dispersão e valores extremos entre os diagnósticos."
    )


def exibir_analise_comparacao(
    dados: pd.DataFrame,
    linhas: str,
    colunas: str,
    minimo_registros: int = 30,
):
    matriz = resumir_matriz_comparativa(dados, linhas, colunas)
    matriz_relevante = matriz[matriz["Registros"].ge(minimo_registros)]

    if matriz_relevante.empty:
        st.warning(
            "Não há combinações com volume suficiente para uma leitura comparativa estável."
        )
        return

    maior = matriz_relevante.sort_values("TaxaDiabetes", ascending=False).iloc[0]
    menor = matriz_relevante.sort_values("TaxaDiabetes", ascending=True).iloc[0]

    st.subheader("Análise da comparação")
    st.markdown(
        f"""
        - Considerando combinações com pelo menos **{minimo_registros} registros**, a maior taxa aparece em **{linhas} = {maior[linhas]}** e **{colunas} = {maior[colunas]}**, com **{formatar_percentual(maior["TaxaDiabetes"])}**.
        - A menor taxa aparece em **{linhas} = {menor[linhas]}** e **{colunas} = {menor[colunas]}**, com **{formatar_percentual(menor["TaxaDiabetes"])}**.
        - A distância entre essas combinações é de **{formatar_pp(maior["TaxaDiabetes"] - menor["TaxaDiabetes"])}**.
        """
    )


def grafico_distribuicao_diabetes(dados: pd.DataFrame):
    resumo = (
        dados["Diabetes"]
        .value_counts(normalize=True)
        .rename_axis("Diabetes")
        .reset_index(name="Percentual")
    )
    fig = px.bar(
        resumo,
        x="Diabetes",
        y="Percentual",
        color="Diabetes",
        text=resumo["Percentual"].map(formatar_percentual),
        color_discrete_map=CORES_DIABETES,
    )
    fig.update_layout(yaxis_tickformat=".0%", showlegend=False, height=340)
    fig.update_traces(textposition="inside", textfont={"color": "#ffffff"}, cliponaxis=False)
    return fig


def grafico_taxa_por_categoria(dados: pd.DataFrame, coluna: str, altura: int = 420):
    resumo = resumir_taxa_por_categoria(dados, coluna)
    fig = px.bar(
        resumo,
        x=coluna,
        y="TaxaDiabetes",
        color="TaxaDiabetes",
        text=resumo["TaxaDiabetes"].map(formatar_percentual),
        color_continuous_scale=["#16a34a", "#f59e0b", "#dc2626"],
        hover_data={"Registros": True, "TaxaDiabetes": ":.1%"},
    )
    fig.update_layout(yaxis_tickformat=".0%", coloraxis_showscale=False, height=altura)
    fig.update_traces(textposition="inside", textfont={"color": "#ffffff"}, cliponaxis=False)
    return fig


def grafico_boxplot_numerico(dados: pd.DataFrame, coluna: str):
    fig = px.box(
        dados,
        x="Diabetes",
        y=coluna,
        color="Diabetes",
        points=False,
        color_discrete_map=CORES_DIABETES,
    )
    fig.update_layout(showlegend=False, height=420)
    return fig


def grafico_ranking_fatores(dados: pd.DataFrame):
    linhas = []
    for coluna in COLUNAS_CATEGORICAS:
        resumo = resumir_taxa_por_categoria(dados, coluna)
        if resumo.empty:
            continue
        maior = resumo.iloc[0]
        menor = resumo.iloc[-1]
        linhas.append(
            {
                "Variável": coluna,
                "Grupo de maior taxa": maior[coluna],
                "Taxa de diabetes": maior["TaxaDiabetes"],
                "Diferença vs menor grupo": maior["TaxaDiabetes"] - menor["TaxaDiabetes"],
                "Registros": maior["Registros"],
            }
        )

    ranking = pd.DataFrame(linhas).sort_values(
        "Diferença vs menor grupo", ascending=False
    )
    fig = px.bar(
        ranking.head(10),
        x="Diferença vs menor grupo",
        y="Variável",
        orientation="h",
        color="Taxa de diabetes",
        text=ranking.head(10)["Diferença vs menor grupo"].map(formatar_percentual),
        color_continuous_scale=["#16a34a", "#f59e0b", "#dc2626"],
        hover_data={
            "Grupo de maior taxa": True,
            "Taxa de diabetes": ":.1%",
            "Diferença vs menor grupo": ":.1%",
            "Registros": True,
        },
    )
    fig.update_layout(
        xaxis_tickformat=".0%",
        xaxis_title="Diferença entre maior e menor taxa de diabetes",
        yaxis={"categoryorder": "total ascending"},
        yaxis_title="Variável analisada",
        coloraxis_showscale=False,
        height=480,
    )
    fig.update_traces(textposition="inside", textfont={"color": "#ffffff"})
    return fig, ranking


def grafico_heatmap_comparativo(dados: pd.DataFrame, linhas: str, colunas: str):
    matriz = resumir_matriz_comparativa(dados, linhas, colunas)
    if matriz.empty:
        return None

    fig = px.density_heatmap(
        matriz,
        x=colunas,
        y=linhas,
        z="TaxaDiabetes",
        text_auto=".0%",
        color_continuous_scale=["#f8fafc", "#f59e0b", "#dc2626"],
    )
    fig.update_layout(coloraxis_colorbar={"tickformat": ".0%"}, height=520)
    return fig


def exibir_dashboard_executivo(dados: pd.DataFrame):
    exibir_metricas(dados)
    exibir_analise_geral(dados)
    col1, col2 = st.columns([0.9, 1.4])
    with col1:
        st.subheader("Distribuição do diagnóstico")
        st.plotly_chart(grafico_distribuicao_diabetes(dados), use_container_width=True)
        exibir_descricao(
            "Mostra a proporção de registros com e sem diabetes dentro dos filtros atuais. "
            "Use este gráfico para entender o tamanho relativo dos grupos comparados."
        )
    with col2:
        st.subheader("Taxa por faixa de idade")
        st.plotly_chart(
            grafico_taxa_por_categoria(dados, "FaixaIdade", altura=340),
            use_container_width=True,
        )
        exibir_descricao(
            "Mostra a taxa de diabetes em cada faixa etária. Barras mais altas indicam "
            "grupos em que a presença de diabetes é mais frequente no recorte filtrado."
        )

    st.subheader("Ranking de associação com diabetes")
    fig, ranking = grafico_ranking_fatores(dados)
    st.plotly_chart(fig, use_container_width=True)
    exibir_descricao(
        "Origem da análise: para cada variável, o app calcula a taxa de diabetes em todos "
        "os seus grupos e compara o grupo com maior taxa contra o grupo com menor taxa. "
        "A barra mostra essa diferença em pontos percentuais."
    )
    st.caption(
        "Exemplo: em `SaudeGeral`, compara-se a categoria com maior taxa de diabetes "
        "contra a categoria com menor taxa dentro dessa mesma variável."
    )
    st.subheader("Detalhe do ranking")
    st.dataframe(
        ranking.head(8).style.format(
            {
                "Taxa de diabetes": "{:.1%}",
                "Diferença vs menor grupo": "{:.1%}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def exibir_explorador_fatores(dados: pd.DataFrame):
    exibir_metricas(dados)
    st.markdown(
        "Explore os gráficos abaixo para investigar, com mais detalhe, como cada fator "
        "categórico se relaciona com a taxa de diabetes e como os indicadores numéricos "
        "se distribuem entre pessoas com e sem diabetes."
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        coluna_categoria = st.selectbox(
            "Fator categórico",
            options=COLUNAS_CATEGORICAS,
            index=COLUNAS_CATEGORICAS.index("PressaoAlta"),
        )
        st.plotly_chart(
            grafico_taxa_por_categoria(dados, coluna_categoria),
            use_container_width=True,
        )
        exibir_descricao(
            "O fator categórico separa os registros em grupos, como pressão alta, "
            "gênero, faixa de idade ou renda. O gráfico mostra a taxa de diabetes "
            "em cada grupo desse fator."
        )
    with col2:
        coluna_numerica = st.selectbox("Indicador numérico", options=COLUNAS_NUMERICAS)
        st.plotly_chart(
            grafico_boxplot_numerico(dados, coluna_numerica),
            use_container_width=True,
        )
        exibir_descricao(DESCRICOES_NUMERICAS[coluna_numerica])

    exibir_analise_fator(dados, coluna_categoria, coluna_numerica)

    st.subheader("Amostra dos grupos do fator selecionado")
    exibir_descricao(
        "A tabela detalha o gráfico acima: cada linha é um grupo do fator escolhido, "
        "`TaxaDiabetes` é a proporção de pessoas com diabetes naquele grupo e "
        "`Registros` indica o tamanho da amostra usada no cálculo."
    )
    resumo = resumir_taxa_por_categoria(dados, coluna_categoria)
    st.dataframe(
        resumo.style.format({"TaxaDiabetes": "{:.1%}"}),
        use_container_width=True,
        hide_index=True,
    )


def exibir_comparacao_grupos(dados: pd.DataFrame):
    exibir_metricas(dados)
    col1, col2 = st.columns(2)
    with col1:
        linhas = st.selectbox(
            "Linhas",
            options=COLUNAS_CATEGORICAS,
            index=COLUNAS_CATEGORICAS.index("FaixaIdade"),
        )
    with col2:
        colunas = st.selectbox(
            "Colunas",
            options=COLUNAS_CATEGORICAS,
            index=COLUNAS_CATEGORICAS.index("SaudeGeral"),
        )

    if linhas == colunas:
        st.info(
            "Escolha variáveis diferentes para linhas e colunas. Comparar uma variável "
            "com ela mesma não forma uma matriz útil; para analisar esse fator isolado, "
            "use o modo Explorador de fatores."
        )
        return

    st.plotly_chart(
        grafico_heatmap_comparativo(dados, linhas, colunas),
        use_container_width=True,
    )
    exibir_descricao(
        "A matriz cruza duas variáveis categóricas. Cada célula mostra a taxa de "
        "diabetes naquela combinação de grupos. Tons mais intensos indicam taxas maiores."
    )
    exibir_analise_comparacao(dados, linhas, colunas)


def exibir_tabela_analitica(dados: pd.DataFrame):
    exibir_metricas(dados)
    exibir_descricao(
        "Esta tabela mostra os registros após todos os filtros aplicados na barra lateral. "
        "Ela serve para auditar os dados por trás dos gráficos: cada linha representa uma "
        "pessoa entrevistada e cada coluna representa uma variável tratada no projeto."
    )
    colunas = st.multiselect(
        "Colunas exibidas",
        options=list(dados.columns),
        default=[
            "Diabetes",
            "PressaoAlta",
            "ColesterolAlto",
            "IMC",
            "SaudeGeral",
            "Genero",
            "FaixaIdade",
            "FaixaRenda",
        ],
    )
    exibir_descricao(
        "Como ler: `Sim` e `Não` indicam presença ou ausência do atributo; `IMC` e os dias "
        "de problemas físicos/mentais são variáveis numéricas; faixas de idade, ensino e "
        "renda são categorias ordenadas."
    )
    st.dataframe(dados[colunas], use_container_width=True, hide_index=True)
    csv = dados[colunas].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar dados filtrados",
        data=csv,
        file_name="diabetes_filtrado.csv",
        mime="text/csv",
    )


def main():
    configurar_pagina()
    dados = carregar_dados(DADOS_TRATADOS)
    dados_filtrados, modo = filtrar_dados(dados)

    exibir_cabecalho(modo)

    if dados_filtrados.empty:
        st.warning("Nenhum registro encontrado com os filtros selecionados.")
        st.stop()

    if modo == "Dashboard executivo":
        exibir_dashboard_executivo(dados_filtrados)
    elif modo == "Explorador de fatores":
        exibir_explorador_fatores(dados_filtrados)
    elif modo == "Comparação de grupos":
        exibir_comparacao_grupos(dados_filtrados)
    else:
        exibir_tabela_analitica(dados_filtrados)


if __name__ == "__main__":
    main()
