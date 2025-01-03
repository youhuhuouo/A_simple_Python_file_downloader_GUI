# Python Download Manager (Python下载管理器)

一个使用Python和ttk构建的简单下载管理器。

A simple download manager built with Python and ttk.

## 功能特点 (Features)
- 支持单个文件下载 (Single file download)
- 显示下载进度 (Download progress display)
- 可暂停和继续下载 (Pause and resume downloads)
- 美观的ttk界面 (Beautiful ttk interface)
- 自动保存到downloads目录 (Auto save to downloads directory)

## 安装要求 (Requirements)
- Python 3.8+
- tkinter/ttk (内置 built-in)
- requests

## 使用方法 (Usage)
1. 安装依赖 (Install dependencies):
```bash
pip install -r requirements.txt
```

2. 运行程序 (Run the program):
```bash
python run.py
```

## 项目结构 (Project Structure)
```
├── run.py                 # 程序入口 (Entry point)
├── src/                   # 源代码目录 (Source code directory)
│   ├── gui/              # GUI相关代码 (GUI related code)
│   ├── core/             # 核心下载功能 (Core download functionality)
│   └── utils/            # 工具函数 (Utility functions)
├── requirements.txt       # 项目依赖 (Dependencies)
└── README.md             # 项目说明 (Documentation)
``` 