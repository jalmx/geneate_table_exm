import random


class Answer:

    def get_all(self):
        pass

    def get(self):
        pass

    def get_answer_random(self):
        pass


class AnswerBool(Answer):

    def __init__(self, answer=False):
        self._answer = self.get_true() if answer else self.get_false()

    def get(self):
        return self._answer

    def get_all(self):
        return (
            "Verdadero",
            "Falso",
        )

    def get_true(self):
        return self.get_all()[0]

    def get_false(self):
        return self.get_all()[1]

    def get_answer_random(self):
        return random.choice(self.get_all())

    def __str__(self):
        return f"The answer bool is: {self._answer}"


class AnswerMulti(Answer):

    def __init__(self, answer_correct: str, answers_wrong: tuple[str, str]):
        self.answer_correct = answer_correct
        self.answers_wrong = answers_wrong

    def get(self):
        return self.answer_correct

    def get_wrong(self):
        return self.answers_wrong

    def get_all(self):
        return (self.answer_correct,) + self.get_wrong()

    def get_answer_random(self):
        return random.choice(self.get_all())


class Question:

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f"Question is: {self.text}"


class QuestionBase:

    def __init__(
        self, question: Question, answer: Answer
    ):
        self.question = question
        self.answer = answer
