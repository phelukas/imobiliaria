# imobiliaria

Sistema De Venda de Imóveis.

## Instalação:

0. Criando e Ativando Ambiente virtual:

```bash
python3 -m venv venv

(linux) source venv/bin/activate
(Windows) venv/Scripts/activate 

```
1. Instalar dependências:

```bash
pip install -r requirements.txt
```

2. Sincronize a base de dados:

```bash
python manage.py migrate
```

3. Crie um usuário (Administrador do sistema):

```bash
python manage.py createsuperuser
```
4. Teste a instalação carregando o servidor de desenvolvimento (http://localhost:8000 no navegador):

```bash
python manage.py runserver
```
