#!/usr/bin/env python3
"""批量重命名素材为统一格式: 日期_类型_内容_v{N}.后缀"""

import sys
from pathlib import Path
from datetime import date
import os


def main(dir_path: str, prefix: str = "") -> None:
    src = Path(dir_path)
    if not src.exists():
        print(f"[batch_rename] 目录不存在: {dir_path}")
        sys.exit(1)
    if not src.is_dir():
        print(f"[batch_rename] 路径不是目录: {dir_path}")
        sys.exit(1)
    src = src.resolve()

    today = date.today().strftime("%Y%m%d")
    ext_map = {
        ".mp4": "video", ".mov": "video", ".avi": "video",
        ".jpg": "img", ".jpeg": "img", ".png": "img",
        ".mp3": "audio", ".wav": "audio", ".aac": "audio",
    }

    renamed = 0
    for f in sorted(src.iterdir()):
        if f.is_dir() or f.name.startswith("."):
            continue
        if not os.access(f, os.R_OK):
            print(f"  [跳过] 无读取权限: {f.name}")
            continue
        ext = f.suffix.lower()
        ftype = ext_map.get(ext, "other")
        pfx = f"{prefix}_" if prefix else ""

        # 找下一个可用序号（幂等，不覆盖已有）
        stem = f"{today}_{ftype}_{pfx}"
        for i in range(1, 999):
            new_name = f"{stem}v{i}{ext}"
            new_path = src / new_name
            if not new_path.exists():
                try:
                    f.rename(new_path)
                    renamed += 1
                    print(f"  {f.name} -> {new_name}")
                except PermissionError:
                    print(f"  [跳过] 权限不足: {f.name}")
                except OSError as e:
                    print(f"  [错误] 重命名失败 {f.name}: {e}")
                break

    print(f"完成: 重命名 {renamed} 个文件")
    print(f"  路径: {src.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scripts/batch_rename.py <素材目录> [前缀]")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
