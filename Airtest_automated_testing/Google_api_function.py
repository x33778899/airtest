import io

import cv2
import jellyfish
from PIL import Image
from google.cloud import vision

import log

logger = log.setup_logger()


# google api 相關
class Google_api_function:
    def __init__(self):
        super().__init__()

    # google api 解析圖片文字獲取座標  
    @classmethod
    def google_api_image_text_get_coordinates(cls, client, image_path, search_string):
        # 讀取圖像文件
        img = cv2.imread(image_path)

        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image_path = vision.Image(content=content)

        # 進行文字辨識
        response = client.text_detection(image=image_path)
        annotations = response.text_annotations

        # 提取圖像中的文字
        image_text = annotations[0].description if annotations else ""

        # 尋找相似度最高的位置
        best_locations = []

        for annotation in annotations:
            text = annotation.description
            similarity = jellyfish.jaro_winkler_similarity(search_string.lower(), text.lower())
            #             print("字串相似度: " + str(similarity))

            # 預防 Google 辨識出來的文字稍有所不同，將相似度超過 0.7 的文字視為相同字串
            if similarity > 0.7:
                vertices = annotation.bounding_poly.vertices
                x_coordinates = [vertex.x for vertex in vertices]
                y_coordinates = [vertex.y for vertex in vertices]
                x = min(x_coordinates)
                y = min(y_coordinates)
                width = max(x_coordinates) - x
                height = max(y_coordinates) - y
                best_location = {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                }
                best_locations.append(best_location)

        if not best_locations:
            logger.info('圖像中未找到相似度超過 0.7 的位置')
        else:
            for location in best_locations:
                x = location['x']
                y = location['y']
                width = location['width']
                height = location['height']
                # 在圖像上顯示匹配結果
                cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)
                cv2.putText(img, image_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        #         cv2.imshow("Matched Image", img)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()

        return best_locations

    # google api 解析圖片文字
    @classmethod
    def google_api_Image_text_analysis(cls, client, image_path, language_type):
        language_table = {
            "en_us": "en",
            "zh_cn": "zh-CN",
            "zh_tw": "zh-TW",
            "es_es": "es",
            "vi_vn": "vi-VN",
            "th_th": "th",
            "en_in": "en-IN",
            "ko_kr": "ko-KR",
            "pt_pt": "pt",
            "ja_jp": "ja-JP"
        }

        # 讀取圖像
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

            # 設置圖像的語言提示
        language_code = language_table.get(language_type.lower())

        # 發送圖像到 Google Cloud Vision API 進行解析
        image = vision.Image(content=content)
        response = client.text_detection(image=image,
                                         image_context={"language_hints": [language_code] if language_code else None})

        # 提取解析結果
        texts = response.text_annotations
        if len(texts) > 0:
            text = texts[0].description
        else:
            text = ""
        return text

    # google api 解析圖片文字
    @classmethod
    def google_api_Image_text_analysis_double_check(cls, client, image_path, language_type):
        language_table = {
            "en_us": "en",
            "zh_cn": "zh-CN",
            "zh_tw": "zh-TW",
            "es_es": "es",
            "vi_vn": "vi-VN",
            "th_th": "th",
            "en_in": "en-IN",
            "ko_kr": "ko-KR",
            "pt_pt": "pt",
            "ja_jp": "ja-JP"
        }

        # 讀取圖像
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        # 設置圖像的語言提示
        language_code = language_table.get(language_type.lower())

        # 發送圖像到 Google Cloud Vision API 進行解析
        image = vision.Image(content=content)
        response = client.text_detection(image=image,
                                         image_context={"language_hints": [language_code] if language_code else None})

        # 提取解析結果
        texts = response.text_annotations
        if len(texts) > 0:
            text = texts[0].description
        else:
            text = ""

        # 獲取文本邊界框信息
        if len(texts) > 1:
            vertices = texts[0].bounding_poly.vertices
            top = min(vertex.y for vertex in vertices)
            bottom = max(vertex.y for vertex in vertices)

            # 獲取圖像寬度
            image = Image.open(image_path)
            image_width = image.width

            # 根據圖像寬度計算裁剪框
            cropped_top = max(top - 10, 0)
            cropped_bottom = min(bottom + 10, image.height)

            # 裁剪圖像為文本區域
            cropped_image = image.crop((0, cropped_top, image_width, cropped_bottom))

            # 保存裁剪後的圖像
            cropped_image.save("cropped_game_image.png")

            # 進行文字識別
            cropped_image_content = io.BytesIO()
            cropped_image.save(cropped_image_content, format='PNG')
            cropped_image_content.seek(0)
            cropped_image_response = client.text_detection(image=vision.Image(content=cropped_image_content.read()),
                                                           image_context={"language_hints": [language_code] if
                                                           language_code else None})
            cropped_texts = cropped_image_response.text_annotations
            if len(cropped_texts) > 0:
                cropped_text = cropped_texts[0].description
            else:
                cropped_text = ""

            return cropped_text
        else:
            return ""

    # 讀取 API 數據
    @classmethod
    def google_api_read(cls):
        credential_path = 'even-metrics-384612-a67c43b0c5d9.json'
        client = vision.ImageAnnotatorClient.from_service_account_file(credential_path)
        return client


