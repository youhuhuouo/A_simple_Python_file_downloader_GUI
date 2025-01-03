#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单下载器入口
Simple downloader entry
"""

from src.gui.main_window import MainWindow

def main():
    """主函数 Main function"""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main() 