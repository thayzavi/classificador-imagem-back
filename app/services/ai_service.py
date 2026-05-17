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



interpreter = tflite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()


input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def preprocess_image(image_path):

    img = Image.open(image_path).convert("RGB")

    img = img.resize((224, 224))

    img_array = np.array(
        img,
        dtype=np.float32
    )

    img_array = (img_array / 127.5) - 1.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    return img_array

FOCOS_DENGUE = {
    "positivo": {
        "descricao": "Possível acúmulo de água parada identificado na imagem, podendo servir como criadouro do mosquito Aedes aegypti.",
        "risco": "alto",
        "prevencao": [
            "Esvazie recipientes com água parada",
            "Realize a limpeza do local",
            "Tampe caixas d’água",
            "Descarte pneus e objetos acumuladores de água",
            "Mantenha calhas limpas"
        ],
        "orientacao": "Recomenda-se realizar a limpeza imediata do local e monitorar possíveis novos focos."
    },

    "negativo": {
        "descricao": "Nenhum possível foco de dengue foi identificado na imagem.",
        "risco": "baixo",
        "prevencao": [
            "Continue monitorando o ambiente",
            "Evite acúmulo de água parada",
            "Mantenha recipientes fechados"
        ],
        "orientacao": "O ambiente aparenta estar seguro, mas a prevenção deve continuar regularmente."
    }
}


def predict_image(image_path):

    try:

        img_array = preprocess_image(image_path)

        interpreter.set_tensor(
            input_details[0]['index'],
            img_array
        )

        interpreter.invoke()

        prediction = interpreter.get_tensor(
            output_details[0]['index']
        )

        confidence = float(prediction[0][0])

        # CASO POSITIVO
        if confidence >= 0.5:

            info = FOCOS_DENGUE["positivo"]

            return {
                "resultado": "Possível foco de dengue",
                "classe": "positivo",
                "confianca": round(confidence * 100, 2),

                "descricao": info["descricao"],
                "risco": info["risco"],
                "prevencao": info["prevencao"],
                "orientacao": info["orientacao"]
            }

        # CASO NEGATIVO
        info = FOCOS_DENGUE["negativo"]

        return {
            "resultado": "Sem foco de dengue",
            "classe": "negativo",
            "confianca": round((1 - confidence) * 100, 2),

            "descricao": info["descricao"],
            "risco": info["risco"],
            "prevencao": info["prevencao"],
            "orientacao": info["orientacao"]
        }

    except Exception as e:

        return {
            "resultado": "Erro ao analisar imagem",
            "classe": "erro",
            "confianca": 0,
            "erro": str(e)
        }