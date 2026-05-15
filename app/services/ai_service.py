import os
import numpy as np
import tflite_runtime.interpreter as tflite

from PIL import Image


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "modelo_dengue.tflite"
)


# Carrega o modelo uma única vez
interpreter = tflite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()


# Informações de entrada e saída
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def preprocess_image(image_path):

    img = Image.open(image_path).convert("RGB")

    # Redimensiona para o tamanho esperado pelo modelo
    img = img.resize((224, 224))

    # Converte para array numpy
    img_array = np.array(
        img,
        dtype=np.float32
    )

    # Normaliza
    img_array = img_array / 255.0

    # Adiciona dimensão batch
    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    return img_array


def predict_image(image_path):

    try:

        img_array = preprocess_image(image_path)

        # Define tensor de entrada
        interpreter.set_tensor(
            input_details[0]['index'],
            img_array
        )

        # Executa inferência
        interpreter.invoke()

        # Obtém resultado
        prediction = interpreter.get_tensor(
            output_details[0]['index']
        )

        confidence = float(prediction[0][0])

        # Classe positiva
        if confidence >= 0.5:

            return {
                "resultado": "Possível foco de dengue",
                "classe": "positivo",
                "confianca": round(confidence * 100, 2)
            }

        # Classe negativa
        return {
            "resultado": "Sem foco de dengue",
            "classe": "negativo",
            "confianca": round((1 - confidence) * 100, 2)
        }

    except Exception as e:

        return {
            "resultado": "Erro ao analisar imagem",
            "classe": "erro",
            "confianca": 0,
            "erro": str(e)
        }