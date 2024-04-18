from datetime import datetime
from json_operations import load_from_json, write_to_json


def write_log(error_name: str, error: str) -> None:
    """Writing errors"""

    log_file = "log.json"

    log_data = load_from_json(log_file)
    log_data.setdefault(error_name, []).append(error)

    write_to_json(log_file, log_data)


def get_curr_datetime() -> str:
    """Getting current datetime in needed format"""

    return datetime.now().strftime("%d-%m-%Y %H:%M")


def error_to_str(error_msg: str) -> str:
    """Getting message about error in needed format"""

    return f"[-] {error_msg}"


def success_to_str() -> str:
    """Getting message about success in needed format"""

    return f"[+] SUCCESSFUL {get_curr_datetime()}"
