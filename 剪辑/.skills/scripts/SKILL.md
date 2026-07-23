---
name: python-aux-scripts
description: Python 辅助脚本技能包，用于批量素材处理、封面生成、文件名管理、格式转换等
metadata:
  short-description: Python 剪辑辅助脚本
  category: automation
  tools: [python, pillow, moviepy, opencv]
---

# Python 辅助脚本技能

## 已注册脚本

| 脚本 | 功能 | 调用方式 |
|------|------|----------|
| scripts/batch_rename.py | 批量重命名素材为统一格式 | python scripts/batch_rename.py |
| scripts/cover_maker.py | 自动生成平台适配的封面图 | python scripts/cover_maker.py |
| scripts/resize_video.py | 批量裁剪/转格式（调用 ffmpeg） | python scripts/resize_video.py |

## 依赖安装

powershell: pip install moviepy opencv-python pillow

## 开发新脚本规范

- 放在 scripts/ 目录下
- 脚本名用 snake_case
- 必须有 main 入口
- 路径用 pathlib.Path 拼接，不手写字符串
- 输出已存在则跳过（幂等），可加 --force 强制覆盖
- 三种异常必须捕获：文件不存在、格式解析失败、库没装
- 报错格式：[脚本名] 哪个文件 + 什么错 + 怎么修
- 跑完打印：路径 + 耗时 + 摘要