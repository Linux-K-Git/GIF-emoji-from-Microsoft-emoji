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
from PIL import Image, ImageSequence, ImageFilter
from io import BytesIO
import numpy as np

def clean_frame_edge(frame, target_color=(255, 0, 0, 255), threshold=50, erase_width=3):
    """
    清除帧中特定颜色的边缘杂色，并擦除非透明区域的边缘像素。
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
    
    # 创建一个掩码，仅对非透明区域进行边缘像素擦除处理
    mask = cleaned_frame.split()[-1].point(lambda p: p > 0 and 255)
    mask_data = np.array(mask)
    
    height, width = mask_data.shape
    for y in range(height):
        for x in range(width):
            if mask_data[y, x] == 255:
                # 检查是否在边缘
                for dy in range(-erase_width, erase_width + 1):
                    for dx in range(-erase_width, erase_width + 1):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width and mask_data[ny, nx] == 0:
                            data[y, x, 3] = 0  # 将像素设置为透明
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

def save_gif(frames, output_path, target_color=(255, 0, 0, 255), threshold=50, erase_width=3):
    try:
        print("Saving GIF...")
        cleaned_frames = []
        for frame in frames:
            # 对每一帧清除不必要的边缘杂色，并进行边缘像素擦除处理
            cleaned_frame = clean_frame_edge(frame, target_color, threshold, erase_width)
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
            save_gif(frames, output_path, erase_width=3)  # 调整边缘像素擦除宽度


if __name__ == "__main__":
    main()
