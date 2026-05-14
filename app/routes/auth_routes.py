from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from app.models.user_model import UserModel

auth_bp = Blueprint("auth", __name__)

bcrypt = Bcrypt()

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    return jsonify({
        "error": "JSON inválido"
    }), 400

    required_fields = [
        "nome",
        "email",
        "endereco",
        "cep",
        "numero_residencia",
        "senha"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Campo obrigatório: {field}"
            }), 400

    # Verifica se email já existe
    existing_user = UserModel.find_by_email(data["email"])

    if existing_user:
        return jsonify({
            "error": "Email já cadastrado"
        }), 409

    hashed_password = bcrypt.generate_password_hash(
        data["senha"]
    ).decode("utf-8")

    new_user = {
        "nome": data["nome"],
        "email": data["email"],
        "endereco": data["endereco"],
        "cep": data["cep"],
        "numero_residencia": data["numero_residencia"],
        "senha": hashed_password
    }

    UserModel.create_user(new_user)

    return jsonify({
        "message": "Usuário cadastrado com sucesso"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if "email" not in data or "senha" not in data:
        return jsonify({
            "error": "Email e senha são obrigatórios"
        }), 400

    user = UserModel.find_by_email(data["email"])

    if not user:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404

    password_valid = bcrypt.check_password_hash(
        user["senha"],
        data["senha"]
    )

    if not password_valid:
        return jsonify({
            "error": "Senha inválida"
        }), 401

    token = create_access_token(
        identity=str(user["_id"])
    )

    return jsonify({
        "message": "Login realizado com sucesso",
        "token": token,
        "usuario": {
            "id": str(user["_id"]),
            "nome": user["nome"],
            "email": user["email"]
        }
    }), 200