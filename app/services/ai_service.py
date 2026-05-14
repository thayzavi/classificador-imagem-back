from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "dengue_model.pt"
)

model = YOLO(MODEL_PATH)


def predict_image(image_path):

    results = model(
        image_path,
        imgsz=320,
        verbose=False
    )

    probs = results[0].probs
    names = results[0].names

    top1 = probs.top1
    confidence = float(probs.top1conf)

    classe = names[top1]

    if classe == "positivo":
        return {
            "resultado": "Possível foco de dengue",
            "classe": classe,
            "confianca": round(confidence * 100, 2)
        }

    return {
        "resultado": "Sem foco de dengue",
        "classe": classe,
        "confianca": round(confidence * 100, 2)
    }