import os
import numpy as np
import tensorflow as tf

from PIL import Image

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "best_float32.tflite"
)

interpreter = tf.lite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


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

        "orientacao": "Recomenda-se realizar a limpeza imediata do local."
    },

    "negativo": {
        "descricao": "Nenhum possível foco de dengue foi identificado na imagem.",

        "risco": "baixo",

        "prevencao": [
            "Continue monitorando o ambiente",
            "Evite água parada",
            "Mantenha recipientes fechados"
        ],

        "orientacao": "O ambiente aparenta estar seguro."
    }
}

def preprocess_image(image_path):

    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(
        img,
        dtype=np.float32
    )

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    return img_array

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

        print("Prediction:", prediction)

        negativo = float(prediction[0][0])
        positivo = float(prediction[0][1])


        if positivo > negativo:

            info = FOCOS_DENGUE["positivo"]

            return {

                "resultado": "Possível foco de dengue",
                "classe": "positivo",

                "confianca": round(
                    positivo * 100,
                    2
                ),

                "descricao": info["descricao"],
                "risco": info["risco"],
                "prevencao": info["prevencao"],
                "orientacao": info["orientacao"]
            }

        info = FOCOS_DENGUE["negativo"]

        return {

            "resultado": "Sem foco de dengue",
            "classe": "negativo",

            "confianca": round(
                negativo * 100,
                2
            ),

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