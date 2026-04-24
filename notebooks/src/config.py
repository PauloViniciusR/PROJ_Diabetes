from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_DADOS = PASTA_PROJETO / "dados"

# caminho para os arquivos de dados de seu projeto
DADOS_ORIGINAIS = PASTA_DADOS / "diabetes.zip"
DADOS_TRATADOS = PASTA_DADOS / "diabetes_tratado.parquet"

# outros caminhos
PASTA_IMAGENS = PASTA_PROJETO / "imagens"
