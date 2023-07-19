import logging
import sys
from Commons_function import Commons_function
import pyautogui
import time
from selenium import webdriver
import cv2
import numpy as np
import os
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from skimage.metrics import structural_similarity as ssim
import pyautogui
from PIL import Image
import pytesseract
from Google_api_function import Google_api_function
import io
from google.cloud import vision
import jellyfish
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import asyncio
import urllib.request
import pytesseract
import openocr

# # 指定图像文件路径
# image_path = 'drag_comparison0.png'

# # 使用 pytesseract 进行文字识别
# text = pytesseract.image_to_string(image_path, lang='chi_sim')
logging.basicConfig(level=logging.INFO)
# # 打印识别的文字
# logging.info(text)











#===============================================================================================================
# # 創建 Google_api_function 的對象
google_api = Google_api_function()

# 使用對象調用 google_api_read 方法
client = google_api.google_api_read()


Commons = Commons_function()
# Commons.update_csv("BAR\nBAR\nR\n777", "777", "game_feature_check.csv")


# def find_most_common_color(image):
#     # 将图像转换为HSV格式
#     image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # 统计各个颜色的像素数量
#     hist = cv2.calcHist([image_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

#     # 找到像素数量最多的颜色
#     max_count = np.max(hist)
#     h, s = np.unravel_index(np.argmax(hist), hist.shape)

#     # 将HSV颜色转换为BGR格式
#     color_bgr = cv2.cvtColor(np.uint8([[[h, s, 255]]]), cv2.COLOR_HSV2BGR)[0][0]

#     return color_bgr, max_count

# # 读取图像
# image = cv2.imread("original_image0.png")  # 替换为您的图像路径

# # 查找图像中最常见的颜色和对应的像素数量
# most_common_color, count = find_most_common_color(image)
# print(most_common_color)

# # 将图像中最常见的颜色框出来
# image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# lower_color = np.array([most_common_color[0] - 10, 50, 50])
# upper_color = np.array([most_common_color[0] + 10, 255, 255])
# mask = cv2.inRange(image_hsv, lower_color, upper_color)
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# if len(contours) > 0:
#     cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# # 显示带有最常见颜色框的图像
# cv2.imshow("Most Common Color", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

logging.info(google_api.google_api_Image_text_analysis(client,"t1.png","zh_tw"))
# logging.info(google_api.google_api_Image_text_analysis_double_check(client,"original_image0.png","zh_cn"))
# rotated_image_path = Commons.rotate_image("string_title3.png", 3)

# # logging.info(google_api.google_api_Image_text_analysis(client,rotated_image_path))
# locations1=google_api.google_api_image_text_get_coordinates(client,"t4.png","罗")
# locations2=google_api.google_api_image_text_get_coordinates(client,"t4.png","场")


# 提取位置信息
# 读取图像文件
# image = cv2.imread("t4.png")

# # 检查是否找到了位置信息
# if locations1 is not None and locations2 is not None:
#     # 获取第一个位置的信息
#     if locations1:
#         x1 = locations1[0]['x']
#         y1 = locations1[0]['y']
#         width1 = locations1[0]['width']
#         height1 = locations1[0]['height']
#     else:
#         x1 = y1 = width1 = height1 = 0

#     # 获取第二个位置的信息
#     if locations2:
#         x2 = locations2[0]['x']
#         y2 = locations2[0]['y']
#         width2 = locations2[0]['width']
#         height2 = locations2[0]['height']
#     else:
#         x2 = y2 = width2 = height2 = 0

#     # 计算需要截取的区域的边界
#     x_min = min(x1, x2)
#     y_min = min(y1, y2)
#     x_max = max(x1 + width1, x2 + width2)
#     y_max = max(y1 + height1, y2 + height2)

#     # 截取图像的指定区域
#     cropped_image = image[y_min:y_max, x_min:x_max]

#     # 显示截取的图像
#     cv2.imshow("Cropped Image", cropped_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("未找到位置信息")
# Commons.update_csv("拍住三公","\u62a2庄三公","game_feature_check.csv")
#     x = pyautogui.position().x
#     time.sleep(1)
#     print("x座標：", x)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # 打开图像文件
# image = cv2.imread('original_image1.png')

