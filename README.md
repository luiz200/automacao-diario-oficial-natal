# automacao-diario-oficial-natal
Automação de coleta de dados do Diário Oficial de Natal-RN

## 📌 Descrição
Este projeto tem como objetivo automatizar a coleta de dados publicados no Diário Oficial do Município de Natal-RN.  
A aplicação realiza o download, extração e armazenamento das informações em um banco de dados, permitindo consultas e análises posteriores.

## 🚀 Tecnologias Utilizadas
- **Python 3.11+**
- **Flask** (API e interface)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Banco de dados)
- **Docker & Docker Compose** (Containerização)
- **BeautifulSoup / Requests** (Coleta e parsing dos dados)

## 📂 Estrutura do Projeto
automacao-diario-oficial-natal/
├── pdfs/
├── api.py
├── aitomacao.py
├── docker-compose.yml # Configuração dos containers
├── Dockerfile # Imagem da aplicação
├── requirements.txt # Dependências Python
└── README.md

## ⚙️ Configuração e Instalação

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### Passos
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/automacao-diario-oficial-natal.git
   cd automacao-diario-oficial-natal
   

Configure as variáveis de ambiente no arquivo .env:

POSTGRES_USER=usuario

POSTGRES_PASSWORD=senha

POSTGRES_DB=diario

DATABASE_URL=postgresql+psycopg2://usuario:senha@db:5432/diario

Suba os containers:
```bash
   docker compose up --build
````


A aplicação Flask ficará disponível em:
http://localhost:5000

🛠️ Uso
O script de automação coleta as edições mais recentes do Diário Oficial.

Os dados são salvos no PostgreSQL e podem ser consultados via API Flask.
