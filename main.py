from pprint import pprint

import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    files_url = "https://cloud-api.yandex.net/v1/disk/resources/files"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def get_upload_link(self, file_path: str) -> dict:
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(self.upload_url, params=params, headers=self.headers)
        jsonify = response.json()
        pprint(jsonify)
        return jsonify


    def upload(self, file_path: str):
        href = self.get_upload_link(file_path).get("href")
        if not href:
            return

        with open(file_path, 'rb') as file:
            response = requests.put(href, data=file)
            if response.status_code == 201:
                print("файл загружен")
                return True
            print("файл не загружен потому что", response.status_code)
            return False


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = "/Users/yulialebedeva/Downloads/instruction-ANACONDA.pdf"
    tooken = "y0_AgAAAAA2r5qLAAjJIQAAAADV_tzPu-aTxlY5TDida9NxoAabFObV40Y"
    uploader = YaUploader(tooken)
    uploader.upload(path_to_file)
