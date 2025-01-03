#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具函数
File utility functions
"""

from pathlib import Path

def get_downloads_dir():
    """
    获取下载目录
    Get downloads directory
    
    Returns:
        Path: 下载目录路径 Downloads directory path
    """
    # 使用程序目录下的downloads文件夹
    # Use downloads folder in program directory
    downloads = Path('Downloads')
    
    # 确保目录存在 Ensure directory exists
    downloads.mkdir(parents=True, exist_ok=True)
    
    return downloads

def get_safe_filename(filename):
    """
    获取安全的文件名
    Get safe filename
    
    Args:
        filename (str): 原始文件名 Original filename
        
    Returns:
        str: 安全的文件名 Safe filename
    """
    # 替换不安全字符 Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename

def get_unique_filepath(filepath):
    """
    获取唯一的文件路径（如果文件已存在则添加序号）
    Get unique filepath (add number if file exists)
    
    Args:
        filepath (Path): 原始文件路径 Original filepath
        
    Returns:
        Path: 唯一的文件路径 Unique filepath
    """
    if not filepath.exists():
        return filepath
        
    directory = filepath.parent
    filename = filepath.stem
    extension = filepath.suffix
    counter = 1
    
    while True:
        new_filepath = directory / f"{filename}_{counter}{extension}"
        if not new_filepath.exists():
            return new_filepath
        counter += 1 