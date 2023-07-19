import asyncio
import os
import time
from collections import deque
import inspect
import pyautogui
import pyperclip

import log
from Google_api_function import Google_api_function

logger = log.setup_logger()


class Translation_string:

    def __init__(self):
        super().__init__()

    # 點選樣式
    @classmethod
    def select_mode(cls, Commons, client, driver, game_mode, game_directory, game_name_count,
                    game_translation_reference_table,
                    game_name, language_type):
        if game_mode == "1":
            # 點擊模式 1
            cls._click_mode_one(Commons, client, driver, game_directory, game_name_count,
                                game_translation_reference_table,
                                game_name, language_type)
        elif game_mode == "2":
            # 點擊模式 2
            cls._click_mode_two(Commons, client, driver, game_directory, game_name_count,
                                game_translation_reference_table,
                                game_name, language_type)
        elif game_mode == "3":
            # 點擊模式 3
            cls._click_mode_three(Commons, client, driver, game_directory, game_name_count,
                                  game_translation_reference_table,
                                  game_name, language_type)

    # 點選模式1
    @classmethod
    def _click_mode_one(cls, Commons, client, driver, game_directory, game_name_count, game_translation_reference_table,
                        game_name, language_type):
        time.sleep(2)
        # 模仿ai點擊功能,隨便一個位子都可以,點掉教學
        Commons.click_coordinates(300, 300)

        time.sleep(3)

        # 遊戲名稱位置
        Commons.screenshot_image(100, 140, 450,
                                 720, 'string_title' + str(game_name_count) + ".png")

        #     截圖全螢幕
        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click,
                                                                     "mode_1/options_language/")
            if check_judgment:
                break
        # 獲取xy軸
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")
        time.sleep(2)
        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)

        time.sleep(3)
        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click, "mode_1/information/")
            if check_judgment:
                break
        # 獲取xy軸
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")
        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)

        # 等待出現?選單
        time.sleep(3)
        # 遊戲說明位置
        Commons.screenshot_image(180, 90, 420,
                                 750, 'string_check_a' + str(game_name_count) + ".png")
        # 賠率表位置遊戲規則位置
        Commons.screenshot_image(270, 270, 300,
                                 200, 'string_check_b' + str(game_name_count) + ".png")

        #     Commons.screenshot_image(380, 90, 300,
        #                              200, 'string_check_c' + str(game_name_count) + ".png")
        # 點選項
        Commons.click_coordinates(230 + 50, 380 + 50)
        time.sleep(3)

        result = deque()
        result.append(game_directory)
        result.append(game_name)

        time.sleep(3)
        #         column_one = Google_api_function().google_api_Image_text_analysis(client, 'string_title' + str(
        #             game_name_count) + '.png')
        column_two = Google_api_function().google_api_Image_text_analysis(client, 'string_check_a' + str(
            game_name_count) + '.png', language_type)
        column_three = Google_api_function().google_api_Image_text_analysis(client, 'string_check_b' + str(
            game_name_count) + '.png', language_type)
        #         result.append(column_one)
        result.append(column_two)
        result.append(column_three)

        cls._drag_select_text(570, 350, 1000, 1000, result)

        result_list = list(result)
        Commons.write_csv(game_translation_reference_table, [result_list])

    # 點選模式2
    @classmethod
    def _click_mode_two(cls, Commons, client, driver, game_directory, game_name_count, game_translation_reference_table,
                        game_name, language_type):
        time.sleep(2)
        #         # 遊戲名稱位置
        Commons.screenshot_image(100, 140, 420,
                                 750, 'string_title' + str(game_name_count) + ".png")
        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click, "mode_2/information/")
            if check_judgment:
                break

        # 獲取xy軸
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")
        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)

        # 等待出現?選單
        time.sleep(4)
        # 玩法規則位置
        Commons.screenshot_image(220, 90, 420,
                                 750, 'string_check_a' + str(game_name_count) + ".png")
        # 所有標頭位置 的圖片寬度
        header_length = 1290
        # 所有標頭位置
        Commons.screenshot_image(320, 90, header_length,
                                 310, 'string_check_b' + str(game_name_count) + ".png")
        # 解析所有標頭文字
        title = Google_api_function().google_api_Image_text_analysis(client,
                                                                     "string_check_b" + str(game_name_count) + ".png",
                                                                                  language_type)
        # 根據標頭裡的換行符號切割
        lines = title.split("\n")
        # 得到標頭總長度/字串切割長度從而得到點選次數跟要點的座標
        # 邏輯為依靠google 解析圖片的功能,google解析圖片文字有空格會自動補上換行符號
        # 我有我切割換行符號可以得到長度,再用截圖的寬度去除長度我可以得到要點幾次以及間距
        # 因為不確定是另存圖片還是複製文字,所以兩件事都做,判斷邏輯save_image_by_coordinates未如果圖片存在解析圖片文字寫入
        length_from_click = header_length / len(lines)

        result = deque()
        result.append(game_directory)
        result.append(game_name)
        result.append(title)

        #         column_one = Google_api_function().google_api_Image_text_analysis(client, 'string_title' + str(
        #             game_name_count) + '.png')
        #         result.append(column_one)

        for i in range(len(lines)):
            Commons.click_coordinates(length_from_click * (i + 1) + 50, 320 + 50)
            cls._drag_select_text(290, 450, 1300, 1200, result)
            time.sleep(4)
            text = cls._save_image_by_coordinates(350, 500,
                                                  "string_check_" + str(game_name_count) + "_" + str(i) + ".png")
            # 如果圖片才在解析圖片寫入文字
            if cls._check_image_exists(text):
                image_text = Google_api_function().google_api_Image_text_analysis(client,
                                                                                  "string_check_" + str(game_name_count)
                                                                                               + "_" + str(i) + ".png",
                                                                                               language_type)
                result.append(image_text)
            time.sleep(4)
            # 點掉x不然點選座標會改變
            Commons.click_coordinates(1900, 999)
            time.sleep(4)

        time.sleep(5)

        result_list = list(result)
        Commons.write_csv(game_translation_reference_table, [result_list])

    # 點選模式3
    @classmethod
    def _click_mode_three(cls, Commons, client, driver, game_directory, game_name_count,
                          game_translation_reference_table,
                          game_name, language_type):
        time.sleep(2)

        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click,
                                                                     "mode_3/game/")
            if check_judgment:
                break

        # 獲取xy軸
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")

        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(Commons.check_url_loading_status_main(driver))
        # 等待出現初級場加載結束
        time.sleep(1)
        # 點掉教學
        Commons.click_coordinates(x_diff + 50, y_diff + 150)
        time.sleep(3)

        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click,
                                                                     "mode_3/options_language/")
            if check_judgment:
                break

        # 獲取xy軸
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")

        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)

        time.sleep(3)

        click = False
        # 遊戲按鈕檢查,預防加載速度影響檢查兩遍
        for i in range(2):
            best_image_path, check_judgment = cls._game_button_check(Commons, driver, game_directory,
                                                                     game_name_count, i, click, "mode_3/information/")
            if check_judgment:
                break

        # 獲取xy軸跟相似度
        x_diff, y_diff = Commons.get_coordinates(best_image_path,
                                                 "screenshot_full_screen" + str(game_name_count) + ".png")

        # 點選項
        Commons.click_coordinates(x_diff + 50, y_diff + 150)

        time.sleep(4)

        # 魚種賠率位置 特色遊戲位置 介面引導位置
        Commons.screenshot_image(220, 600, 250,
                                 150, 'string_check_a' + str(game_name_count) + ".png")

        # 點選特色遊戲
        Commons.click_coordinates(150 + 50, 380)

        time.sleep(2)
        # 頁數位置
        Commons.screenshot_image(880, 80, 50,
                                 1110, 'string_check_page' + str(game_name_count) + ".png")

        time.sleep(2)
        # 頁數辨識
        number_check = Google_api_function().google_api_Image_text_analysis_double_check(client, 'string_check_page' + str(
            game_name_count) + '.png', language_type)
        #         number_click = ""
        # 預防萬一,如果該位置不是數字
        if number_check == "" or not number_check.isdigit():
            number_check = 6

        result = deque()
        result.append(game_directory)
        result.append(game_name)
        # 魚種賠率位置 特色遊戲位置 介面引導位置 辨識
        column_one = Google_api_function().google_api_Image_text_analysis(client, 'string_check_a' + str(
            game_name_count) + '.png', language_type)

        result.append(column_one)

        # 根據頁數決定要截圖辨識幾次特色遊戲的內容
        for x in range(int(number_check)):
            Commons.screenshot_image(280, 450, 1280
                                     , 470, 'string_check_b' + str(game_name_count) + "_" + str(x) + ".png")
            Commons.click_coordinates(1208 + 50, 900)
            time.sleep(2)

            # 特色遊戲 圖片辨識
            featured_game_content = Google_api_function().google_api_Image_text_analysis(client, 'string_check_b' + str(
                game_name_count) + "_" + str(x) + ".png", language_type)
            result.append(featured_game_content)
        time.sleep(2)

        result_list = list(result)
        Commons.write_csv(game_translation_reference_table, [result_list])
        time.sleep(1)

    # 預防加載問題影響到尋找按鈕,最多檢查兩遍
    @classmethod
    def _game_button_check(cls, Commons, driver, game_directory, game_name_count, i, click, parent_directory):
        # 截圖全螢幕
        driver.save_screenshot("screenshot_full_screen" + str(game_name_count) + ".png")
        time.sleep(2)
        # 自己找按鈕點擊,尋找?按鈕
        best_image_path = Commons.find_best_match("screenshot_full_screen" + str(game_name_count) + ".png",
                                                  parent_directory)
        if game_directory in best_image_path:
            print("圖片正確")
            click = True
        elif "common" in best_image_path:
            print("圖片正確")
            click = True
        else:
            if i == 0:
                print("圖片有問題")
            else:
                logger.warning("查出來的遊戲目錄:   "+parent_directory + "    最適合的遊戲目錄是:   " + best_image_path + ":   圖片有問題")
        return best_image_path, click

    # 檢查圖片是否存在
    @classmethod
    def _check_image_exists(cls, file_path):
        return os.path.exists(file_path) and os.path.isfile(file_path)

    # 複製文字的功能
    @classmethod
    def _drag_select_text(cls, start_x_axis, start_y_axis, copy_x_axis, copy_y_axis, result_list):
        # 移動鼠標標記到指定位置
        pyautogui.moveTo(start_x_axis, start_y_axis, duration=0.5)
        time.sleep(1)
        # 模擬滾輪往上滾動
        pyautogui.scroll(1000)

        time.sleep(1)

        # 模擬鼠標點擊並按住左鍵
        pyautogui.mouseDown()

        # 移動鼠標以選擇文本區域
        pyautogui.move(copy_x_axis, 0, duration=0.5)  # 向右移動
        pyautogui.move(0, copy_y_axis, duration=0.5)  # 向下移動

        # 釋放鼠標左鍵
        pyautogui.mouseUp()

        # 模擬按下複製快捷鍵
        pyautogui.hotkey('ctrl', 'c')  # 或者使用 pyautogui.hotkey('cmd', 'c')（适用于 macOS）

        # 從剪貼板中獲取複製的數據
        copied_data = pyperclip.paste()
        # 空字串不寫入
        if copied_data != "":
            result_list.append(copied_data)

        return result_list

    # 右鍵另存圖片的功能
    @classmethod
    def _save_image_by_coordinates(cls, start_x_axis, start_y_axis, file_name):
        # 模擬滾輪往上滾動
        pyautogui.scroll(2000)
        # 移動鼠標到指定的坐標位置
        pyautogui.moveTo(start_x_axis, start_y_axis, duration=0.5)

        # 模擬鼠標右鍵點擊
        pyautogui.click(button='right')

        # 假設在右鍵菜單中的"另存圖片"選項位置為相對於右鍵點擊位置的偏移量
        save_image_x_offset = 100
        save_image_y_offset = 50

        # 移動鼠標到另存圖片選項的位置
        pyautogui.move(save_image_x_offset, save_image_y_offset, duration=0.5)

        # 模擬鼠標左鍵點擊
        pyautogui.click()

        # 指定寫入在跟該class同一層目錄
        # 構建保存路徑
        current_file_path = inspect.getfile(cls)
        # 將路徑分割為目錄和文件名
        directory, _ = os.path.split(current_file_path)

        # 構建保存路徑
        save_path = os.path.join(directory, file_name)

        # 刪除同名檔案預防圖片已存在（如果存在）
        if os.path.exists(save_path):
            os.remove(save_path)

        # 將保存路徑複製到剪貼板
        pyperclip.copy(save_path)

        # 等待保存圖片窗口打開（根據實際情況調整等待時間）
        pyautogui.sleep(1)

        # 模擬按下快捷鍵Ctrl+V（黏貼路徑）
        pyautogui.hotkey('ctrl', 'v')

        # 模擬按下回車鍵（確認保存)
        pyautogui.press('enter')

        # 預防複製文字的時候複製不到字串把它清掉
        pyperclip.copy('')

        return file_name



