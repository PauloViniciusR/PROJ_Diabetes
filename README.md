# Análise estatística de base de dados de diabetes

Projeto de análise exploratória e estatística desenvolvido com base no
dataset **Diabetes Health Indicators**, disponível no Kaggle e originado
da pesquisa BRFSS 2015 conduzida pelo CDC (Centers for Disease Control
and Prevention).

A base reúne respostas de uma pesquisa de saúde comportamental aplicada
nos Estados Unidos, combinando indicadores clínicos, hábitos de vida e
dados demográficos. O objetivo foi explorar a distribuição dos dados e
identificar padrões entre as variáveis e o diagnóstico de diabetes.

![imagem](imagens/diabetes.jpg)

## Organização do projeto

```
├── .gitignore         <- Arquivos e diretórios a serem ignorados pelo Git
├── ambiente.yml       <- O arquivo de requisitos para reproduzir o ambiente de análise
├── LICENSE            <- Licença de código aberto (MIT)
├── README.md          <- README principal para desenvolvedores que usam este projeto.
|
├── dados              <- Arquivos de dados para o projeto.
|
├── notebooks          <- Jupyter Notebooks.
│
|   └──src             <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      ├── config.py    <- Configurações básicas do projeto
|      └── estatistica.py  <- Funções criadas especificamente para este projeto
|
├── referencias        <- Dicionários de dados.
|
├── imagens            <- Imagens utilizadas no projeto
```

## Configuração do ambiente

1. Faça o clone do repositório.

    ```bash
    git clone git@github.com:exemplohashtag/projeto_teste.git
    ```

2. Crie um ambiente virtual para o seu projeto utilizando o `conda`.

   ```bash
   conda env create -f ambiente.yml --name estatistica
   ```

## Executando o painel Streamlit

O projeto também possui um painel interativo em Streamlit para explorar a base
tratada.

Para executar localmente:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para publicar no Streamlit Community Cloud:

1. Envie o repositório para o GitHub.
2. Acesse <https://share.streamlit.io/>.
3. Crie um novo app apontando para este repositório.
4. Defina o arquivo principal como `app.py`.
5. Confirme que o arquivo `dados/diabetes_tratado.parquet` está no repositório.

## Um pouco mais sobre a base

[Clique aqui](referencias/01_dicionario_de_dados.md) para ver o dicionário de dados da base utilizada.

