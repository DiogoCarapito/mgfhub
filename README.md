[![Github Actions Workflow](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml)

# mgfhub
Ferramenta de pesquisa e análise de indicadores dos Cuidados de Saúde Primarios portugueses

Inclui:

- pesquisa por palavras chave da descricao ou número do indicador
- filtrar por indicadores do IDE, IDG ou todos
- visualização em tabela ou cartões
- Relatórios de analise de desempenho da unidade e por equipa

Nova versão 2.0 disponível em [mgfhub.com](mgfhub.com)

## cheat sheet

### venv
create venv
```bash
python3 -m venv .venv
```

### activate venv
```bash
source .venv/bin/activate
```

### Dockerfile

#### build
```bash
docker build -t mgfhub:latest .
````

#### check image id
```bash
docker images
````

#### run with image id
```bash
docker run -p 8501:8501 mgfhub:latest
````
