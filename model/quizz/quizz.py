import json
import os

from model.db import db
from model.questions.question import Question
from pathlib import Path


class Quizz(db.Model):
    __tablename__ = "quizz"

    id = db.Column(db.Integer, primary_key=True)
    questions_number = db.Column(db.Integer())
    theme = db.Column(db.String())
    battle_id = db.Column(db.Integer, db.ForeignKey('battles.id'), nullable=False)
    questions = db.relationship('Question', backref='quizz', lazy=True)

    def __init__(self, theme: str, question_number: int):
        self.theme = theme.lower()
        self.question_number = question_number
        self.questions = []
        self.progress = None

    def create_quizz(self):
        try:
            current_path = os.path.dirname(__file__)
            print(current_path)
            with open(Path(current_path) / '..' / 'utils' / 'theme' / self.theme / 'questions.json', "r") as questions:
                data_questions = json.load(questions)

            with open(Path(current_path) / '..' / 'utils' / 'theme' / self.theme / 'answers.json', "r") as answers:
                data_answers = json.load(answers)
        except IOError as ie:
            raise FileNotFoundError("Merci de vérifier le thème choisi")
        except Exception as e:
            raise NotImplementedError(f"Unknow exception catched: {e}")
        self.secure_creation_quizz(data_questions)
        for i in range(self.question_number):
            question = Question()
            question.select_question(data_questions)
            question.get_answers(data_answers)
            self.questions.append(question)
            data_questions.pop(question.index)

    def secure_creation_quizz(self, data):
        if not len(data) >= int(self.question_number):
            raise ValueError("Le nombre de question est trop important")

    def quizz_progress(self, index: int):
        progress = index / self.question_number * 100
        self.progress = int(progress)
        return self.progress

    def read_quizz(self):
        for question in self.questions:
            question.get_answers()
