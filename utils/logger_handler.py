from datetime import datetime
import  logging
from utils.path_tool import get_abs_path
import os


# 文件存放地址
LOGO_ROT = get_abs_path("log")
# 确保存放目录存在
os.makedirs(LOGO_ROT, exist_ok=True)

# 日志配置格式
DEFAULT_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s-%(filename)s:%(lineno)s - %(message)s")

def get_logger(
        name : str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file: str = None
):
    """
    获取日志对象
    :param name: 日志名称
    :param console_level: 控制台日志级别
    :param file_level: 文件日志级别
    :param log_file: 日志文件
    :return: 日志对象
    :return: 日志对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 避免重复添加日志处理器
    if logger.handlers:
        return logger

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)
    # 文件日志处理器
    if not log_file:
        log_file = os.path.join(LOGO_ROT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(DEFAULT_LOG_FORMAT)
        logger.addHandler(file_handler)

    return  logger

# 获取日志对象
logger = get_logger()

if __name__ == '__main__':
    logger.info("hello world")