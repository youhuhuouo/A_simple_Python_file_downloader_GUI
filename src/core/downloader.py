#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单下载器核心类
Simple downloader core class
"""

import threading
import requests
import time
from pathlib import Path
from ..utils.file_utils import get_downloads_dir, get_safe_filename, get_unique_filepath

class Downloader:
    """简单下载器类 Simple downloader class"""
    
    def __init__(self):
        self.session = requests.Session()
        self.is_paused = False
        self.is_cancelled = False
        self.download_thread = None
        
    def download(self, url, progress_callback=None, save_path=None):
        """
        下载文件
        Download file
        
        Args:
            url (str): 下载链接 Download URL
            progress_callback (callable): 进度回调函数 Progress callback function
            save_path (str, optional): 保存路径 Save path
        """
        # 重置状态 Reset status
        self.is_paused = False
        self.is_cancelled = False
        
        # 在线程外处理文件路径 Handle file path outside thread
        if save_path is None:
            filename = url.split('/')[-1] or 'downloaded_file'
            filename = get_safe_filename(filename)
            save_path = get_downloads_dir() / filename
            save_path = get_unique_filepath(save_path)
        else:
            save_path = Path(save_path)
            
        # 确保下载目录存在 Ensure download directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        def download_thread():
            try:
                # 发送请求 Send request
                response = self.session.get(url, stream=True)
                response.raise_for_status()
                
                # 获取文件大小 Get file size
                total_size = int(response.headers.get('content-length', 0))
                
                # 下载文件 Download file
                with open(save_path, 'wb') as f:
                    if total_size == 0:  # 未知大小 Unknown size
                        f.write(response.content)
                        if progress_callback:
                            progress_callback(1, 1, 0)  # 100% progress
                    else:
                        downloaded = 0
                        start_time = time.time()
                        last_time = start_time
                        last_downloaded = 0
                        speed = 0
                        
                        for chunk in response.iter_content(chunk_size=8192):
                            if self.is_cancelled:
                                if progress_callback:
                                    progress_callback(-3, -3, 0)  # 表示取消 Indicate cancellation
                                return
                                
                            while self.is_paused and not self.is_cancelled:
                                time.sleep(0.1)  # 暂停时等待 Wait while paused
                                start_time = time.time()  # 重置开始时间
                                last_downloaded = downloaded  # 重置上次下载量
                                
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # 计算速度 Calculate speed
                                current_time = time.time()
                                time_diff = current_time - last_time
                                
                                # 每0.5秒更新一次速度 Update speed every 0.5 seconds
                                if time_diff >= 0.5:
                                    speed = (downloaded - last_downloaded) / time_diff
                                    last_downloaded = downloaded
                                    last_time = current_time
                                
                                if progress_callback:
                                    progress_callback(downloaded, total_size, speed)
                
                if progress_callback and not self.is_cancelled:
                    progress_callback(-1, -1, 0)  # 表示完成 Indicate completion
                    
            except Exception as e:
                print(f"下载错误|Download error: {str(e)}")
                if progress_callback:
                    progress_callback(-2, -2, 0)  # 表示错误 Indicate error
        
        # 在新线程中启动下载 Start download in new thread
        self.download_thread = threading.Thread(target=download_thread)
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def pause(self):
        """暂停下载 Pause download"""
        self.is_paused = True
        
    def resume(self):
        """继续下载 Resume download"""
        self.is_paused = False
        
    def cancel(self):
        """取消下载 Cancel download"""
        self.is_cancelled = True
        self.is_paused = False 