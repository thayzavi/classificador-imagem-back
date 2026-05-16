import os

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

from app.config.config import Config
from app.models.analysis_model import AnalysisModel
from app.services.ai_service import predict_image
from app.services.pdf_service import generate_pdf
from app.utils.upload import save_image


analysis_bp = Blueprint("analysis", __name__)

UPLOAD_FOLDER = Config.UPLOAD_FOLDER


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

    if not bairro or not local or not data_foto:
        return jsonify({
            "error": "Todos os campos são obrigatórios"
        }), 400

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    saved_image = save_image(
        image,
        UPLOAD_FOLDER
    )

    if not saved_image["success"]:
        return jsonify({
            "error": saved_image["error"]
        }), 400

    image_path = saved_image["path"]
    filename = saved_image["filename"]

    result = predict_image(image_path)

    analysis_data = {
        "user_id": user_id,
        "bairro": bairro,
        "local": local,
        "data_foto": data_foto,
        "imagem": filename,

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
            "imagem": analysis_data["imagem"],

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
            "data_foto": item["data_foto"]
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
        "imagem": analysis["imagem"],
        "resultado": analysis["resultado"],
        "classe": analysis["classe"],
        "confianca": analysis["confianca"]
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

    image_path = os.path.join(
        UPLOAD_FOLDER,
        analysis["imagem"]
    )

    if os.path.exists(image_path):
        os.remove(image_path)

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

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        f"{id}.pdf"
    )

    generate_pdf(
        pdf_path,
        analysis
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )