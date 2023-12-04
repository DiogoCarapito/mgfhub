[![Github Actions Workflow](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/mgfhub/actions/workflows/main.yaml)

# mgfhub
Ferramenta de pesquisa de indicadores de cuidados de saúde primarios 

Inclui:

- pesquisa por palavras chave da descricao do indicador ou código do indicador
- filtrar por com impacto no IDG, sem impacto no IDG ou todos
- visualização em tabela ou cartões 
- visualização de indicadores com impacto do IDG em sunburst

Um projeto em desenvolvimento

Disponível em [mgfhub.com](mgfhub.com)




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
docker build -t Home:latest .
````

#### check image id
```bash
docker images
````

#### run with image id
```bash
docker run -p 8501:8501 Home:latest
````


