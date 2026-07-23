---
name: ffmpeg-batch-processing
description: FFmpeg 命令行视频处理技能包，涵盖批量转码、裁剪、合并、截取等常见操作
metadata:
  short-description: FFmpeg 批量视频处理
  category: video-processing
  tools: [ffmpeg, python]
---

# FFmpeg 批量处理技能

## 常用命令模板

### 批量转码（H.264 抖音版）
`
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 320k output.mp4
`

### 批量裁剪为 9:16（抖音竖屏）
`
ffmpeg -i input.mp4 -vf "crop=iw*(9/16):ih,scale=1080:1920" -c:a copy output.mp4
`

### 批量裁剪为 3:4（小红书竖屏）
`
ffmpeg -i input.mp4 -vf "crop=iw*(3/4):ih,scale=1080:1344" -c:a copy output.mp4
`

### 截取片段
`
ffmpeg -i input.mp4 -ss 00:00:10 -t 30 -c copy clip.mp4
`

### 合并多个视频
`
# 创建 filelist.txt 内容：
# file 'video1.mp4'
# file 'video2.mp4'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4
`

### 提取音频
`
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
`

### 替换音频轨道
`
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
`

### 添加淡入淡出
`
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=1" -af "afade=t=in:st=0:d=0.5,afade=t=out:st=9.5:d=1" output.mp4
`

## 调用规则

- 优先用 剪映PC版 完成剪辑工作，ffmpeg 只处理剪映无法批量处理或无法完成的环节
- 所有 ffmpeg 命令需要干燥运行：输出已存在则跳过（不覆盖已有成果）
- 跑完 ffmpeg 后验证输出文件存在且大小不为 0
