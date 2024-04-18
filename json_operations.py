import json
from typing import Dict


def load_from_json(file_name: str) -> Dict:
    """Getting info from json"""

    try:
        with open(file_name, 'r') as file:
            return json.loads(file.read())

    except FileNotFoundError:
        return {}


def write_to_json(file_name: str, data: Dict) -> None:
    """Writing to json"""

    with open(file_name, 'w') as file:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        file.write(json_data)


def check_data(course: str) -> bool:
    with open("logins.json", 'r') as file:
        data = json.load(file)

        print(data[course])
        if not data[course]:
            print("FALSE")
            return False
    print("TRUE")
    return True

