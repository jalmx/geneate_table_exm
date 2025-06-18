import json
import sys
from os import path
from pathlib import Path
from sys import argv


class CLI:
    HELP = """
    How to use:

        gtable <path_src_questions>.txt
        gtable <path_src_questions>.txt <random_answer>.json

        gtable exam_p1.txt
        gtable exam_p1.txt random.json
    """

    def init(self):
        """Init script"""

        try:
            if len(argv) == 1:
                print("ERROR")
                print(self.HELP)

            elif argv[1] == "-h" or argv[1] == "--help":
                print("help:")
                print(self.HELP)
                sys.exit(0)

            elif len(argv) >= 2 or len(argv) <= 3:
                json_answer_wrong = None
                path_question = Path(argv[1])
                name_gift_file = self.create_name(path_question)
                # print(len(argv))

                if len(argv) == 3:
                    json_path = argv[2]
                    json_answer_wrong = self.load_answer_from_json(json_path)

                text = load_file_from_exam(path_question)
                questions = parse_questions(text, data=json_answer_wrong)

                build_file(name_gift_file, questions)
            else:
                print("ERROR")
                print(self.HELP)
        except Exception as ex:
            import datetime
            with open(f"error_{datetime.datetime.today()}.log", "w+") as file:
                file.write(str(ex))
            print("error -> log")

    def create_name(self, path_file: str | Path) -> str:
        """Generate the name file will save gift.txt

        Args:
            path_file (str): path from file to input

        Returns:
            str: new name for the file <name>_gift.txt
        """
        name_full = path.basename(path_file)
        name = path.splitext(name_full)[0]
        name += "_table.html"
        return name

    def load_answer_from_json(self,json_path: str) -> dict:
        """Load answers from json file to dict

        Returns:
            str: Path from json file
        """
        with open(json_path, mode="r") as file:
            return json.load(file)


if __name__ == "__main__":
    CLI().init()
