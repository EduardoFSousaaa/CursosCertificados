# Projeto Extensão para certificados de cursos
## __Construido por: Eduardo Frisch Sousa__
## Tecnologias usadas: HTML, CSS, Javascript,Python
* BootsTrap 5 (Css e Javascript)
* Python Blibiotecas:  
  &emsp;Flask com blueprints  
  &emsp;Templates JINJA
# Instalação:
* USE python.exe -m  Antes dos pip se necessario colocar na raiz do terminal(Pode esta errado a descrição)
* pip install --pre Flask
* pip install --pre blueprintpy
* pip install --pre Jinja2
* pip install --pre SQLAlchemy 
* pip install --pre ntplib 
* alterar variavel root path

## Rodando com Docker

# 1. Subir os containers
```bash
docker compose up --build -d
```

# 2. Gerar o arquivo de migration (só precisa fazer uma vez por mudança de schema)
```bash
docker compose exec web uv run flask --app wsgi db migrate -m "initial schema"
```

# 3. Aplicar a migration no banco
```bash
docker compose exec web uv run flask --app wsgi db upgrade
```

# 4. Popular usuários base
```bash
docker compose exec web uv run flask --app wsgi seed
```

A aplicação sobe em http://localhost:8000.
