#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单下载器GUI
Simple downloader GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from ..core.downloader import Downloader

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("简单下载器|Simple Downloader")
        self.root.geometry("600x250")
        
        self.downloader = Downloader()
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI Initialize UI"""
        # URL输入框 URL input
        url_frame = ttk.Frame(self.root, padding="10")
        url_frame.pack(fill=tk.X)
        
        ttk.Label(url_frame, text="下载链接|URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 下载按钮 Download button
        self.download_btn = ttk.Button(url_frame, text="下载|Download", command=self._download)
        self.download_btn.pack(side=tk.LEFT)
        
        # 控制按钮 Control buttons
        control_frame = ttk.Frame(self.root, padding="5")
        control_frame.pack(fill=tk.X)
        
        self.pause_btn = ttk.Button(control_frame, text="暂停|Pause", command=self._pause_resume, state="disabled")
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(control_frame, text="取消|Cancel", command=self._cancel, state="disabled")
        self.cancel_btn.pack(side=tk.LEFT)
        
        # 进度条 Progress bar
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            orient="horizontal", 
            length=300, 
            mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        # 状态标签 Status label
        self.status_label = ttk.Label(
            self.root, 
            text="就绪|Ready", 
            padding="10"
        )
        self.status_label.pack()
        
        # 速度标签 Speed label
        self.speed_label = ttk.Label(
            self.root,
            text="",
            padding="5"
        )
        self.speed_label.pack()
        
    def _format_speed(self, speed):
        """格式化速度显示 Format speed display"""
        if speed < 1024:
            return f"{speed:.1f} B/s"
        elif speed < 1024 * 1024:
            return f"{speed/1024:.1f} KB/s"
        else:
            return f"{speed/1024/1024:.1f} MB/s"
        
    def _update_progress(self, downloaded, total, speed):
        """
        更新进度
        Update progress
        """
        if downloaded == -1 and total == -1:  # 下载完成 Download completed
            self.progress_bar["value"] = 100
            self.status_label.config(text="下载完成|Download completed")
            self._reset_buttons()
            messagebox.showinfo("完成|Complete", "下载完成|Download completed")
            return
            
        if downloaded == -2 and total == -2:  # 下载错误 Download error
            self.status_label.config(text="下载失败|Download failed")
            self._reset_buttons()
            messagebox.showerror("错误|Error", "下载失败|Download failed")
            return
            
        if downloaded == -3 and total == -3:  # 下载取消 Download cancelled
            self.status_label.config(text="下载已取消|Download cancelled")
            self._reset_buttons()
            return
            
        # 更新进度条 Update progress bar
        progress = (downloaded / total) * 100
        self.progress_bar["value"] = progress
        
        # 更新状态和速度 Update status and speed
        self.status_label.config(
            text=f"下载中|Downloading... {progress:.1f}% ({downloaded}/{total} bytes)"
        )
        self.speed_label.config(text=f"速度|Speed: {self._format_speed(speed)}")
        
    def _reset_buttons(self):
        """重置按钮状态 Reset button states"""
        self.download_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.cancel_btn.config(state="disabled")
        self.speed_label.config(text="")
        
    def _download(self):
        """开始下载 Start download"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误|Error", "请输入URL|Please enter URL")
            return
            
        # 重置进度条 Reset progress bar
        self.progress_bar["value"] = 0
        self.status_label.config(text="下载中...|Downloading...")
        
        # 更新按钮状态 Update button states
        self.download_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.cancel_btn.config(state="normal")
        
        # 开始下载 Start download
        self.downloader.download(url, progress_callback=self._update_progress)
        
    def _pause_resume(self):
        """暂停/继续下载 Pause/Resume download"""
        if self.downloader.is_paused:
            self.downloader.resume()
            self.pause_btn.config(text="暂停|Pause")
            self.status_label.config(text="下载中...|Downloading...")
        else:
            self.downloader.pause()
            self.pause_btn.config(text="继续|Resume")
            self.status_label.config(text="已暂停|Paused")
            
    def _cancel(self):
        """取消下载 Cancel download"""
        self.downloader.cancel()
        
    def run(self):
        """运行程序 Run program"""
        self.root.mainloop() 