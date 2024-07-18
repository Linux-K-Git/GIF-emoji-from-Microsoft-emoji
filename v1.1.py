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
from PIL import Image, ImageSequence
from io import BytesIO

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

def save_gif(frames, output_path):
    try:
        print("Saving GIF...")
        # 将帧转换为 P 模式并指定透明色
        frames_converted = [frame.convert('RGBA').quantize() for frame in frames]
        
        # 使用第一帧保存 GIF，其余帧追加
        frames_converted[0].save(output_path, save_all=True, append_images=frames_converted[1:], loop=0, duration=100, transparency=0)
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
            save_gif(frames, output_path)

if __name__ == "__main__":
    main()
