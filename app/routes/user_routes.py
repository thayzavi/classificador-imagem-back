from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.db import mongo

user_bp = Blueprint("user", __name__)


@user_bp.route("/user/perfil", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    user = mongo.db.users.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return jsonify({
            "error": "Usuário não encontrado"
        }), 404

    return jsonify({
        "id": str(user["_id"]),
        "nome": user["nome"],
        "email": user["email"],
        "endereco": user["endereco"],
        "cep": user["cep"],
        "numero_residencia": user["numero_residencia"]
    }), 200

@user_bp.route("/user/perfil", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = get_jwt_identity()

    data = request.get_json()

    return jsonify({
        "error": "JSON inválido"
    }), 400

    update_data = {}

    allowed_fields = [
        "nome",
        "endereco",
        "cep",
        "numero_residencia"
    ]

    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    return jsonify({
        "message": "Perfil atualizado com sucesso"
    }), 200

@user_bp.route("/user/perfil", methods=["DELETE"])
@jwt_required()
def delete_profile():

    user_id = get_jwt_identity()

    mongo.db.users.delete_one({
        "_id": ObjectId(user_id)
    })

    return jsonify({
        "message": "Conta removida com sucesso"
    }), 200