import logging




# 設定日誌格式
log_format = "[%(asctime)s] [%(levelname)s] %(message)s"

# 設定不同等級的日誌路徑
debug_log_file = "debug.log"
warning_log_file = "warning.log"


def setup_logger():
    # 建立日誌物件
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    # 建立檔案處理器和格式器 - 除錯日誌
    debug_file_handler = logging.FileHandler(debug_log_file)
    debug_file_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter(log_format)
    debug_file_handler.setFormatter(debug_formatter)
    logger.addHandler(debug_file_handler)

    # 建立檔案處理器和格式器 - 警告日誌
    warning_file_handler = logging.FileHandler(warning_log_file)
    warning_file_handler.setLevel(logging.WARNING)
    warning_formatter = logging.Formatter(log_format)
    warning_file_handler.setFormatter(warning_formatter)
    logger.addHandler(warning_file_handler)

    # 建立終端機處理器和格式器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger