import os
import shutil
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from pydantic import BaseModel


class AbstractFileStorage(ABC):

    @abstractmethod
    def upload_file(self, upload_dto: BaseModel) -> str:
        ...

    MIME_TYPES = {
        "pdf": "application/pdf",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "dwg": "image/vnd.dwg",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "svg": "image/svg+xml",
        "rvt": "application/octet-stream",
        "nwc": "application/x-nwc",
    }

    @staticmethod
    def check_and_create_dir(dir_name: str) -> str:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name

    @staticmethod
    def preprocess_rus_file_name(file_name: str) -> str:
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
            'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
            'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya'
        }

        result = ''
        for char in file_name:
            lower_char = char.lower()
            if lower_char in translit_map:
                trans_char = translit_map[lower_char]
                # сохраняем регистр
                if char.isupper():
                    trans_char = trans_char.capitalize()
                result += trans_char
            else:
                result += char
        return result

    @staticmethod
    def clear_file_name(file_name: str) -> str:
        replaces = {
            " ": "_",
            "(": "",
            ")": "",
            "/": "_",
            "\\": "_",
            ",": "_",
            ";": "_",
            ":": "_",
        }
        for key, value in replaces.items():
            file_name = file_name.replace(key, value)
        return file_name

    def check_file_type(self, file_name: str, mime_type: str, mime_keys: List[str] | None = None) -> bool:
        file_ext = file_name.split(".")[-1]
        mime_types = {key: self.MIME_TYPES.get(key) for key in mime_keys} if mime_keys is not None else self.MIME_TYPES
        t = mime_types.get(file_ext)
        if file_ext == "dwg" and t != mime_type:
            return mime_type == "application/octet-stream"
        if t is None:
            return False
        return t == mime_type

    @staticmethod
    def check_unique_file_name(file_name: str) -> str:
        now_time = datetime.now().strftime("%d-%m-%Y-%H-%M")
        file_pieces = file_name.split(".")
        file_path, file_ext = "".join(file_pieces[:-1]), file_pieces[-1]
        return file_path + "_" + now_time + "." + file_ext

    @staticmethod
    def check_unique_file_name_ts(file_name: str) -> str:
        now_time = datetime.now().timestamp()
        file_pieces = file_name.split(".")
        file_path, file_ext = "".join(file_pieces[:-1]), file_pieces[-1]
        return file_path + "_" + str(now_time) + "." + file_ext

    @staticmethod
    def check_file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

    @staticmethod
    def delete_file_if_exists(file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
