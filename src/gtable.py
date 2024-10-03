#!/usr/bin/env python
# pylint: disable=bare-except
"""
Generate a table html from file text
"""

import json
from pathlib import Path
import random
from sys import argv
from os import path
import sys

HELP = """
How to use:

    gtable <path_src_questions>.txt
    gtable <path_src_questions>.txt <random_answer>.json

    gtable exam_p1.txt
    gtable exam_p1.txt random.json
    
"""


def _clear_sentence(question: str) -> str:
    """clear the question if contain number to start que sentence

    Args:
        question (str): Sentence string

    Returns:
        str: Sentence clear, without number and any space
    """
    question = question.strip()
    if question[0].isdigit() or question[0].startswith("-"):
        position = question.find(" ")
        return question[position:].strip()

    return question.strip()


def _generate_txt_questions_base(txt: str, number: int, answer: str) -> str:
    """Generate line for html with the question

    Args:
        txt (str): question body
        number (int): number for the question
        answer (str): text with all answers

    Returns:
        str: template html with all body
    """
    return f' <tr><td colspan="3"> {number}.- {_clear_sentence(txt)}</td></tr>{answer}'


def _generate_answers(answer: str, answers_wrong: list)-> str:
    """Generate all text for the answer section row

    Args:
        answer (str): answer right
        answers_wrong (list): list of answers to complement the row

    Returns:
        str: html like this

        <tr>
            <td width="33%" style="text-align: center;">answer one </td>
            <td width="33%" style="text-align: center;">answer two</td>
            <td width="33%" style="text-align: center;">answer three </td>
        </tr>
    """
    answers_wrong.append(answer)

    answer_final = ""

    answers_wrong.sort(reverse=random.choice([True, False]))

    for answer_wrong in answers_wrong:

        answer_final += f'<td width="33%" style="text-align: center;">{_clear_sentence(answer_wrong)}</td>\n'

    return f"<tr>{answer_final}</tr>"


def _generate_question_multi(
    txt: str, answer: str, number: int, wrong_answer: list
) -> str:
    answer = _generate_answers(answer=answer, answers_wrong=wrong_answer)

    return _generate_txt_questions_base(txt=txt, number=number, answer=answer)


def _is_true_question(answer: str) -> str:
    """Generate template html with the answers for True and False

    Args:
        answer (str): Answer can be (True | False)

    Returns:
        str: <tr>
        <td width="33%" style="text-align: center;" >Verdadero</td>
        <td  width="33%"></td>
        <td width="33%" style="text-align: center;">Falso</td>
        </tr>
    """
    answers = ["Verdadero", "Falso"]
    response = ""
    if not _clear_sentence(answer).upper() == "Verdadero".upper():
        answers.reverse()

    response += f'<td  style="text-align: center"> {answers[0]} </td>'
    response += '<td  style="text-align: center"></td>'
    response += f'<td  style="text-align: center"> {answers[1]} </td>'

    return f"<tr> {response}</tr>"


def _generate_question_bool(txt: str, answer: str, number: int) -> str:
    answer = _is_true_question(answer=answer)

    return _generate_txt_questions_base(txt=txt, number=number, answer=answer)


def parse_question_rows(
    txt: str,
    answer: str,
    number: int,
    number_raw_question: int,
    wrong_answer: dict = None,
):
    """Parse the question from list to create a html template

    Args:
        txt (str): body question
        answer (str): correct answer
        number (int): number question
        number_raw_question (int): number question
        wrong_answer (dict, optional): list of wrong answers. Defaults to None.

    Returns:
        _type_: _description_
    """
    if wrong_answer and wrong_answer.get(str(number_raw_question)):
        return _generate_question_multi(
            txt=txt,
            answer=answer,
            number=number,
            wrong_answer=wrong_answer.get(str(number_raw_question)),
        )

    return _generate_question_bool(txt=txt, answer=answer, number=number)


def load_file_from_exam(path_file) -> list:
    """Reade file from path and return all content in str"""

    with open(path_file, mode="r") as document:
        return document.read()


def load_answer_from_json(json_path: str) -> dict:
    """Load answers from json file to dict

    Returns:
        str: Path from json file
    """
    with open(json_path, mode="r") as file:
        return json.load(file)


def _clear_questions(txt) -> str:
    content_raw = txt.replace("\t", "").split("\n")
    content_pre = []

    for line in content_raw:
        if len(line) > 0:
            content_pre.append(line.strip())

    start = False
    content = []
    for line in content_pre:
        if str(line)[0].isdigit() or start:
            start = True
            content.append(line)

    return content


def parse_questions(txt: str, data=None) -> list:
    """Take the content from file with questions to generate a list with questions
    to load in a new file"""

    content_raw = _clear_questions(txt)
    questions = []

    count = 0

    count_question = 1
    while count < len(content_raw):
        question = content_raw[count]
        count += 1
        answer = content_raw[count]
        count += 1

        questions.append(
            parse_question_rows(
                question,
                answer,
                number=count_question,
                wrong_answer=data,
                number_raw_question=count_question,
            )
        )
        count_question += 1

    questions.insert(0, '<table width="100%"><tbody>')
    questions.append("</tbody></table>")
    return questions


def build_file(path_to_save, questions):
    """Save the final file

    Args:
        path_to_save (str): path_to_save to save the file
        questions (list): All questions to save in list
    """
    with open(path_to_save, mode="w+") as file:

        for txt in questions:
            file.write(txt + "\n")

    print(f"File saved: {path_to_save}")


def create_name(path_file: str) -> str:
    """Generare the name file will save gift.txt

    Args:
        path_file (str): path from file to input

    Returns:
        str: new name for the file <name>_gift.txt
    """
    name_full = path.basename(path_file)
    name = path.splitext(name_full)[0]
    name += "_table.html"
    return name


def main():
    """Init script"""

    try:
        if len(argv) == 1:
            print("ERROR")
            print(HELP)

        elif argv[1] == "-h" or argv[1] == "--help":
            print("help:")
            print(HELP)
            sys.exit(0)

        elif len(argv) >= 2 or len(argv) <= 3:
            json_answer_wrong = None
            path_question = Path(argv[1])
            name_gift_file = create_name(path_question)
            # print(len(argv))

            if len(argv) == 3:
                json_path = argv[2]
                json_answer_wrong = load_answer_from_json(json_path)

            text = load_file_from_exam(path_question)
            questions = parse_questions(text, data=json_answer_wrong)

            build_file(name_gift_file, questions)
        else:
            print("ERROR")
            print(HELP)
    except Exception as ex:
        import datetime
        with open(f"error_{datetime.datetime.today()}.log", "w+") as file:
            file.write(str(ex))
        print("error -> log")


if __name__ == "__main__":
    main()
