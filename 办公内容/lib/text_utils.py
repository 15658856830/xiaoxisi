"""文本辅助工具 — 中文字符检测、字体选择等"""
import sys
from pathlib import Path

CN_FONT = "微软雅黑"
EN_FONT = "Arial"
FONT_FALLBACK = ["微软雅黑", "SimSun", "SimHei", "Arial"]


def has_cn(text: str) -> bool:
    """检测字符串是否包含中文字符"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)


def pick_font(text: str, cn_font: str = CN_FONT, en_font: str = EN_FONT) -> str:
    """根据文本内容选择字体"""
    return cn_font if has_cn(text) else en_font


def resolve_output(path: str | Path, subdir: str = "") -> Path:
    """返回 output/ 目录下的路径"""
    base = Path(__file__).resolve().parent.parent / "output"
    if subdir:
        base = base / subdir
    base.mkdir(parents=True, exist_ok=True)
    return base / path if path else base


def check_input(path: str | Path, script_name: str = "") -> Path:
    """校验输入文件存在，不存在则退出"""
    p = Path(path).resolve()
    if not p.exists():
        tag = f"[{script_name}] " if script_name else ""
        print(f"{tag}输入文件不存在: {p}")
        sys.exit(1)
    return p
