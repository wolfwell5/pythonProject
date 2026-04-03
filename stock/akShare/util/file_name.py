"""
文件名和路径生成工具

提供自动生成带时间戳的文件名、获取调用者路径等功能
"""

import inspect
import os
from datetime import datetime
from pathlib import Path


def get_caller_filename_absolute_path():
    """
    获取调用者的文件绝对路径（向上追溯三层：csv.py -> file_name.py -> 实际调用者）
    
    Returns:
        str: 调用者文件的绝对路径
    """
    # 当前帧：get_caller_filename_absolute_path
    # f_back: generate_file_name
    # f_back.f_back: csv.py 中的方法
    # f_back.f_back.f_back: 真正的调用者 (如 1get_top10_free_holders.py)
    frame = inspect.currentframe().f_back.f_back.f_back.f_back
    file_path = frame.f_code.co_filename
    del frame
    print(f"file path {file_path}")
    return file_path


def get_akshare_base_path():
    """
    获取 akShare 基础目录路径
    
    Returns:
        Path: akShare util 目录的父目录
    """
    # 获取当前文件 (util/file_name.py) 的绝对路径
    current_file = os.path.abspath(__file__)
    # 返回上一级目录 (akShare 目录)
    return Path(os.path.dirname(current_file))


def build_folder_path(specific_folder, use_caller_path=False):
    """
    构建目标文件夹路径
    
    Args:
        specific_folder: 子文件夹名称
        use_caller_path: 是否使用调用者路径作为基准（默认 False，使用 akShare 根目录）
        
    Returns:
        str: 完整的文件夹路径
    """
    # 如果是绝对路径，直接返回
    if os.path.isabs(specific_folder):
        return specific_folder
    
    # 根据参数选择基准路径
    if use_caller_path:
        # 使用调用者路径（兼容旧逻辑）
        caller_path = get_caller_filename_absolute_path()
        base_path = Path(caller_path).parent
    else:
        # 使用 akShare 根目录（新逻辑）
        base_path = get_akshare_base_path()
    
    # 拼接完整路径
    folder_path = base_path / specific_folder
    return str(folder_path)


def ensure_directory_exists(folder_path):
    """
    确保目录存在，不存在则创建
    
    Args:
        folder_path: 目录路径
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)


def generate_file_name(core_word, specific_folder, add_timestamp=True) -> str:
    """
    生成完整的 CSV 文件路径
    
    Args:
        core_word: 文件名核心词
        specific_folder: 子文件夹名称
        add_timestamp: 是否添加时间戳（默认 True）
        
    Returns:
        str: 完整的文件路径
    """
    # 构建文件夹路径
    folder_path = build_folder_path(specific_folder, use_caller_path=True)
    
    # 确保目录存在
    ensure_directory_exists(folder_path)
    
    # 生成文件名
    if add_timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
        file_name = f"{timestamp}_{core_word}.csv"
    else:
        # 如果不加时间戳，确保有 .csv 后缀
        if core_word.lower().endswith('.csv'):
            file_name = core_word
        else:
            file_name = f"{core_word}.csv"
    
    # 返回完整路径
    return os.path.join(folder_path, file_name)
