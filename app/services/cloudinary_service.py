import cloudinary.uploader


def upload_image(image):

    result = cloudinary.uploader.upload(
        image,
        folder="biolens"
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }