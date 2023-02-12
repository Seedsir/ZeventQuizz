import pytest
from main import create_app
from models import User, Question, Answer
from models.db import db


@pytest.fixture()
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    with app.test_request_context():
        yield app.test_client()


@pytest.fixture()
def user():
    user = User("Seedsir", '12345678')
    user.create_user(user.username, '12345678', refresh_token=None)
    last_user = User.query.order_by(User.id.desc()).first()
    user.id = int(last_user.id)
    return user


@pytest.fixture()
def question():
    question = Question()
    question.create_question("Est ce que mes tests passent ?", "Tester mon code")
    last_insert = Question.query.order_by(Question.id.desc()).first()
    question.id = int(last_insert.id)
    question.theme = last_insert.theme
    yield question

@pytest.fixture()
def answer():
    answer = Answer.query.order_by(Answer.id.desc()).first()
    yield answer


@pytest.fixture()
def question_with_true_answer():
    question = Question()
    question.create_question("Est ce que mes tests passent avec un bool a true?", "Tester mon code")
    last_insert = Question.query.order_by(Question.id.desc()).first()
    question.id = int(last_insert.id)
    answer = Answer(question.id, "Cette réponse est vraie", True)
    answer.create_answer(question.id, "Cette réponse est vraie", True)
    yield question

