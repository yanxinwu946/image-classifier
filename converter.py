import os
import argparse
from PIL import Image

def convert_images(source_dir, target_ext, delete_original):
    # 统一后缀格式
    target_ext = target_ext.lower().replace('.', '')
    if target_ext not in ['jpg', 'jpeg', 'png']:
        print("[-] 错误: 目前仅支持转换为 jpg 或 png")
        return

    # 支持读取的源格式
    source_extensions = ('.webp', '.bmp', '.jpeg', '.jpg', '.png', '.heic', '.tiff')
    
    print(f"[*] 启动转换任务: 目标格式 -> {target_ext.upper()}")
    
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith(source_extensions):
                # 检查是否已经是目标格式（且后缀名一致）
                if filename.lower().endswith(f".{target_ext}"):
                    continue

                file_path = os.path.join(root, filename)
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(root, f"{base_name}.{target_ext}")

                try:
                    with Image.open(file_path) as img:
                        # 如果转 JPG，需要处理透明通道 (RGBA -> RGB)
                        if target_ext in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'P', 'LA'):
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = background
                        elif img.mode != 'RGB' and target_ext in ['jpg', 'jpeg']:
                            img = img.convert('RGB')

                        # 保存
                        img.save(output_path, target_ext.upper(), quality=95, optimize=True)
                        print(f"[+] 转换成功: {filename} -> {base_name}.{target_ext}")

                    # 转换成功后根据参数决定是否删除原图
                    if delete_original:
                        os.remove(file_path)

                except Exception as e:
                    print(f"[!] 转换失败 {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量转换图片格式为 JPG 或 PNG")
    parser.add_argument("path", nargs="?", default=".", help="文件夹路径")
    parser.add_argument("--to", default="jpg", choices=['jpg', 'png'], help="目标格式 (默认 jpg)")
    parser.add_argument("--del", dest="delete", action="store_true", help="转换后删除原文件")

    args = parser.parse_args()
    
    abs_path = os.path.abspath(args.path)
    if os.path.isdir(abs_path):
        convert_images(abs_path, args.to, args.delete)
    else:
        print(f"[-] 路径不存在: {abs_path}")
