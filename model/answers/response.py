import json
from main import db


class Response(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String())
    is_true = db.Column(db.Bolean())

    def __init__(self, question_id):
        self.question_id = question_id

    def get_possible_answers(self, answers_list):
        for answer in answers_list:
            if answer["id"] == self.question_id:
                return answer["answers"]