# # 将图像转换为灰度图像
# image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # 对图像进行预处理，包括二值化处理和向左倾斜
# _, image_threshold = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# # 检测图像中的轮廓
# contours, _ = cv2.findContours(image_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # 寻找最大轮廓
# largest_contour = max(contours, key=cv2.contourArea)

# # 计算最小外接矩形
# rect = cv2.minAreaRect(largest_contour)
# angle = rect[-1]

# # 对图像进行旋转矫正
# rows, cols = image.shape[:2]
# rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 5)
# rotated_image = cv2.warpAffine(image_threshold, rotation_matrix, (cols, rows))

# # 使用 Tesseract 进行文字识别
# text = pytesseract.image_to_string(rotated_image, lang='chi_sim')

# # 打印识别结果
# print(text)
# # game_set = ar.read_csv_compare_similarity("game_string_check.csv", "Click Before")
# search_set = set(["免佣百家\u4e50"]) 

# intersection_set = game_set.intersection(search_set)

# logging.info(intersection_set)

# if len(intersection_set) == 0:
#     logging.info("集合為空")
# else:
#     logging.info("不是空的")
#     logging.info(intersection_set)




# # 獲取xy軸
# similarity = Commons.image_comparison("none/none.png",
#                                                      'original_image1.png')


# Commons.crop_image("drag_comparison4.png", 1700, 400, 220, 150)
# test=Commons.rotate_image("original_image2.png", 5)
# texts=google_api.google_api_Image_text_analysis(client,test)


# # # result_text = texts.replace("\n", "")  # 清除換行符號
# # # print(result)

# logging.info(texts)

# lines = text.split("\n")


# for line in lines:
#     logging.info("我是資料  "+line)


# logging.info("我是長度  "+str(len(lines)))

# previous_url = None
# previous_status = None

# async def check_loading_status(url):
#     response = await loop.run_in_executor(None, requests.head, url)
#     status_code = response.status_code
#     return status_code

# async def process_request(request):
#     global previous_url, previous_status

#     url = request['name']
#     status = request.get('transferSize') > 0 and request.get('decodedBodySize') > 0

#     status_code = await check_loading_status(url)

#     logging.info(f"請求 URL: {url}")
#     logging.info(f"加載狀態: {'已完成' if status else '仍在加載'}")
#     logging.info(f"狀態碼: {status_code}")

#     if previous_url is not None and url == previous_url and status == previous_status:
#         logging.info("URL 相同")
#         should_stop = True


# async def main(driver):
#     loop = asyncio.get_event_loop()  # 创建事件循环
#     global previous_url, previous_status

#     # 獲取初始加載的資源數量
#     initial_resource_count = len(driver.find_elements(By.XPATH, "//img | //link | //script | //source"))

#     while True:
#         # 獲取當前正在加載的網絡請求信息
#         xhr_requests = driver.execute_script("return window.performance.getEntriesByType('resource')")

#         # 使用异步任务列表并发处理请求
#         tasks = [loop.create_task(process_request(request)) for request in xhr_requests]
#         await asyncio.gather(*tasks)

#         # 更新上一次的 URL 和加載狀態
#         if len(xhr_requests) > 0:
#             last_request = xhr_requests[-1]
#             previous_url = last_request['name']
#             previous_status = last_request.get('transferSize') > 0 and last_request.get('decodedBodySize') > 0
        
#         if should_stop:
#             break

#         time.sleep(2)

# # 初始化 WebDriver
# driver = webdriver.Chrome()

# # 加載網頁
# driver.get("https://apifront.qaz411.com/lx/S004/8.0.31/index.html?ps=qptest-wss.qaz411.com:8031&gameId=0&companyId=5064&theme=S004&agent=1101285&account=1101285_0000&token=7830ba8a1141dff325314d2fece5ed110bf7c407f29181021e95863846ad21ca1d0d1773882222b59961322fb5a9ecd16f01c675e7f61b72519360b9d2547b4c684bca43638c0e80ddeef668ebd621d7798fd8ed36fca17e126b6f9394e9de16b6b65a2efe0cdbc153eb80dbd727ab413462d15f6790fe4bc9ab088ec1f26bba&type=1&platform=1&languageType=zh_cn&sml=0&backgroundUrl=null&title=gfg&ckey=1101282_chessapilixin&lobbyType=0")









