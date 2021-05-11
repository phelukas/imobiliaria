# imobiliaria

Sistema De Venda de Imóveis.

## Instalação:

0. Instalar dependências:

```bash
pip install -r requirements.txt
```

1. Sincronize a base de dados:

```bash
python manage.py migrate
```

2. Crie um usuário (Administrador do sistema):

```bash
python manage.py createsuperuser
```
3. Teste a instalação carregando o servidor de desenvolvimento (http://localhost:8000 no navegador):

```bash
python manage.py runserver
```
