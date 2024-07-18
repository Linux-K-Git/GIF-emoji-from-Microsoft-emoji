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
 */

import requests
from PIL import Image, ImageSequence
from io import BytesIO
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import re
import os
import urllib.parse

def clean_frame_edge(frame, target_color=(255, 0, 0, 255), threshold=50, erase_width=3): 
    frame = frame.convert("RGBA")
    data = np.array(frame)
    red, green, blue, alpha = data.T

    areas_to_clear = (abs(red - target_color[0]) < threshold) & \
                     (abs(green - target_color[1]) < threshold) & \
                     (abs(blue - target_color[2]) < threshold) & \
                     (alpha == target_color[3])

    data[..., :-1][areas_to_clear.T] = (0, 0, 0)
    data[..., -1][areas_to_clear.T] = 0

    cleaned_frame = Image.fromarray(data)
    
    mask = cleaned_frame.split()[-1].point(lambda p: p > 0 and 255)
    mask_data = np.array(mask)
    
    height, width = mask_data.shape
    for y in range(height):
        for x in range(width):
            if mask_data[y, x] == 255:
                for dy in range(-erase_width, erase_width + 1):
                    for dx in range(-erase_width, erase_width + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and mask_data[ny, nx] == 0:
                            data[y, x, 3] = 0
                            break

    cleaned_frame = Image.fromarray(data)

    return cleaned_frame

def download_image(url, proxies):
    try:
        print(f"Downloading image from {url}...")
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        print("Image downloaded successfully.")
        return response.content
    except requests.RequestException as e:
        print(f"Error downloading image: {e}")
        return None

def process_image(img_data):
    try:
        print("Opening image...")
        img = Image.open(BytesIO(img_data))
        print("Image opened successfully.")

        if img.is_animated:
            print("Image is animated. Extracting frames...")
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            print(f"Extracted {len(frames)} frames.")
        else:
            print("Image is not animated.")
            frames = [img]

        return frames
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def resize_frame(frame, size):
    return frame.resize(size, Image.LANCZOS)

def save_gif(frames, output_path, target_color=(255, 0, 0, 255), threshold=30, erase_width=1, fps=None): 
    try:
        print("Saving GIF...")
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(clean_frame_edge, frame, target_color, threshold, erase_width) for frame in frames]
            cleaned_frames = [future.result() for future in futures]
        
        # Calculate duration based on the desired fps
        if fps:
            duration = int(1000 / fps)
        else:
            duration = 100  # Default duration if fps is not specified
        
        cleaned_frames[0].save(output_path, save_all=True, append_images=cleaned_frames[1:], loop=0, duration=duration, disposal=2, optimize=True)
        print(f"GIF saved as {output_path}")
    except Exception as e:
        print(f"Error saving GIF: {e}")

def extract_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    urls = re.findall(r'src="([^"]+)"', content)
    return [url.strip() for url in urls if url.strip()]

def generate_filename_from_url(url):
    parsed_url = urllib.parse.urlparse(url)
    filename = urllib.parse.unquote(os.path.basename(parsed_url.path))
    return filename

def main():
    # Variables to control frame rate, save path, and proxy address
    fps =  30 
    # Desired frame rate 默认帧率
    save_path = "./emojis_print_end/"  
    # Path to save the GIFs 保存路径
    proxy_address = "http://127.0.0.1:7897"  
    # Proxy address 代理地址

    # Ensure the save path exists
    os.makedirs(save_path, exist_ok=True)

    proxies = {
        "http": proxy_address,
        "https": proxy_address,
    }

    urls = extract_urls_from_file("url.txt")
    if not urls:
        print("No valid URLs found in url.txt.")
        return

    for url in urls:
        img_data = download_image(url, proxies)
        if img_data:
            frames = process_image(img_data)
            if frames:
                base_filename = generate_filename_from_url(url)

                for size in [(256, 256), (64, 64)]:
                    resized_frames = [resize_frame(frame, size) for frame in frames]
                    output_path = os.path.join(save_path, f"{base_filename}_{size[0]}x{size[1]}.gif")
                    save_gif(resized_frames, output_path, erase_width=1, fps=fps)

if __name__ == "__main__":
    main()

# 变量控制：fps、save_path 和 proxy_address 通过变量控制，并在 main 函数中传递。
# 从文件读取URL：extract_urls_from_file 函数从 url.txt 文件中读取所有URL。
# 下载和处理图像：使用指定的代理地址下载图像，并处理生成GIF。
# 保存路径创建：确保保存路径存在，如果不存在则创建。
# 保存GIF：使用指定帧率保存GIF。
# 实现从 url.txt 文件中正则匹配读取URL，下载图像并生成高帧率、高质量的GIF图像（允许多个url）
# 格式为：<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Smiling%20Face%20with%20Hearts.png" alt="Smiling Face with Hearts" width="1024" height="1024" />。
