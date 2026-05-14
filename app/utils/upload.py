import os
from werkzeug.utils import secure_filename
from uuid import uuid4


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(image, upload_folder):

    if image.filename == "":
        return {
            "success": False,
            "error": "Nenhuma imagem enviada"
        }

    if not allowed_file(image.filename):
        return {
            "success": False,
            "error": "Formato inválido"
        }

    extension = image.filename.rsplit(".", 1)[1].lower()

    filename = f"{uuid4().hex}.{extension}"

    filepath = os.path.join(upload_folder, filename)

    image.save(filepath)

    return {
        "success": True,
        "filename": filename,
        "path": filepath
    }