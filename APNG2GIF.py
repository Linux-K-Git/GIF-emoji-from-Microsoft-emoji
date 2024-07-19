'''
/* 
 * GIF-emoji-from-Microsoft-emoji
 * Copyright © 2024 Linux-K
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 * https://github.com/Linux-K-Git/GIF-emoji-from-Microsoft-emoji
 */
'''

import os
import imageio
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def process_image(file_name, input_folder, output_folder, resolution, frame_rate):
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.gif')

    try:
        # 读取APNG文件
        reader = imageio.get_reader(input_path, 'pillow')
        frames = []
        durations = []
        for frame in reader:
            image = Image.fromarray(frame).convert("RGBA")
            # 调整图片大小
            image = image.resize(resolution, Image.LANCZOS)
            frames.append(image)
            durations.append(reader.get_meta_data()['duration'])

        if frames:
            # 使用高位颜色深度进行处理
            high_quality_frames = [frame.convert("P", palette=Image.ADAPTIVE, colors=256) for frame in frames]
            
            # 保存为GIF
            high_quality_frames[0].save(
                output_path,
                save_all=True,
                append_images=high_quality_frames[1:],
                optimize=False,
                duration=[int(1000 / frame_rate) for _ in durations],
                loop=0,
                disposal=2,  # 使用 'disposal=2' 以确保每一帧独立显示
                transparency=0  # 确保透明度处理正确
            )
            print(f"Converted {input_path} to {output_path}")
        else:
            print(f"No frames extracted from {input_path}. Skipping.")

    except Exception as e:
        print(f"Failed to process {input_path}: {e}")

def convert_apng_to_gif(input_folder, resolution=(800, 600), frame_rate=10):
    for root, _, files in os.walk(input_folder):
        # 获取所有PNG文件
        png_files = [f for f in files if f.lower().endswith('.png')]
        if not png_files:
            continue

        output_folder = os.path.join(root, 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 使用多线程处理图片
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_image, file_name, root, output_folder, resolution, frame_rate)
                for file_name in png_files
            ]
            # 等待所有任务完成
            for future in futures:
                future.result()

if __name__ == "__main__":
    input_folder = 'xxxxx'  # 输入APNG所在文件夹路径，注意不同的系统采用对应的路径格式，如window中为双斜线，而Linux则为单斜线
    resolution = (256, 256)  # 自定义分辨率
    frame_rate = 24  # 自定义帧率

    convert_apng_to_gif(input_folder, resolution, frame_rate)

#将文件夹内的所有APNG图片转换为GIF格式，保存到同一文件夹的output子文件夹中。
#这是一个使用python代码实现APNG转换位GIF图像格式的快速解决脚本，调用几乎所有的CPU线程资源在短时间内迅速转换，而不需要之前方法一个一个下载录制，但也不是完美的