# def check_resource_loading(url):
#     driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
#     driver.get(url)

#     # Get the resource elements in the webpage
#     resource_elements = driver.find_elements(By.XPATH, "//img | //link | //script | //source")

#     # Check the loading status of each resource
#     for element in resource_elements:
#         resource_url = element.get_attribute("src") or element.get_attribute("href")
#         if not check_loading_status(resource_url):
#             return False

#     # Check the loading status of XHR resources
#     xhr_requests = driver.execute_script("return window.performance.getEntriesByType('resource')")
#     for xhr_request in xhr_requests:
#         resource_url = xhr_request.get("name")
#         if not check_loading_status(resource_url):
#             return False

#     return True

# # Check the loading status of a resource
# def check_loading_status(resource_url):
#     # Handle each resource's loading status
#     print(f"Resource URL: {resource_url}")

#     if resource_url is None:
#         print("Resource URL is empty, skipping check")
#         return True

#     if resource_url.startswith("http") or resource_url.startswith("https"):
#         response = requests.head(resource_url)
#         if response.status_code == 200:
#             print("Resource loaded successfully")
#             return True
#         else:
#             print(f"Resource loading failed, status code: {response.status_code}")
#             return False
#     else:
#         # Handle XHR requests here (e.g., using appropriate libraries or methods)
#         # Example code:
#         # if check_xhr_loading_status(resource_url):
#         #     print("XHR resource loaded successfully")
#         #     return True
#         # else:
#         #     print("XHR resource loading failed")
#         #     return False
#         # Modify the above code according to your specific XHR handling logic
#         pass

#     return False

# url = "https://apifront.qaz411.com/lx/S004/8.0.31/index.html?ps=qptest-wss.qaz411.com:8031&gameId=0&companyId=5064&theme=S004&agent=1101285&account=1101285_0000&token=7830ba8a1141dff325314d2fece5ed110bf7c407f29181021e95863846ad21ca1d0d1773882222b59961322fb5a9ecd16f01c675e7f61b72519360b9d2547b4c684bca43638c0e80ddeef668ebd621d7798fd8ed36fca17e126b6f9394e9de16b6b65a2efe0cdbc153eb80dbd727ab413462d15f6790fe4bc9ab088ec1f26bba&type=1&platform=1&languageType=zh_cn&sml=0&backgroundUrl=null&title=gfg&ckey=1101282_chessapilixin&lobbyType=0"  # 要檢查的網頁URL

# resource_loaded = False

# while not resource_loaded:
#     resource_loaded = check_resource_loading(url)
#     time.sleep(0.1)  # 暫停2秒後再次檢查
    
    
print(1234)



# logging.info(google_api.google_api_Image_text_analysis(client,"string_check_page0.png"))



# def test_write_csv(png_text, filename, header_name):
#     header = [
#         [header_name]  # 添加英文標題
#     ]
#     data = [
#         [png_text]
#     ]

#     with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
#         writer = csv.writer(file)
#         writer.writerows(header)  # 寫入標題
#         writer.writerows(data)  # 寫入數據
        

# # test_write_csv(google_api.google_api_Image_text_analysis(client,"test1.png"),"test.csv","translation results")

# # Create logger and set level


# logger = logging.getLogger('my_logger')
# logger.setLevel(logging.INFO)

# # 创建控制台日志处理器，并设置编码为utf-8
# handler = logging.StreamHandler(sys.stdout, encoding='utf-8')
# handler.setLevel(logging.INFO)

# # 创建日志格式化器
# formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

# # 将格式化器添加到处理器
# handler.setFormatter(formatter)

# # 将处理器添加到日志记录器
# logger.addHandler(handler)

# # 输出日志消息
# logger.info("【游戏规则】当相同图示相连并达获奖条件时，获得对应图示的奖励。所有标志必须由最左至右连续出现，方可获得赢分。所有赢分以押分倍数一倍显示。得分乘以押分。如遇任何故障导致游戏结果无法被判定时，此局游戏不成立【任意连线】任何图案连成一线或任何图案与777连线即可赢分。如遇任何故障导致游戏结果无法被判定时，此局游戏不成立")



