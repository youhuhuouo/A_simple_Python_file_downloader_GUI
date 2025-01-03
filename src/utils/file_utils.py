#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具函数
File utility functions
"""

import os
from urllib.parse import urlparse, unquote

def get_filename_from_url(url):
    """
    从URL中获取文件名
    Get filename from URL
    
    Args:
        url (str): 下载链接 Download URL
        
    Returns:
        str: 文件名 Filename
    """
    # 解析URL Get filename from URL
    parsed = urlparse(url)
    path = unquote(parsed.path)
    
    # 获取文件名 Get filename
    filename = os.path.basename(path)
    
    # 如果没有文件名，使用默认名称 If no filename, use default name
    if not filename:
        filename = "downloaded_file"
        
    return filename

def ensure_dir(directory):
    """
    确保目录存在
    Ensure directory exists
    
    Args:
        directory (str): 目录路径 Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory) 

def get_download_dir():
    """
    获取下载目录
    Get download directory
    
    Returns:
        str: 下载目录路径 Download directory path
    """
    # 获取程序所在目录 Get program directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    download_dir = os.path.join(base_dir, 'downloads')
    
    # 确保下载目录存在 Ensure download directory exists
    ensure_dir(download_dir)
    return download_dir

def get_safe_filename(filename):
    """
    获取安全的文件名（移除非法字符）
    Get safe filename (remove illegal characters)
    
    Args:
        filename (str): 原始文件名 Original filename
        
    Returns:
        str: 安全的文件名 Safe filename
    """
    # 替换Windows下的非法字符 Replace illegal characters in Windows
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename

def get_unique_filename(filepath):
    """
    获取唯一的文件名（如果文件已存在则添加序号）
    Get unique filename (add sequence number if file exists)
    
    Args:
        filepath (str): 文件路径 File path
        
    Returns:
        str: 唯一的文件路径 Unique file path
    """
    if not os.path.exists(filepath):
        return filepath
        
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    index = 1
    while True:
        new_filepath = os.path.join(directory, f"{name} ({index}){ext}")
        if not os.path.exists(new_filepath):
            return new_filepath
        index += 1 