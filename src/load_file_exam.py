import json
import logging
from pathlib import Path

from src.question import QuestionBase


class Exam:
    _json_answers_wrong = None

    def __init__(self, content: str | None = None,
                 path_file: str | Path | None = None,
                 json_path: str | Path | None = None):
        self._content = content
        self._path_file = path_file
        self._json_path = json_path

        if path_file:
            logging.log(level=logging.INFO, msg="Load exam from file")
            self._load_file_from_exam(self._path_file)
        if json_path:
            self._load_answer_from_json(self._json_path)

    def _load_file_from_exam(self, path_file) -> None:
        """Reade file from path and return all content in str"""
        self._path_file = path_file or self._path_file

        if not self._path_file:
            raise Exception("No file to extract content")

        with open(self._path_file, mode="r") as document:
            self._content = document.read()

    def _load_answer_from_json(self, json_path: str | None = None) -> None:
        """Load answers from json file to dict

        Returns:
            str: Path from json file
        """
        if json_path:
            self._json_path = json_path

        with open(json_path, mode="r") as file:
            self._json_answers_wrong = json.load(file)

    def build(self):
        if not self._content:
            raise Exception("No content exist")

        rows_clear = self._clear_content()
        print(rows_clear)

    def _clear_content(self):
        """
        Have to eliminate all content before the questions with answers
        Returns:

        """
        new_rows = []

        for row in self._content.split("\n"):
            row_clear = row.strip()
            if row_clear:
                row_clear = row_clear[0]
            if (len(row_clear)) and (
                row_clear.isdigit() or row_clear.startswith("-")):
                new_rows.append(row)

        print(new_rows)
        return new_rows

    def extract_sentences(self, txt: str):

        questions: list[QuestionBase] | None = None

        question = True
        for row in questions:
            if row.startswith("\t") or row.startswith("  "):
                self._clear_raw_answer(row)
            else:
                self._clear_row_question(row)

    def _clear_raw_answer(self, txt) -> list:

        content_pre = []

        # for line in content_raw:
        #     if len(line) > 0:
        #         content_pre.append(line.strip())

        start = False
        content = []
        for line in content_pre:
            if str(line)[0].isdigit() or start:
                start = True
                content.append(line)

        return content

    def _clear_row_question(self, question: str) -> str:
        """clear the question if contain number to start que sentence

        Args:
            question (str): Sentence string

        Returns:
            str: Sentence clear, without number and any space
        """
        question = question.strip()
        print(f"question: {question}")
        if question[0].isdigit() or question[0].startswith("-"):
            position = question.find(" ")
            return question[position:].strip()

        return question.strip()


def test():
    Exam(path_file="Examen.txt").build()


if __name__ == "__main__":
    test()
