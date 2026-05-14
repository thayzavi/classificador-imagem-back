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
│   └── yolopt/
│       └── best.pt
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
