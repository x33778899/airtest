import json
import pandas as pd
from collections import OrderedDict


class Json_creator:
    def __init__(self):
        print("json檔產生中")
        self.language_table = {
            "en_us": "英文",
            "zh_cn": "簡中",
            "zh_tw": "繁中",
            "es_es": "西班牙文",
            "vi_vn": "越南文",
            "th_th": "泰文",
            "en_in": "印度文",
            "ko_kr": "韓文",
            "pt_pt": "葡萄牙文",
            "ja_jp": "日文"
        }

    # 產生json檔
    def json_creator(self):
        # Read JSON file
        data = self.read_json('./language_config/zh_cn_config.json')
        # Get specific property values
        json_data = self.get_json_dict(data)

        xlsx_list_language = ["繁中", "簡中", "英文", "韓文", "泰文", "越南文", "葡萄牙文", "西班牙文", "印度文",
                              "日文"]
        xlsx_list_title = "中拚"
        xlsx_file_path = "./language_config/遊戲列表.xlsx"

        language_dict = OrderedDict()
        for title in xlsx_list_language:
            result_xlsx1, result_xlsx2 = self.read_game_xlsx(xlsx_file_path, "多幣別開放", title, xlsx_list_title)
            language_dict[title] = (result_xlsx1, result_xlsx2)

        combined_data = []
        for key, values in language_dict.items():
            combined_values = list(zip(values[0], values[1]))
            combined_data.append((key, combined_values))

        modified_data = []
        for key, values in combined_data:
            modified_key = next((k for k, v in self.language_table.items() if v == key), key)
            modified_values = values
            modified_data.append((modified_key, modified_values))

        missing_directories = set()  # Track missing game directories
        for lang, data_list in modified_data:
            json_list = []
            for game_name, game_directory in data_list:
                mode = json_data.get(game_directory)
                if mode is not None:
                    json_obj = {
                        'game_name': game_name,
                        'mode': mode,
                        'game_directory': game_directory,
                    }
                    json_list.append(json_obj)
                else:
                    missing_directories.add((lang, game_directory))

            self.language_config_create(json_list, lang)

        self.missing_directories_create(missing_directories)

    # 有缺少的遊戲目錄
    @classmethod
    def missing_directories_create(cls, missing_directories):
        # Write missing game directories to a text file
        with open('./language_config_create/missing_directories.txt', 'w', encoding='utf-8') as file:
            file.write("Missing game directories:\n")
            for lang, game_directory in missing_directories:
                file.write(f"Language: {lang}, Game Directory: {game_directory}\n")

    # 產生語系json檔
    @classmethod
    def language_config_create(cls, json_list, lang):
        file_name = f'./language_config_create/{lang}_config.json'
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(json_list, file, ensure_ascii=False, indent=4)

    # 將json放在字典裡
    @classmethod
    def get_json_dict(cls, data):
        game_directory_dict = {}
        for element in data:
            game_directory = element['game_directory']
            mode = element['mode']
            game_directory_dict[game_directory] = mode
        return game_directory_dict

    # 讀取json檔
    @classmethod
    def read_json(cls, path):
        with open(path, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data

    # 讀取xlsx檔
    @classmethod
    def read_game_xlsx(cls, excel_file_path, sheet_name, title1, title2):
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        result_xlsx1 = df[title1].tolist()
        result_xlsx2 = df[title2].tolist()
        return result_xlsx1, result_xlsx2
