import inspect
import os
from datetime import datetime
from pathlib import Path


def get_caller_filename_absolute_path():
    # 获取调用栈的上一帧（即调用该函数的上下文）
    frame = inspect.currentframe().f_back.f_back.f_back
    # 获取文件的完整路径
    file_path = frame.f_code.co_filename
    # 清理帧对象以避免内存泄漏
    del frame
    return file_path


def generate_file_name(core_word, specific_folder) -> str:
    class_name = get_caller_filename_absolute_path()
    path_obj = Path(class_name)
    # E:\Develop\Repos\pythonProject\stock\akShare\十大流通股东
    akshare_base_path = path_obj.parent

    folder_path = f'{akshare_base_path}/{specific_folder}/'
    file_name = f'{datetime.now().strftime("%Y-%m-%d-%H-%M")}_{core_word}.csv'

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return os.path.join(folder_path, file_name)
