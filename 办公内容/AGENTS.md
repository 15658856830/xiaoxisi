# 小西斯 — 办公自动化
 
 Python 脚本解决 Word/Excel/PPT/PDF 的日常制作与编辑。
 
## 数据链
 
 ```
 数据来源 → scripts/脚本处理 → lib/工具 + templates/模板组装 → output/生成结果
 ```
 
 脚本只有一条链路：读输入 → 处理数据 → 调 lib 工具 + 套 template → 写 output。
 
## 工作流程

1. 理解需求：查看相关文件
2. 对齐目标：陈述理解，你确认
3. 拆解计划：列出步骤，给你看
4. 执行一步 → 反馈 → 你决定「继续还是调整」
5. 输出 demo（单页样板/典型段落）
6. 对照需求检查：不满足则回退到 4
7. 你确认 demo → 全量输出
8. 总结成果物

任何时候说「不对」或「做下一个」，我当场调整，不等全跑完。

## 多线并行

当任务可以拆分为互不依赖的子任务时，我会自动启用多个 agent 并行工作来压缩总耗时：

- 同时处理多个 Office 文件（如批量美化 PPT、同时处理 Word 和 Excel）
- 同时运行多个独立的 Python 脚本
- 多文件处理时，读输入、模板组装、输出三步流水线并行

你不需要手动拆分任务，交给我的时候说明整体目标和产出要求即可，我自行判断哪些环节可以并行。

## 工作约束
 
 动手前：定清楚输入/目标格式/模板 → 路径基于项目根目录 → 检查依赖是否安装。
 
 写脚本时：
 - 模板先打开看结构再填，不猜
 - 中文编码：读 utf-8，写 csv 用 utf-8-sig
 - 中文字体：微软雅黑 → SimSun → SimHei → Arial
 - 路径用 Path 拼接，不手拼字符串
 - 三种异常必须捕获：文件不存在、格式解析失败、库没装。报错要说清哪个文件 + 什么错 + 怎么修
 - 幂等：跑两次不脏数据，输出已存在则加序号
 - 跑完清理临时文件
 - 上下文管理：复杂任务每完成一轮确认就主动压缩上下文，不等到挤爆
 
 跑完后：验证文件存在且不为0 → 打印路径 + 耗时 + 摘要。
 
## 技术栈
 
 Word: python-docx | Excel: openpyxl, pandas | PPT: python-pptx | PDF: pypdf2, pdfplumber, reportlab | 图表: matplotlib
 
## 目录
 
 ```
 scripts/word, excel, ppt/   # 脚本
 templates/word, excel, ppt/ # 模板文件
 lib/                        # 公共工具
 output/                     # 生成结果
 ```
 
## 首次使用
 
 ```powershell
 python -m venv .venv && .\.venv\Scripts\Activate.ps1 && pip install -r requirements.txt
 ```
