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

def download_image(url):
    try:
        print("Downloading image...")
        proxies = {
            "http": "http://127.0.0.1:7897",
            "https": "http://127.0.0.1:7897",
        }
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
    return frame.resize(size, Image.Resampling.LANCZOS)

def save_gif(frames, output_path, target_color=(255, 0, 0, 255), threshold=30, erase_width=1): #threshold控制越贴近黑色的符合删除度，值越低删除的像素越少，适当控制以减少错误
    try:
        print("Saving GIF...")
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(clean_frame_edge, frame, target_color, threshold, erase_width) for frame in frames]
            cleaned_frames = [future.result() for future in futures]
        
        cleaned_frames[0].save(output_path, save_all=True, append_images=cleaned_frames[1:], loop=0, duration=100, disposal=2)
        print(f"GIF saved as {output_path}")
    except Exception as e:
        print(f"Error saving GIF: {e}")

def extract_url_from_html(html):
    match = re.search(r'src="([^"]+)"', html)
    if match:
        return match.group(1)
    return None

def generate_filename_from_url(url):
    # 解析 URL，获取文件名部分并解码
    parsed_url = urllib.parse.urlparse(url)
    filename = urllib.parse.unquote(os.path.basename(parsed_url.path))
    
    # 将空格替换为下划线（可选）
    # filename = filename.replace(' ', '_')
    
    return filename

def main():
    html_input = input("Enter the HTML code: ")
    url = extract_url_from_html(html_input)
    if not url:
        print("No valid URL found in the input.")
        return

    img_data = download_image(url)
    if img_data:
        frames = process_image(img_data)
        if frames:
            base_filename = generate_filename_from_url(url)

            # 生成两种分辨率的GIF图像
            for size in [(256, 256), (84, 84)]:
                resized_frames = [resize_frame(frame, size) for frame in frames]
                output_path = f"./emojis_print/{base_filename}_{size[0]}x{size[1]}.gif"
                save_gif(resized_frames, output_path, erase_width=1)

if __name__ == "__main__":
    main()

##终端输入格式为：<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Smiling%20Face%20with%20Hearts.png" alt="Smiling Face with Hearts" width="25" height="25" />
##正则过滤src后内容并作为文件名保存 https://github.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis