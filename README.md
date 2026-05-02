# Análise estatística de base de dados de diabetes

Projeto de análise exploratória e estatística desenvolvido com base no
dataset **Diabetes Health Indicators** disponível no Kaggle, originado
da pesquisa BRFSS 2015 conduzida pelo CDC (Centers for Disease Control
and Prevention).

A base contém 253.680 respostas de uma pesquisa de saúde comportamental
aplicada nos Estados Unidos, com 22 variáveis que combinam indicadores
clínicos, hábitos de vida e dados demográficos. A variável-alvo
(`Diabetes_binary`) indica a presença ou ausência de diabetes/pré-diabetes.

O objetivo do projeto foi explorar e entender a distribuição dos dados,
identificar padrões entre as variáveis e extrair insights sobre os
indicadores mais associados ao diagnóstico de diabetes — sem uso de
modelos preditivos.

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

## Um pouco mais sobre a base

[Clique aqui](referencias/01_dicionario_de_dados.md) para ver o dicionário de dados da base utilizada.


