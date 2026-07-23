 """文件操作辅助工具"""

 import os
 import shutil
 from pathlib import Path


 def ensure_dir(path: str | Path) -> Path:
     """确保目录存在，不存在则创建。"""
     p = Path(path)
     p.mkdir(parents=True, exist_ok=True)
     return p


 def safe_copy(src: str | Path, dst: str | Path) -> Path:
     """安全复制文件，目标已存在时自动添加序号。"""
     src, dst = Path(src), Path(dst)
     if not dst.exists():
         return Path(shutil.copy2(src, dst))

     stem, suffix = dst.stem, dst.suffix
     for i in range(1, 100):
         new_dst = dst.with_name(f"{stem}_backup{i}{suffix}")
         if not new_dst.exists():
             return Path(shutil.copy2(src, new_dst))
     raise FileExistsError(f"无法创建备份文件，已达上限: {dst}")


 def resolve_output(path: str | Path, subdir: str = "") -> Path:
     """返回 output/ 目录下的路径。"""
     base = Path(__file__).resolve().parent.parent / "output"
     if subdir:
         base = base / subdir
     ensure_dir(base)
     return base / path if path else base
