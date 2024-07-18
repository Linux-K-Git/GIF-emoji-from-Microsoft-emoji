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

import requests
from PIL import Image, ImageSequence, ImageFilter
from io import BytesIO
import numpy as np

def clean_frame_edge(frame, target_color=(255, 0, 0, 255), threshold=50, smooth_iterations=3):
    """
    清除帧中特定颜色的边缘杂色，并进行非透明区域的边缘柔化处理。
    """
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
    
    # 创建一个掩码，仅对非透明区域进行边缘柔化处理
    mask = cleaned_frame.split()[-1].point(lambda p: p > 0 and 255)
    
    # 增强边缘柔化强度
    for _ in range(smooth_iterations):
        cleaned_frame = cleaned_frame.filter(ImageFilter.SMOOTH)
        cleaned_frame = cleaned_frame.filter(ImageFilter.SMOOTH_MORE)
    
    # 仅将掩码覆盖的区域合并到原图中
    cleaned_frame.putalpha(mask)

    return cleaned_frame

def download_image(url):
    try:
        print("Downloading image...")
        proxies = {
            "http": "http://127.0.0.1:7897",
            "https": "http://127.0.0.1:7897",
        }
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 检查请求是否成功
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

def save_gif(frames, output_path, target_color=(255, 0, 0, 255), threshold=50, smooth_iterations=3):
    try:
        print("Saving GIF...")
        cleaned_frames = []
        for frame in frames:
            # 对每一帧清除不必要的边缘杂色，并进行边缘柔化处理
            cleaned_frame = clean_frame_edge(frame, target_color, threshold, smooth_iterations)
            cleaned_frames.append(cleaned_frame)
        
        # 使用第一帧保存 GIF，其余帧追加
        cleaned_frames[0].save(output_path, save_all=True, append_images=cleaned_frames[1:], loop=0, duration=100, disposal=2)
        print(f"GIF saved as {output_path}")
    except Exception as e:
        print(f"Error saving GIF: {e}")


def main():
    url = "https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Smiling%20Face%20with%20Hearts.png"
    img_data = download_image(url)

    if img_data:
        frames = process_image(img_data)

        if frames:
            output_path = "smiling_face_with_hearts.gif"
            save_gif(frames, output_path, smooth_iterations=5)  # 调整边缘柔化强度


if __name__ == "__main__":
    main()
