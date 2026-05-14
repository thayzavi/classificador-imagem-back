# 🦟 Dengue AI API

API REST desenvolvida com Flask para detecção de possíveis focos de dengue através de imagens utilizando Inteligência Artificial com YOLO.

O sistema permite:

- Cadastro e autenticação de usuários
- Upload de imagens
- Análise automática com IA
- Histórico de análises
- Geração de PDF
- Download de laudos
- Documentação Swagger

---

# 🚀 Tecnologias Utilizadas

- Python 3.11
- Flask
- Flask JWT Extended
- MongoDB
- Flask PyMongo
- Ultralytics YOLO
- OpenCV
- ReportLab
- Swagger / Flasgger

---

# 📂 Estrutura do Projeto

```bash
classificador-imagem-back/
│
├── app/
│   │
│   ├── config/
│   │   └── config.py
│   │
│   ├── database/
│   │   └── db.py
│   │
│   ├── docs/
│   │   └── swagger.yml
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   └── analysis_model.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   └── analysis_routes.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   └── pdf_service.py
│   │
│   ├── uploads/
│   │   ├── imagens/
│   │   └── pdfs/
│   │
│   ├── utils/
│   │   └── upload.py
│   │
│   └── model/
│       └── dengue_model.pt
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md

# ⚙️ Instalação

1. Clone o projeto
```
git clone https://github.com/seu-usuario/projeto-ai.git

´´´
2. Entre na pasta
```
cd projeto-ai
```
3. Crie o ambiente virtual

Windows
```
python -m venv venv
```
Linux/Mac
```
python3 -m venv venv
```
4. Ative o ambiente virtual

Windows
```
venv\Scripts\activate
```
Linux/Mac
```
source venv/bin/activate
```
5. Instale as dependências
```
pip install -r requirements.txt
```

# 🔐 Configuração do .env

Crie um arquivo .env na raiz do projeto.

```
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
JWT_SECRET_KEY=segredo123

```

# ▶️ Executando o Projeto
```
python main.py
```

A API ficará disponível em:
```
http://127.0.0.1:5000

```

# 📚 Swagger

A documentação Swagger estará disponível em:
```
http://127.0.0.1:5000/apidocs

```
# 🔑 Autenticação JWT

A API utiliza JWT Bearer Token.
Após realizar login, utilize o token nas rotas protegidas:

```
Authorization: Bearer SEU_TOKEN
```

# 📌 Endpoints da API
     Autenticação (Auth)

```
| Método | Rota | Descrição |
|---|---|---|
| POST | `/register` | Cadastro de novo usuário |
| POST | `/login` | Login e geração de token JWT |
```
# 👤 Usuário

```
| Método | Rota | Descrição |
|---|---|---|
| GET | `/user/perfil` | Retorna dados do perfil |
| PUT | `/user/perfil` | Atualiza dados do usuário |
| DELETE | `/user/perfil` | Remove a conta do usuário |

```
# 🧠 Análises e IA
```
| Método | Rota | Descrição |
|---|---|---|
| POST | `/analysis` | Envia imagem para análise (FormData: foto, bairro, local, data_foto) |
| GET | `/analysis/history` | Lista histórico de análises do usuário |
| GET | `/analysis/{id}` | Detalhes de uma análise específica |
| GET | `/analysis/download/{id}` | Gera e baixa relatório em PDF |
| DELETE | `/analysis/{id}` | Exclui registro de análise |
```

# 📄 Geração de PDF

Após a análise, o sistema permite gerar um PDF contendo:

- Informações da análise
- Resultado da IA
- Confiança da previsão
- Dados da imagem

# 🛠️ Dependências
```
Flask
flask-jwt-extended
flask-pymongo
flask-bcrypt
flasgger
PyYAML
python-dotenv
ultralytics
torch
opencv-python
reportlab
pymongo
```
## 👥 Equipe
- Thayza Vitória
- Gabriel Ernandes
- Raissa Vitória
- Fabricio Estevam
- Pedro Victor
- Benardo