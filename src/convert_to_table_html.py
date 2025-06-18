import random

from question import *


class ConvertQuestionToTable:

    def __init__(self, questions: list[QuestionBase], path_to_save: str = "."):
        self._questions = questions
        self._path_to_save = path_to_save
        self._html = None

    def _generate_html_row_question(self, question: QuestionBase,
                                    number: int = 0) -> str:
        """Generate line for html with the question

        Args:
            txt (str): question body
            number (int): number for the question
            answer (str): text with all answers
        Returns:
            str: template html with all body
        """
        return f'<tr><td colspan="3"> {number}.- {question.question.text}</td></tr>{self._get_html_row_answer(question)}'

    def _get_html_row_answer(self, question: QuestionBase) -> str:
        """Generate template html with the answers for True and False

        Returns:
            str: <tr>
            <td width="33%" style="text-align: center;" >Answer 1</td>
            <td  width="33%">None | Answer 2</td>
            <td width="33%" style="text-align: center;">Answer 3</td>
            </tr>
        """
        answers = question.answer.get_all()
        print("----", answers)
        response = ""
        if len(answers) == 2:
            response = f'<td  style="text-align: center">{answers[0]}</td>'
            response += '<td  style="text-align: center"></td>'
            response += f'<td  style="text-align: center">{answers[1]}</td>'
        else:
            for answer_wrong in random.sample(answers, len(answers)):
                response += f'<td width="33%" style="text-align: center;">{answer_wrong}</td>\n'

        return f"<tr> {response}</tr>"

    def build_html_table(self) -> None:
        """Take the content from file with questions to generate a list with
        questions to load in a new file"""

        self._html = '<table width="100%"><tbody>'

        for i, q in enumerate(self._questions):
            self._html += self._generate_html_row_question(number=i + 1,
                                                           question=q)

        self._html += "</tbody></table>"

        print(self._html)

    def save(self, path_to_save, questions):
        """Save the final file

        Args:
            path_to_save (str): path_to_save to save the file
            questions (list): All questions to save in list
        """
        self._path_to_save = path_to_save if path_to_save else self._path_to_save

        with open(path_to_save, mode="w+") as file:
            for txt in questions:
                file.write(txt + "\n")

        print(f"File saved: {path_to_save}")


def test():
    q1 = QuestionBase(
        Question(
            text="El interruptor termomagnético general debe colocarse antes de cualquier derivación en una instalación eléctrica residencial."),
        AnswerBool(True))

    q2 = QuestionBase(
        Question(
            text="La puesta a tierra solo es necesaria en instalaciones industriales, no en viviendas"),
        AnswerBool(False))

    q3 = QuestionBase(
        Question(
            text="¿Cuál *es el voltaje típico de un timbre residencial directo?"),
        AnswerMulti("127V", ("12V", "220V",)))

    qs = [q1, q2, q3]
    ConvertQuestionToTable(qs).build_html_table()


if __name__ == "__main__":
    test()
