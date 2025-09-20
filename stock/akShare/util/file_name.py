import inspect
import os
from datetime import datetime
from pathlib import Path

# absolute_path = 'E:/Develop/Repos/pythonProject/stock/akShare/sample_data/'


def get_caller_filename_absolute_path():
    # 获取调用栈的上一帧（即调用该函数的上下文）
    frame = inspect.currentframe().f_back.f_back.f_back
    # 获取文件的完整路径
    file_path = frame.f_code.co_filename
    # 清理帧对象以避免内存泄漏
    del frame
    return file_path


def generate_file_name(core_word) -> str:
    class_name = get_caller_filename_absolute_path()
    path_obj = Path(class_name)
    # E:\Develop\Repos\pythonProject\stock\akShare
    akshare_base_path = path_obj.parent.parent  # 获取"北交所"目录的父目录

    # 转换为字符串
    # base_path_str = str(akshare_base_path)

    fetched_data_path=f'{akshare_base_path}/sample_data/'
    # file_name, ext = os.path.splitext(os.path.basename(class_name))
    parent_dir=os.path.basename(os.path.dirname(class_name))
    # file_parent_folder_name = os.path.basename(os.path.dirname(class_name))
    # folder_path = f'{fetched_data_path}{parent_dir}/{file_name}'
    folder_path = f'{fetched_data_path}{parent_dir}/'
    file_name = f'{datetime.now().strftime("%Y-%m-%d-%H-%M")}_{core_word}.csv'

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return os.path.join(folder_path, file_name)