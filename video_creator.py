from moviepy.editor import *
import os
from natsort import natsorted

def create_zoom_clip(image_path, duration=2):
    # 创建图片剪辑
    clip = ImageClip(image_path)
    
    # 定义缩放函数
    def zoom(t):
        # 从1.0变到1.2
        zoom_factor = 1.0 + (0.2 * t/duration)
        return zoom_factor
    
    # 应用缩放效果
    clip = clip.resize(zoom)
    # 设置持续时间
    clip = clip.set_duration(duration)
    
    return clip

def process_image_batch(image_files, output_path, start_index):
    # 创建视频片段列表
    clips = []
    
    # 处理每张图片
    for img in image_files:
        clip = create_zoom_clip(img)
        clips.append(clip)
    
    # 连接所有片段
    final_clip = concatenate_videoclips(clips)
    
    # 添加背景音乐
    audio = AudioFileClip("/Users/liyihang/Downloads/cursortest/shorts/biubiubiu.m4a")
    # 裁剪音频至视频长度
    audio = audio.subclip(0, final_clip.duration)
    
    # 设置音频
    final_clip = final_clip.set_audio(audio)
    
    # 写入文件
    final_clip.write_videofile(
        f"{output_path}/output_{start_index}.mp4",
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # 清理内存
    final_clip.close()
    audio.close()

def main():
    # 输入输出路径
    input_dir = "/Users/liyihang/Downloads/cursortest/shorts/imgs"
    output_dir = "/Users/liyihang/Downloads/cursortest/shorts/output"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有图片文件并排序
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files = natsorted(image_files)  # 自然排序
    
    # 按每10张图片分组处理
    for i in range(0, len(image_files), 10):
        batch = image_files[i:i+10]
        if batch:  # 确保批次不为空
            process_image_batch(batch, output_dir, i//10)

if __name__ == "__main__":
    main() 