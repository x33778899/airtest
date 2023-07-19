import asyncio
import logging
import time

import pandas as pd
import pyautogui
from selenium.webdriver.common.by import By

import log
from Commons_function import Commons_function
from Google_api_function import Google_api_function
from Translation_string import Translation_string


class Airtest_automated_start:
    # 設定日誌
    logger = log.setup_logger()

    # 功能參數調整
    @classmethod
    def _function_parameter(cls):
        # 判斷遊戲點選功能是否正常
        game_feature_check = 'game_feature_check.csv'
        # 翻譯對照表
        game_translation_reference_table = "game_translation_reference_table.csv"
        # 沒有得到前端圖片間距是幾試出來的
        image_size = 285
        # y軸截圖座標
        image_height = 360
        # y軸截圖範圍
        image_height_range = 170
        # x軸等於13的原因是沒拖曳x=0可以點到你要的東西,拖曳後點選x會有上一次拖曳前的最後一個
        x = 13
        # y軸
        y = 300
        # drag_along_the_x_axis =image_size*6 代表我只點6張圖,設成+13方便直接修改x測試
        drag_along_the_x_axis = image_size * 6 + 13
        # 遊戲名稱計算
        game_name_count = 0
        # 單純判斷因為count=0 要額外截圖,理論上只有0跟0以上的判斷
        count = 0
        # 拖曳次數
        drag_count = 0
        # 從右點到左
        reverse_calculation = 1
        # 目前點在幾行
        row = 1
        # 網頁
        url = "https://apifront.qaz411.com/lx/S004/8.0.51/index.html?ps=qptest-wss.qaz411.com:8031&gameId=0&companyId=5064&theme=S004&agent=1101285&account=1101285_abcddd&token=82854d92e8ea52f0c4305cd5dcab989a25cf4baa67dab7cd3565d623585b7fef697f9f44ef6de10ef552a79842d9940d54dfc96daaead8777152c70d7cda5ecb3d2a4c594bac7dcac89c56a67690b9f01df4ad9b4799fd2f8c26afe2db06cdac50edf024bf3c09f10f19639e47a48e5a5000bbc3ec5dc1dc46a0742b5d57d84b&type=1&platform=1&languageType=zh_cn&sml=0&backgroundUrl=null&title=gfg&ckey=1101282_chessapilixin&lobbyType=0"

        #     url ="https://apifront.qaz411.com/lx/S004/8.0.32/index.html?ps=qptest-wss.qaz411.com:8032&gameId=0&companyId=5001&theme=S004&agent=1100005&account=1100005_abc&token=5f192b3583c6ef9409cc66cd932a91cd50e7aebfe83ccfe79b3b3cfc5d8371b61ef19e0ff78bd28ba4fa9280886c829c3387e9172cf64885e4fc8a3bcf14a575ce0c2fc5bce67e555f1ef87dad81ddb6bbb08c1c2ac296dd7b426f5a4abb08886bae5373f20dd558503855c69f991d235159d42070bd074ddd20191b5618bae5&type=1&platform=1&languageType=zh_cn&sml=1&backgroundUrl=&title=lx"
        return image_height, image_size, count, drag_along_the_x_axis, drag_count, game_feature_check, \
            game_translation_reference_table, game_name_count, image_height_range, reverse_calculation, row, x, y, url

    # 選擇功能
    @classmethod
    def _automated_test_mode(cls, Commons, client, driver, function, game_name_count, game_translation_reference_table,
                             language_type, original_image_text, game_feature_check):
        if function == 1:
            pass
        elif function == 2:
            ts = Translation_string()  # 實例化Translation_string類
            game_mode_item = Commons.read_json_config(original_image_text, language_type,
                                                      'original_image' + str(game_name_count) + ".png",
                                                      client, game_feature_check, game_name_count)
            logging.info(game_mode_item)

            game_mode = game_mode_item["mode"]
            game_name = game_mode_item["game_name"]
            game_directory = game_mode_item["game_directory"]

            time.sleep(2)

            ts.select_mode(Commons, client, driver, game_mode, game_directory, game_name_count,
                           game_translation_reference_table, game_name, language_type)

    # 開始執行程式
    @classmethod
    def start(cls, function):
        # 創建 Google_api_function 的對象
        google_api = Google_api_function()

        # 使用對象調用 google_api_read 方法
        client = google_api.google_api_read()
        # 設定參數
        image_height, image_size, count, drag_along_the_x_axis, drag_count, game_feature_check, game_translation_reference_table, \
            game_name_count, image_height_cut, reverse_calculation, row, x, y, url = cls._function_parameter()

        Commons = Commons_function()

        # 迴圈開始執行前先清乾淨csv
        Commons.clear_csv(game_feature_check, ['Click Before', 'Click After', 'Comparison Result'])

        # 迴圈開始執行前先清乾淨csv
        Commons.clear_csv(game_translation_reference_table,
                          ["game_directory", "game_name"])
        # 切割字串獲取language_type
        language_type = cls._get_language_type(url)

        # 建立網頁驅動
        driver = Commons.createwd(url)

        # 獲取螢幕尺寸
        screen_width, screen_height = pyautogui.size()

        print(f"螢幕尺寸：{screen_width} x {screen_height}")
        loop = asyncio.get_event_loop()
        # 暫存字串
        temporary_string = ""
        while True:
            #             x = pyautogui.position().x

            loop.run_until_complete(Commons.url_loading_status(driver))

            time.sleep(2)
            canvas = driver.find_element(By.TAG_NAME, "canvas")

            location = canvas.location
            # 從右點到左不進入判斷
            # 從新設定點選座標條件
            count, drag_count, x = cls._from_set_coordinates(count, drag_along_the_x_axis, drag_count,
                                                             reverse_calculation, x)
            # 判斷拖曳次數
            for i in range(drag_count):
                Commons.window_dragging_logic(drag_along_the_x_axis, i, drag_count)
            # 第一張圖開始的位子計算方式不同

            if count == 0 or reverse_calculation >= 2:
                if drag_count > 0:
                    # 只有在剛拖曳完這一次,跟反者點第一次需要判斷是不是到底了
                    if count == 0 and reverse_calculation == 1:
                        # 用來判斷視窗拖曳是否拉到底
                        Commons.crop_image("drag_comparison" + str(drag_count) + ".png", 1800, 400, 140, 150)

                        temporary_string = Google_api_function().google_api_Image_text_analysis(client,
                                                                                                "cropped_drag_image.png"
                                                                                                , language_type)
                        logging.info(temporary_string)
                    # 正常邏輯temporary_string不會為空
                    if temporary_string == "":
                        # 判斷是不是拖曳到底了
                        # 拉到底從左邊開始點不準確從右邊開始點到左邊
                        # 相似度可以在多試幾次後修正
                        # 點選前截圖
                        Commons.screenshot_image(image_height, image_height_cut, image_size,
                                                 screen_width - reverse_calculation * image_size - 13,
                                                 'original_image' + str
                                                 (game_name_count) + ".png")

                        time.sleep(1)
                        # 只要不是debug模式
                        if function != 0:
                            # 解析文字
                            original_image_text = Google_api_function().google_api_Image_text_analysis_double_check(
                                client,
                                'original_image' + str
                                (game_name_count) + ".png",
                                language_type)

                            time.sleep(1)
                            # 遊戲是否有被重複點選檢查
                            intersection_set = cls._game_execution_duplicate_check(game_feature_check,
                                                                                   original_image_text)
                            # 如果集合不為空,辨識遊戲是否重複出現,點者反者點最多6個遊戲
                            if len(intersection_set) != 0 and function != 0 or reverse_calculation == 7:
                                y += 330
                                drag_count = 0
                                image_height += 330
                                reverse_calculation = 1
                                # 本來就點在第二行了可以中斷了
                                if row == 2:
                                    print("自動化測試結束")
                                    break
                                else:
                                    print("開始點選第二行")
                                    row = 2
                                    Commons.refresh(driver)
                                    continue

                            else:
                                print("集合為空,代表不重複")
                                time.sleep(1)

                                # 模仿ai點擊功能
                                Commons.click_coordinates(screen_width - reverse_calculation * image_size, y)

                                loop.run_until_complete(Commons.url_loading_status(driver))

                                time.sleep(5)
                                # # debug 模式
                                # 點擊選項後的截圖
                                Commons.screenshot_image(image_height, image_height_cut, image_size,
                                                         screen_width - reverse_calculation * image_size - 13,
                                                         'compare_image' + str(game_name_count) + ".png")

                                time.sleep(3)

                                logging.info(intersection_set)

                                # 解析文字
                                compare_image_text = Google_api_function().google_api_Image_text_analysis(client,
                                                                                                          'compare_image' + str(
                                                                                                              game_name_count) + '.png',
                                                                                                          language_type)

                                # csv 判斷 功能是否正常
                                cls._check_game_clicking_to_csv(compare_image_text, game_feature_check,
                                                                original_image_text)

                                # 自動化測試的模式選擇
                                cls._automated_test_mode(Commons, client, driver, function, game_name_count,
                                                         game_translation_reference_table, language_type,
                                                         original_image_text, game_feature_check)

                                game_name_count += 1

                                reverse_calculation += 1

                                Commons.refresh(driver)
                        # debug 模式
                        else:
                            if reverse_calculation <= 6:
                                time.sleep(1)
                                Commons.screenshot_image(image_height, image_height_cut, image_size,
                                                         screen_width - reverse_calculation * image_size - 13,
                                                         'original_image' + str
                                                         (game_name_count) + ".png")
                                time.sleep(1)
                                # 模仿ai點擊功能
                                Commons.click_coordinates(screen_width - reverse_calculation * image_size, y)

                                time.sleep(1)

                                loop.run_until_complete(Commons.url_loading_status(driver))

                                game_name_count += 1

                                time.sleep(1)

                                reverse_calculation += 1
                                if reverse_calculation == 7:
                                    y += 330
                                    drag_count = 0
                                    image_height += 330
                                    reverse_calculation = 1
                                    if row == 2:
                                        print("自動化測試結束")
                                        break
                                    else:
                                        print("開始點選第二行")
                                        row = 2
                                        Commons.refresh(driver)
                                        continue
                            Commons.refresh(driver)
                    else:
                        # 網頁截圖流程的邏輯
                        count, game_name_count, x = cls._web_page_screenshot_evaluation_process(image_height,
                                                                                                image_size,
                                                                                                client, count, driver,
                                                                                                game_feature_check,
                                                                                                game_translation_reference_table,
                                                                                                game_name_count,
                                                                                                image_height_cut,
                                                                                                x, y, Commons,
                                                                                                language_type, loop,
                                                                                                function)
                else:
                    # 網頁截圖流程的邏輯
                    count, game_name_count, x = cls._web_page_screenshot_evaluation_process(image_height,
                                                                                            image_size,
                                                                                            client, count, driver,
                                                                                            game_feature_check,
                                                                                            game_translation_reference_table,
                                                                                            game_name_count,
                                                                                            image_height_cut,
                                                                                            x, y, Commons,
                                                                                            language_type, loop,
                                                                                            function)

            else:
                # 網頁截圖流程的邏輯
                count, game_name_count, x = cls._web_page_screenshot_evaluation_process(image_height,
                                                                                        image_size,
                                                                                        client, count, driver,
                                                                                        game_feature_check,
                                                                                        game_translation_reference_table,
                                                                                        game_name_count,
                                                                                        image_height_cut,
                                                                                        x, y, Commons,
                                                                                        language_type, loop, function)
        loop.close()

    @classmethod
    # 遊戲是否有被重複點選檢查
    def _game_execution_duplicate_check(cls, game_feature_check, original_image_text):
        search_set = set([original_image_text.strip().replace('\n', '')])
        # 交集比對計算如果有一樣的代表可以換第二行了
        game_set = cls._read_csv_compare_similarity(game_feature_check, "Click Before")
        game_set = set(item.strip().replace('\n', '') for item in game_set)  # 進行格式處理
        intersection_set = game_set.intersection(search_set)
        return intersection_set

    # 從新設定點選座標條件
    @classmethod
    def _from_set_coordinates(cls, count, drag_along_the_x_axis, drag_count, reverse_calculation, x):
        if x >= drag_along_the_x_axis and not reverse_calculation > 1:
            drag_count += 1
            x = 13
            count = 0
        return count, drag_count, x

    # 獲取languageType
    @classmethod
    def _get_language_type(cls, url):
        language_type_prefix = url.split("languageType=")[1]
        language_type = language_type_prefix.split("&")[0]
        return language_type

    # 網頁截圖遊戲流程的邏輯
    @classmethod
    def _web_page_screenshot_evaluation_process(cls, image_height, image_size, client, count, driver,
                                                game_feature_check, game_translation_reference_table, game_name_count,
                                                image_height_range, x, y, Commons, language_type, loop
                                                , function):

        # 點選前截圖
        Commons.screenshot_image(image_height, image_height_range, image_size, x - 13,
                                 'original_image' + str(game_name_count) + ".png")

        if function != 0:
            # 圖片文字解析
            original_image_text = Google_api_function().google_api_Image_text_analysis_double_check(client,
                                                                                                    'original_image' + str(
                                                                                                        game_name_count) + ".png",
                                                                                                    language_type)
            # 預防字串間隔過長被辨識出換行符號,把換行符號清掉
            original_image_text_replace = original_image_text.replace("\n", "")  # 清除換行符號
            # 如果翻譯出來沒有字串遊戲不點擊
            if original_image_text_replace == "":
                x += image_size
                count += 1
                game_name_count += 1
                Commons.refresh(driver)
                time.sleep(2)

            else:

                time.sleep(1)
                # 模仿ai點擊功能
                Commons.click_coordinates(x, y)

                time.sleep(1)

                loop.run_until_complete(Commons.url_loading_status(driver))

                time.sleep(5)

                # 點擊選項後的截圖
                Commons.screenshot_image(image_height, image_height_range, image_size, x - 13,
                                         'compare_image' + str(game_name_count) + ".png")

                time.sleep(2)

                compare_image_text = Google_api_function().google_api_Image_text_analysis(client, 'compare_image' + str(
                    game_name_count) + '.png', language_type)
                # csv 判斷 功能是否正常
                cls._check_game_clicking_to_csv(compare_image_text, game_feature_check, original_image_text_replace)

                #     test_csv = read_csv(game_name_count)
                #     logging.info(test_csv)
                # 自動化測試的模式選擇
                cls._automated_test_mode(Commons, client, driver, function, game_name_count,
                                         game_translation_reference_table,
                                         language_type, original_image_text, game_feature_check)

                x += image_size
                count += 1
                game_name_count += 1
                # 畫面從新整理
                Commons.refresh(driver)
        # debug 模式
        else:
            time.sleep(1)
            # 模仿ai點擊功能
            Commons.click_coordinates(x, y)

            time.sleep(1)

            loop.run_until_complete(Commons.url_loading_status(driver))

            time.sleep(5)

            x += image_size
            count += 1
            game_name_count += 1
            # 畫面從新整理
            Commons.refresh(driver)

        return count, game_name_count, x

    # 判斷從右點到左是否有相同資料
    @classmethod
    def _read_csv_compare_similarity(cls, file_path, header):
        result_set = set()
        df = pd.read_csv(file_path, encoding='utf-8-sig', dtype=str)
        title = df[header].astype(str)  # 將列數據轉換為字符串類型

        for data in title:
            if pd.notnull(data):  # 確保數據不為空
                result_set.add(data.strip().replace('\n', ''))  # 去除字符串前後空格並添加到集合中預防出意外加\n處理
        return result_set

    # 將遊戲功能是否正常寫入csv
    @classmethod
    def _check_game_clicking_to_csv(cls, compare_image_text, filename, original_image_text):
        if original_image_text != compare_image_text:
            result = [original_image_text, compare_image_text, "True"]  # 創建一個空的集合
            result_list = list(result)
            Commons_function.write_csv(filename, [result_list])
            print("遊戲功能正常")
        else:
            result = [original_image_text, compare_image_text, "False"]  # 創建一個空的集合
            result_list = list(result)
            Commons_function.write_csv(filename, [result_list])
            print("遊戲功能不正常")



