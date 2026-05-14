from ultralytics import YOLO

model = YOLO("model/dengue_model.pt")

def predict_image(image_path):

    results = model(image_path)

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