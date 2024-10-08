# mgfhub

[![Github Actions Workflow](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml)

Ferramenta de pesquisa e análise de indicadores dos Cuidados de Saúde Primarios portugueses

Funcionalidades:

- pesquisa por palavras chave da descrição ou número do indicador
- filtrar por indicadores do IDE, IDG ou todos
- visualização em tabela ou cartões
- Relatórios de analise de desempenho da unidade, equipas e por profissional, com filtros e analise de evolução temporal

Nova versão 2.1 disponível em [mgfhub.com](mgfhub.com)

---

## cheat sheet

### create and activate .venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Dockerfile

build

```bash
docker build -t mgfhub:latest .
```

check image id

```bash
docker images
```

run with image id

```bash
docker run -p 8501:8501 mgfhub:latest
````
