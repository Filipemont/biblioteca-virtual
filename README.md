# Biblioteca Unichristus

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue.svg)](https://www.docker.com/)

Um sistema de gerenciamento de biblioteca baseado na web, projetado para a Unichristus. O sistema permite que os usuários gerenciem livros, usuários e funções. Ele também inclui recursos como autenticação de usuário, recuperação de senha e integração com o Google Gemini para funcionalidades de IA.

## Recursos

- **Autenticação de Usuário:** Registro de usuário, login e autenticação segura com 2FA (Autenticação de Dois Fatores).
- **Recuperação de Senha:** Funcionalidade de recuperação de senha por e-mail.
- **Gerenciamento de Usuários e Funções:** Gerenciamento de usuários e atribuição de funções (por exemplo, administrador, bolsista).
- **Gerenciamento de Livros:** Operações CRUD (Criar, Ler, Atualizar, Excluir) para livros.
- **Painel de Administração:** Um painel de administração para gerenciar o sistema de forma eficiente.
- **Integração com IA:** Integração com o Google Gemini para resumo de livros.
- **Armazenamento de Arquivos:** Utiliza o MinIO para armazenamento de arquivos, como capas de livros.

## Tecnologias Utilizadas

- **Backend:** Python, Flask, Gunicorn
- **Banco de Dados:** PostgreSQL, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript, Bootstrap, AdminLTE3
- **Autenticação:** Flask-Login, bcrypt, pyotp
- **Armazenamento de Arquivos:** MinIO
- **IA:** Google Generative AI (Gemini)
- **Containerização:** Docker, Docker Compose

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Começando

Para configurar e executar o projeto localmente, siga estas etapas:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/biblioteca-unich.git
   cd biblioteca-unich
   ```

2. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
     ```
     SECRET_KEY=sua-chave-secreta
     POSTGRES_USER=seu-usuario
     POSTGRES_PASSWORD=sua-senha
     POSTGRES_DB=seu-banco-de-dados
     MINIO_ROOT_USER=minio-admin
     MINIO_ROOT_PASSWORD=minio-secret-key
     MAIL_SERVER=smtp.example.com
     MAIL_PORT=587
     MAIL_USE_TLS=True
     MAIL_USERNAME=seu-email
     MAIL_PASSWORD=sua-senha-de-email
     GEMINI_API_KEY=sua-api-key-do-gemini
     ```

3. **Inicie os serviços de infraestrutura:**
   - Este comando irá iniciar os contêineres do PostgreSQL e MinIO.
   ```bash
   docker compose -f docker-compose-infra.yml up -d
   ```

4. **Inicie a aplicação:**
   - Este comando irá construir e iniciar o contêiner da aplicação Flask.
   ```bash
   docker compose up --build
   ```

5. **Acesse a aplicação:**
   - Abra seu navegador e acesse [http://localhost:5000](http://localhost:5000).

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```
├── app/                  # Contém o código-fonte da aplicação
│   ├── controller/       # Lógica de negócios e controladores
│   ├── ext/              # Extensões e utilitários do Flask
│   ├── forms/            # Definições de formulários WTForms
│   ├── model/            # Modelos de banco de dados SQLAlchemy
│   ├── service/          # Serviços (por exemplo, serviço do Gemini)
│   ├── static/           # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/        # Templates HTML Jinja2
│   └── view/             # Views do Flask
├── docker-compose.yml    # Define os serviços da aplicação
├── docker-compose-infra.yml # Define os serviços de infraestrutura (PostgreSQL, MinIO)
├── Dockerfile            # Define a imagem Docker para a aplicação
├── requirements.txt      # Dependências do Python
└── README.md             # Este arquivo
```

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
