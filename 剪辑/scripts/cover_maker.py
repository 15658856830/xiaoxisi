#!/usr/bin/env python3
"""自动生成平台适配的封面图 — 抖音(9:16) 和 小红书(3:4)"""

import sys
from pathlib import Path
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[cover_maker] 依赖 Pillow 未安装，请运行: pip install pillow")
    sys.exit(1)


def make_cover(
    output_path: str,
    title: str,
    subtitle: str = "",
    platform: str = "douyin",
    bg_color: tuple = (0x2B, 0x57, 0x9A),
    text_color: tuple = (255, 255, 255),
    font_path: str | None = None,
) -> None:
    sizes = {"douyin": (1080, 1920), "xiaohongshu": (1080, 1440)}
    size = sizes.get(platform, (1080, 1920))
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype(font_path, 64) if font_path else ImageFont.load_default()
        sub_font = ImageFont.truetype(font_path, 36) if font_path else ImageFont.load_default()
    except Exception:
        title_font = sub_font = ImageFont.load_default()

    # 主标题居中
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = (size[0] - tw) // 2
    cy = (size[1] - th) // 2 - 60
    draw.text((cx, cy), title, fill=text_color, font=title_font)

    # 副标题
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        sx = (size[0] - sw) // 2
        sy = cy + th + 30
        draw.text((sx, sy), subtitle, fill=text_color, font=sub_font)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"[cover_maker] 封面已生成: {out} ({platform}, {size[0]}x{size[1]})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scripts/cover_maker.py <标题> [输出路径] [平台] [副标题]")
        sys.exit(1)
    title = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output/cover.png"
    platform = sys.argv[3] if len(sys.argv) > 3 else "douyin"
    subtitle = sys.argv[4] if len(sys.argv) > 4 else ""
    make_cover(out_path, title, subtitle, platform)
    print(f"  路径: {Path(out_path).resolve()}")
    print(f"  平台: {platform}")
    print(f"  标题: {title}")
    if subtitle:
        print(f"  副标题: {subtitle}")
    out = Path(out_path)
    if out.exists():
        print(f"  文件大小: {out.stat().st_size} 字节")
