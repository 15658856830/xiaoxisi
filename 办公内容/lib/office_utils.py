 """办公通用工具 — 样式、格式化等辅助"""

 from pathlib import Path

 # 常用的中文字体回退列表
 FONT_FALLBACK = ["微软雅黑", "SimSun", "SimHei", "Arial"]


 def ensure_template(template_name: str, subdir: str) -> Path | None:
     """获取 templates/{subdir}/{template_name} 的路径，不存在则返回 None。"""
     p = Path(__file__).resolve().parent.parent / "templates" / subdir / template_name
     return p if p.exists() else None


 def pretty_time(seconds: float) -> str:
     """将秒数格式化为可读字符串。"""
     if seconds < 60:
         return f"{seconds:.1f} 秒"
     return f"{int(seconds // 60)} 分 {int(seconds % 60)} 秒"
