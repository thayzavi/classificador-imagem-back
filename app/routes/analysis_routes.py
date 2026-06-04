import os
import tempfile

from bson.errors import InvalidId
from flask import (
    Blueprint,
    request,
    jsonify,
    send_file
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

import cloudinary.uploader

from app.config.config import Config
from app.models.analysis_model import AnalysisModel
from app.services.ai_service import predict_image
from app.services.pdf_service import generate_pdf
from app.services.cloudinary_service import upload_image


analysis_bp = Blueprint("analysis", __name__)

UPLOAD_FOLDER = Config.UPLOAD_FOLDER

temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    ) as temp:

        temp_path = temp.name
        image.save(temp_path)

    result = predict_image(temp_path)

finally:
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)

image.seek(0)

upload_result = upload_image(image)


@analysis_bp.route("/analysis", methods=["POST"])
@jwt_required()
def create_analysis():

    user_id = get_jwt_identity()

    if "foto" not in request.files:
        return jsonify({
            "error": "Imagem obrigatória"
        }), 400

    image = request.files["foto"]

    bairro = request.form.get("bairro")
    local = request.form.get("local")
    data_foto = request.form.get("data_foto")
    
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    if not bairro or not local or not data_foto:
        return jsonify({
            "error": "Todos os campos são obrigatórios"
        }), 400

    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return jsonify({
                "error": "Latitude ou longitude inválida"
            }), 400

    analysis_data = {
        "user_id": user_id,
        "bairro": bairro,
        "local": local,
        "data_foto": data_foto,

        "localizacao": {
            "latitude": latitude,
            "longitude": longitude
        } if latitude and longitude else None,

        "imagem_url": upload_result["url"],
        "public_id": upload_result["public_id"],

        "resultado": result["resultado"],
        "classe": result["classe"],
        "confianca": result["confianca"],

        "descricao": result["descricao"],
        "risco": result["risco"],
        "prevencao": result["prevencao"],
        "orientacao": result["orientacao"]
    }

    inserted = AnalysisModel.create_analysis(
        analysis_data
    )

    return jsonify({
        "message": "Análise realizada com sucesso",
        "analysis_id": str(inserted.inserted_id),

        "resultado": {
            "bairro": analysis_data["bairro"],
            "local": analysis_data["local"],
            "data_foto": analysis_data["data_foto"],

            "imagem_url": analysis_data["imagem_url"],

            "resultado": analysis_data["resultado"],
            "classe": analysis_data["classe"],
            "confianca": analysis_data["confianca"],

            "descricao": analysis_data["descricao"],
            "risco": analysis_data["risco"],
            "prevencao": analysis_data["prevencao"],
        "orientacao": analysis_data["orientacao"]
    }
}), 201


@analysis_bp.route("/analysis/history", methods=["GET"])
@jwt_required()
def get_history():

    user_id = get_jwt_identity()

    analyses = AnalysisModel.get_by_user(user_id)

    response = []

    for item in analyses:

        response.append({
            "id": str(item["_id"]),
            "bairro": item["bairro"],
            "local": item["local"],
            "resultado": item["resultado"],
            "confianca": item["confianca"],
            "data_foto": item["data_foto"],
            "localizacao": item.get("localizacao"),
            "imagem_url": item["imagem_url"],
        })

    return jsonify(response), 200


@analysis_bp.route("/analysis/<id>", methods=["GET"])
@jwt_required()
def get_analysis_details(id):

    user_id = get_jwt_identity()

    try:
        analysis = AnalysisModel.get_by_id(id)

    except InvalidId:
        return jsonify({
            "error": "ID inválido"
        }), 400

    if not analysis:
        return jsonify({
            "error": "Análise não encontrada"
        }), 404

    if analysis["user_id"] != user_id:
        return jsonify({
            "error": "Acesso negado"
        }), 403

    return jsonify({
        "id": str(analysis["_id"]),
        "bairro": analysis["bairro"],
        "local": analysis["local"],

        "data_foto": analysis["data_foto"],

        "imagem_url": analysis["imagem_url"],

        "localizacao": analysis.get("localizacao"),

        "resultado": analysis["resultado"],
        "classe": analysis["classe"],
        "confianca": analysis["confianca"],

        "descricao": analysis.get("descricao"),
        "risco": analysis.get("risco"),
        "prevencao": analysis.get("prevencao"),
        "orientacao": analysis.get("orientacao")
    }), 200


@analysis_bp.route("/analysis/<id>", methods=["DELETE"])
@jwt_required()
def delete_analysis(id):

    user_id = get_jwt_identity()

    try:
        analysis = AnalysisModel.get_by_id(id)

    except InvalidId:
        return jsonify({
            "error": "ID inválido"
        }), 400

    if not analysis:
        return jsonify({
            "error": "Análise não encontrada"
        }), 404

    if analysis["user_id"] != user_id:
        return jsonify({
            "error": "Acesso negado"
        }), 403

    if analysis.get("public_id"):
        cloudinary.uploader.destroy(
            analysis["public_id"]
        )

    AnalysisModel.delete(id)

    return jsonify({
        "message": "Análise excluída com sucesso"
    }), 200


@analysis_bp.route("/analysis/download/<id>", methods=["GET"])
@jwt_required()
def download_analysis(id):

    user_id = get_jwt_identity()

    try:
        analysis = AnalysisModel.get_by_id(id)

    except InvalidId:
        return jsonify({
            "error": "ID inválido"
        }), 400

    if not analysis:
        return jsonify({
            "error": "Análise não encontrada"
        }), 404

    if analysis["user_id"] != user_id:
        return jsonify({
            "error": "Acesso negado"
        }), 403

    pdf_buffer = generate_pdf(analysis)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"analise_{id}.pdf",
        mimetype="application/pdf"
    )