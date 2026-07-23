#!/usr/bin/env python3
"""批量裁剪/转格式（调用 ffmpeg）"""

import subprocess
import sys
from pathlib import Path


def main(input_dir: str, output_dir: str, target: str = "douyin") -> None:
    src = Path(input_dir)
    if not src.exists():
        print(f"[resize_video] 输入目录不存在: {input_dir}")
        sys.exit(1)
    if not src.is_dir():
        print(f"[resize_video] 路径不是目录: {input_dir}")
        sys.exit(1)
    src = src.resolve()
    dst = Path(output_dir)
    dst = dst.resolve()
    dst.mkdir(parents=True, exist_ok=True)

    profiles = {
        "douyin":       {"scale": "1080:1920", "crop": "iw*9/16:ih"},
        "xiaohongshu":  {"scale": "1080:1344", "crop": "iw*3/4:ih"},
    }
    profile = profiles.get(target, profiles["douyin"])

    # 验证 ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[resize_video] ffmpeg 未安装或不在 PATH 中")
        sys.exit(1)

    video_exts = {".mp4", ".mov", ".avi", ".mkv"}
    converted = 0

    for f in sorted(src.iterdir()):
        if f.suffix.lower() not in video_exts:
            continue
        out_path = dst / f"{f.stem}_{target}{f.suffix}"
        if out_path.exists():
            print(f"  跳过(已存在): {out_path.name}")
            continue

        vf = f"crop={profile['crop']},scale={profile['scale']}"
        cmd = [
            "ffmpeg", "-i", str(f),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "320k",
            "-y", str(out_path),
        ]
        print(f"  {f.name} -> {out_path.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  [错误] ffmpeg 失败 (返回码 {result.returncode})")
            print(f"  stderr: {result.stderr[:200]}")
            if out_path.exists():
                out_path.unlink()
            continue
        if out_path.exists() and out_path.stat().st_size > 0:
            converted += 1
        else:
            print(f"  [错误] 输出文件无效: {out_path}")

    print(f"\n完成: 转换 {converted} 个文件 -> {dst}")
    print(f"  目标: {target}")
    for f in sorted(dst.iterdir()):
        sz = f.stat().st_size / (1024*1024)
        print(f"  {f.name} ({sz:.1f} MB)" if sz > 0.1 else f"  {f.name} ({f.stat().st_size} B)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python scripts/resize_video.py <输入目录> <输出目录> [平台]")
        print("  平台: douyin (默认), xiaohongshu")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "douyin")
