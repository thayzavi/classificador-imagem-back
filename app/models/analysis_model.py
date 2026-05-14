from bson import ObjectId
from bson.errors import InvalidId

from app.database.db import mongo


class AnalysisModel:

    @staticmethod
    def create_analysis(data):

        return mongo.db.analysis.insert_one(data)

    @staticmethod
    def get_by_id(analysis_id):

        try:

            return mongo.db.analysis.find_one({
                "_id": ObjectId(analysis_id)
            })

        except InvalidId:
            return None

    @staticmethod
    def get_by_user(user_id):

        return list(
            mongo.db.analysis.find({
                "user_id": user_id
            }).sort("data_foto", -1)
        )

    @staticmethod
    def get_all():

        return list(
            mongo.db.analysis.find().sort(
                "data_foto",
                -1
            )
        )

    @staticmethod
    def update_analysis(analysis_id, data):

        try:

            return mongo.db.analysis.update_one(
                {
                    "_id": ObjectId(analysis_id)
                },
                {
                    "$set": data
                }
            )

        except InvalidId:
            return None

    @staticmethod
    def delete(analysis_id):

        try:

            return mongo.db.analysis.delete_one({
                "_id": ObjectId(analysis_id)
            })

        except InvalidId:
            return None

    @staticmethod
    def count_analysis():

        return mongo.db.analysis.count_documents({})

    @staticmethod
    def count_positive_cases():

        return mongo.db.analysis.count_documents({
            "resultado": "Possível foco de dengue"
        })

    @staticmethod
    def count_negative_cases():

        return mongo.db.analysis.count_documents({
            "resultado": "Sem foco de dengue"
        })