# google_api.google_api_Image_text_get_coordinates(client,"screenshot_full_screen0.png","777")

# logging.info(Commons.get_coordinates("mode_1/information/DYDB_JAVA.png","screenshot_full_screen8.png"))

# image1 = cv2.imread("drag_comparison2.png")
# image2 = cv2.imread("drag_comparison4.png")


# if image1 is None or image2 is None:
#     print("無法讀取圖片")


# # 轉換圖像為灰度
# gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
# gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# # 初始化SIFT特徵描述符
# sift = cv2.SIFT_create()

# # 找到特徵點和特徵描述符
# keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
# keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

# if descriptors1 is None or descriptors2 is None:
#     print("找不到特徵點或特徵描述符")


# # 初始化FLANN匹配器
# flann = cv2.FlannBasedMatcher()

# # 進行特徵匹配
# matches = flann.knnMatch(descriptors1, descriptors2, k=2)

# # 篩選好的匹配點
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.7 * n.distance:
#         good_matches.append(m)

# if len(good_matches) == 0:
#     print("找不到相似匹配")


# # 計算相似度
# similarity = len(good_matches) / len(matches)
# print("相似度:", similarity)

# # 顯示匹配結果
# matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# cv2.imshow("Matched Image", matched_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()












# 讀取圖片



# image = Image.open("screenshot_full_screen2.png")

# # 使用 pytesseract 將圖片解析成文字
# text = pytesseract.image_to_string(image, lang='eng')



# # 读取目标图像
# comparison_image = 'screenshot1.png'
# target_image = cv2.imread(comparison_image, cv2.IMREAD_GRAYSCALE)

# # 初始化匹配方法
# method = cv2.TM_CCOEFF_NORMED

# # 保存最高相似度和对应的图像路径
# best_similarity = 0.0
# best_image_path = ""

# # 遍历目录下的所有图像文件
# directory = "options/"
# for filename in os.listdir(directory):
#     if filename.endswith(".png") or filename.endswith(".jpg"):
#         # 读取图像文件
#         image = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)

#         # 进行模板匹配
#         result = cv2.matchTemplate(image, target_image, method)

#         # 获取最大匹配结果
#         _, similarity, _, _ = cv2.minMaxLoc(result)

#         print(similarity)
        
#         # 更新最高相似度和对应的图像路径
#         if similarity > best_similarity:
#             best_similarity = similarity
#             best_image_path = os.path.join(directory, filename)

# # 输出相似度最高的图像的路径
# if best_image_path != "":
#     print("Most similar image:", best_image_path)

#     # 读取图像
#     image1 = cv2.imread(comparison_image)
#     image2 = cv2.imread(best_image_path)

#     # 转换图像为灰度
#     gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#     gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

#     # 初始化SIFT特征描述符
#     sift = cv2.SIFT_create()

#     # 找到特征点和特征描述符
#     keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
#     keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

#     # 初始化FLANN匹配器
#     flann = cv2.FlannBasedMatcher()

#     # 进行特征匹配
#     matches = flann.knnMatch(descriptors1, descriptors2, k=2)

#     # 筛选好的匹配点
#     good_matches = []
#     for m, n in matches:
#         if m.distance < 0.7 * n.distance:
#             good_matches.append(m)

#     # 输出匹配点的数量
#     print("Number of matches:", len(good_matches))

#     # 排序匹配结果
#     good_matches.sort(key=lambda x: x.distance)

#     # 只保留最佳匹配
#     best_match = good_matches[0]

#     # 获取最佳匹配的特征点坐标
#     index1 = best_match.queryIdx
#     index2 = best_match.trainIdx
#     point1 = keypoints1[index1].pt
#     point2 = keypoints2[index2].pt

#     # 输出最佳匹配的坐标差异
#     x_diff = point1[0] - point2[0]
#     y_diff = point1[1] - point2[1]
#     print("(x, y):", x_diff, y_diff)

#     # 显示匹配结果
#     matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#     cv2.imshow("Matched Image", matched_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()





