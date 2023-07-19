import asyncio
import csv
import json
import logging
import os
import time

import aiohttp
import cv2
import jellyfish
import pandas as pd
import pyautogui
from PIL import Image
from airtest_selenium.proxy import WebChrome
from selenium.webdriver.chrome.options import Options

from Google_api_function import Google_api_function


class Commons_function:
    def __init__(self):
        super().__init__()
        self.should_stop = False
        logging.basicConfig(level=logging.INFO)

    # 建立網頁驅動
    @classmethod
    def createwd(cls, url):
        chrome_options = Options()
        chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        driver = WebChrome(chrome_options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(url)
        driver.maximize_window()
        return driver

    # 獲得封包狀態
    @classmethod
    async def get_request_data(cls, session, request):
        url = request['name']
        try:
            async with session.get(url, timeout=5) as response:
                status_code = response.status
                return url, status_code
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            #             print("錯誤")
            pass
        except Exception as e:
            logging.error(f"請求發生錯誤：{e}")
        return url, None

    @classmethod
    async def url_loading_status(cls, driver):
        max_iterations = 50
        iteration = 0
        previous_requests = None
        driver.execute_script("window.performance.clearResourceTimings();")

        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector) as session:
            while True:
                xhr_requests = driver.execute_script("return window.performance.getEntriesByType('resource')")
                current_requests = set(request['name'] for request in xhr_requests)
                print("當前長度: " + str(len(xhr_requests)))
                if iteration >= max_iterations:
                    logging.info("已達到最大迭代次數")
                    break

                tasks = [cls.get_request_data(session, request) for request in xhr_requests]
                results = await asyncio.gather(*tasks)

                iteration += 1

                if previous_requests is not None and current_requests == previous_requests:
                    logging.info("封包相同")
                    break

                previous_requests = current_requests

                await asyncio.sleep(0)

                start_time = time.time()
                # 確定執行2秒
                while time.time() - start_time < 2:
                    await asyncio.sleep(0)

                await asyncio.sleep(0)

    #     # 獲得封包狀態
    #     @classmethod
    #     async def get_request_data(cls, session, request):
    #         url = request['name']
    #         async with session.get(url) as response:
    #             status_code = response.status
    #             return url, status_code

    #     # 用封包加載狀態判斷結束執行下一個事件
    #     @classmethod
    #     async def url_loading_status(cls, driver):
    #         max_iterations = 50
    #         iteration = 0
    #         previous_requests = None
    #         driver.execute_script("window.performance.clearResourceTimings();")
    #         async with aiohttp.ClientSession() as session:
    #             while True:
    #                 xhr_requests = driver.execute_script("return window.performance.getEntriesByType('resource')")
    #                 current_requests = set(request['name'] for request in xhr_requests)

    #                 #                 print("當前長度: " + str(len(xhr_requests)))

    #                 if iteration >= max_iterations:
    #                     logging.info("已達到最大迭代次數")
    #                     break

    #                 tasks = [cls.get_request_data(session, request) for request in xhr_requests]
    #                 results = await asyncio.gather(*tasks)

    #                 #                 for url, status_code in results:
    #                 #                     print(f'URL: {url}, 狀態: {status_code}')

    #                 iteration += 1

    #                 if previous_requests is not None and current_requests == previous_requests:
    #                     logging.info("封包相同")
    #                     break

    #                 previous_requests = current_requests

    #                 await asyncio.sleep(2)

    # 修改資料
    @classmethod
    def update_csv(cls, s1, s2, filename):
        df = pd.read_csv(filename, encoding='utf-8-sig', dtype=str)
        click_before_column = df["Click Before"]

        # 将包含s1的字符串替换为s2
        click_before_column = click_before_column.str.replace(s1.strip().replace('\n', ''), s2.strip().replace('\n', ''))
        # 将修改后的列重新赋值给原始DataFrame
        df["Click Before"] = click_before_column

        # 将修改后的DataFrame另存为CSV文件
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    # 寫入csv
    @classmethod
    def write_csv(cls, filename, data_list):
        # 计算集合中最长的长度
        max_length = max(len(data) for data in data_list)

        # 创建一个嵌套列表，每个子列表对应一个集合的数据
        nested_data = []
        for data in data_list:
            nested_data.append(data + [''] * (max_length - len(data)))

        with open(filename, 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(nested_data)

    @classmethod
    def crop_image_height(cls, image_path):
        # 讀取圖像
        image = cv2.imread(image_path)

        # 獲取圖像尺寸
        height, width = image.shape[:2]

        # 將圖像裁剪為高度為120的部分
        cropped_image = image[max(height - 120, 0):, :]

        # 保存裁剪後的圖像
        cropped_image_path = 'cropped_image.jpg'
        cv2.imwrite(cropped_image_path, cropped_image)

        return cropped_image_path

    # 讀取語系json 設定檔
    @classmethod
    def read_json_config(cls, game_name, language_type, image_path, client, file_name, game_name_count):
        google_api = Google_api_function()
        # 預防找不到任何對應的數據時使用 mode 1
        default_json = [
            {
                "game_name": "",
                "mode": "1",
                "game_directory": ""
            }
        ]

        with open("language_config/" + language_type + '_config.json', encoding='utf-8-sig') as f:
            data = json.load(f)

        matching_items = {}  # 用於存儲匹配項的字典
        max_similarity = 0  # 最高相似度
        max_similarity_item = None  # 具有最高相似度的項目

        for item in data:
            # 比較遊戲名稱的相似度，主要是預防中文辨識有問題，而且因為字體是斜體有可能導致辨識有問題
            similarity = jellyfish.jaro_winkler_similarity(game_name.strip().replace('\n', ''),
                                                           item['game_name'].strip().replace('\n', ''))

            if similarity >= 0.7 or game_name.strip().replace('\n', '') == item['game_name'].strip().replace('\n', ''):
                matching_items[item['game_name'].strip().replace('\n', '')] = similarity  # 使用遊戲名稱作為字典的鍵，相似度作為值

                if similarity > max_similarity:
                    max_similarity = similarity
                    max_similarity_item = item
        if not matching_items:
            # 如果斜體辨識不出來進行圖像旋轉
            rotated_image_path = cls.rotate_image(image_path, 1)
            time.sleep(1)
            # 使用 Google Cloud Vision API 再解析一次圖片
            text = google_api.google_api_Image_text_analysis_double_check(client, rotated_image_path, language_type)
            time.sleep(1)
            for item in data:
                similarity = jellyfish.jaro_winkler_similarity(text.strip().replace('\n', ''),
                                                               item['game_name'].strip().replace('\n', ''))
                if similarity >= 0.5 or text.strip().replace('\n', '') == item['game_name'].strip().replace('\n', ''):
                    matching_items[item['game_name'].strip().replace('\n', '')] = similarity  # 使用遊戲名稱作為字典的鍵，相似度作為值

                    if similarity > max_similarity:
                        max_similarity = similarity
                        max_similarity_item = item

        if max_similarity_item:
            print("資料一次修改")
            cls.update_csv(game_name.strip().replace('\n', ''), text.strip().replace('\n', ''), file_name)
            return max_similarity_item

        if not matching_items:
            # 裁剪圖像為一半
            cropped_image_path = cls.crop_image_height(image_path)
            time.sleep(1)

            # 使用 Google Cloud Vision API 再次解析圖像
            text = google_api.google_api_Image_text_analysis_double_check(client, cropped_image_path, language_type)
            time.sleep(1)

            time.sleep(1)

            for item in data:
                similarity = jellyfish.jaro_winkler_similarity(text.strip().replace('\n', ''),
                                                               item['game_name'].strip().replace('\n', ''))
                if similarity >= 0.7 or text.strip().replace('\n', '') == item['game_name'].strip().replace('\n', ''):
                    matching_items[item['game_name'].strip().replace('\n', '')] = similarity  # 使用游戏名称作为字典的键，相似度作为值

                    if similarity > max_similarity:
                        max_similarity = similarity
                        max_similarity_item = item

        if max_similarity_item:
            print("資料二次修改")
            cls.update_csv(game_name, text, file_name)
            return max_similarity_item

        return default_json[0]  # 如果找不到匹配項，則返回預設的 JSON 項目

    # 進行截圖
    @classmethod
    def screenshot_image(cls, image_height, image_height_range, screenshot_range, x, image_name):
        im = pyautogui.screenshot(region=(x, image_height, screenshot_range, image_height_range))
        im.save(image_name)

    # 點選座標
    @classmethod
    def click_coordinates(cls, x, y):
        pyautogui.click(x, y, duration=0.25)

    # 清除csv檔案
    @classmethod
    def clear_csv(cls, filename, header):
        # 標頭
        data = [
            header  # 添加英文標頭
        ]

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    # 拖曳視窗
    @classmethod
    def window_dragging_logic(cls, drag_along_the_x_axis, i, drag_count):
        start_x = drag_along_the_x_axis
        start_y = 600

        time.sleep(1)
        # 移动鼠标到起始位置
        pyautogui.moveTo(1800, start_y)
        time.sleep(1)

        # 按下鼠标左键
        pyautogui.mouseDown()

        # 拖曳鼠标到目标位置
        pyautogui.moveTo(-1800, 0, duration=2.0)

        time.sleep(1)
        if i + 1 == drag_count:
            screenshot = pyautogui.screenshot()
            screenshot.save("drag_comparison" + str(drag_count) + ".png")

        time.sleep(2)

        pyautogui.mouseUp()

        time.sleep(2)

    # 從已經截好的圖 在截出我要的部分
    @classmethod
    def crop_image(cls, image_path, x, y, width, height):
        # 打開圖像
        image = Image.open(image_path)

        # 根據指定的坐標軸截取圖像的特定範圍
        cropped_image = image.crop((x, y, x + width, y + height))

        # 保存截取的圖像
        cropped_image.save('cropped_drag_image.png')

    # 畫面從新整理
    @classmethod
    def refresh(cls, driver):
        driver.refresh()

    # 得到xy軸
    @classmethod
    def get_coordinates(cls, best_image_path, compare_image):
        # 讀取圖像
        image1 = cv2.imread(compare_image)
        image2 = cv2.imread(best_image_path)

        if image1 is None or image2 is None:
            print("無法讀取圖像")
            return 0, 0

        # 轉換圖像為灰度
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # 初始化SIFT特徵描述符
        sift = cv2.SIFT_create()

        # 找到特徵點和特徵描述符
        keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

        if descriptors1 is None or descriptors2 is None:
            print("找不到特徵點或特徵描述符")
            return 0, 0

        # 初始化FLANN匹配器
        flann = cv2.FlannBasedMatcher()

        # 進行特徵匹配
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        # 篩選好的匹配點
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        if len(good_matches) == 0:
            print("找不到相似匹配")
            return 0, 0

        # 排序匹配结果
        good_matches.sort(key=lambda x: x.distance)

        # 只保留最佳匹配
        best_match = good_matches[0]

        # 獲取最佳匹配的特徵點坐標
        index1 = best_match.queryIdx
        index2 = best_match.trainIdx
        point1 = keypoints1[index1].pt
        point2 = keypoints2[index2].pt

        # 輸出最佳匹配的坐標差異
        x_diff = point1[0] - point2[0]
        y_diff = point1[1] - point2[1]

        print("(x, y):", x_diff, y_diff)

        # 顯示匹配結果
        #         matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #         cv2.imshow("Matched Image", matched_image)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()

        return x_diff, y_diff

    # 圖像相似度比對
    @classmethod
    def image_comparison(cls, comparison_image1, comparison_image2):
        image1 = cv2.imread(comparison_image1)
        image2 = cv2.imread(comparison_image2)

        if image1 is None or image2 is None:
            print("無法讀取圖片")
            return 0

        # 轉換圖像為灰度
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # 初始化SIFT特徵描述符
        sift = cv2.SIFT_create()

        # 找到特徵點和特徵描述符
        keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

        if descriptors1 is None or descriptors2 is None:
            print("找不到特徵點或特徵描述符")
            return 0

        # 初始化FLANN匹配器
        flann = cv2.FlannBasedMatcher()

        # 進行特徵匹配
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        # 篩選好的匹配點
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        if len(good_matches) == 0:
            print("找不到相似匹配")
            return 0

        # 計算相似度
        similarity = len(good_matches) / len(matches)
        print("相似度:", similarity)

        #         # 顯示匹配結果
        #         matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None,
        #                                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #         cv2.imshow("Matched Image", matched_image)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()

        return similarity

    # 獲取最適合的圖片
    @classmethod
    def find_best_match(cls, comparison_image, directory):
        target_image = cv2.imread(comparison_image, cv2.IMREAD_GRAYSCALE)
        # 初始化匹配方法
        method = cv2.TM_CCOEFF_NORMED
        # 保存最高相似度和對應的圖像路徑
        best_similarity = 0.0
        best_image_path = ""
        # 遍歷目錄下的所有圖像文件
        for filename in os.listdir(directory):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                # 讀取圖像文件
                image = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)

                # 進行模板匹配
                result = cv2.matchTemplate(image, target_image, method)

                # 獲取最大匹配結果
                _, similarity, _, _ = cv2.minMaxLoc(result)

                print(filename + ":   " + str(similarity))

                # 更新最高相似度和對應的圖像路徑
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_image_path = os.path.join(directory, filename)
                # 輸出相似度最高的圖像的路徑
        if best_image_path != "":
            print("Most similar image:", best_image_path)
        return best_image_path

    # 旋轉圖片,並且切圖片大小
    @classmethod
    def rotate_image(cls, image_path, angle):
        # 讀取圖片
        image = cv2.imread(image_path)

        # 取得圖片尺寸
        height, width = image.shape[:2]

        # 計算旋轉中心點
        center = (width // 2, height // 2)

        # 定義旋轉矩陣
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # 執行仿射變換
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

        #         # 儲存傾斜後的圖片
        rotated_image_path = 'rotated_image.jpg'
        cv2.imwrite(rotated_image_path, rotated_image)
        return rotated_image_path


