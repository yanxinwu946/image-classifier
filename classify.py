import os
import hashlib
import shutil
import argparse
from PIL import Image

def get_short_hash(file_path):
    """生成文件内容的6位MD5 hash"""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()[:6]
    except Exception:
        return None

def classify_images(source_dir, keep_original):
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif')
    dirs = ['landscape', 'portrait']

    # 在目标目录下创建文件夹
    for d in dirs:
        target_path = os.path.join(source_dir, d)
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    # 遍历指定文件夹
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # 跳过文件夹本身和非图片文件
        if os.path.isdir(file_path) or not filename.lower().endswith(extensions):
            continue

        try:
            # 1. 获取图片尺寸
            with Image.open(file_path) as img:
                width, height = img.size
                folder = 'landscape' if width >= height else 'portrait'
            
            # 2. 生成Hash命名
            file_ext = os.path.splitext(filename)[1].lower()
            short_hash = get_short_hash(file_path)
            if not short_hash: continue
            
            new_name = f"{short_hash}{file_ext}"
            final_dest = os.path.join(source_dir, folder, new_name)

            # 3. 冲突检查
            if os.path.exists(final_dest):
                print(f"[-] 冲突跳过: {filename} (Hash {short_hash} 已存在)")
                continue

            # 4. 执行操作
            if keep_original:
                shutil.copy2(file_path, final_dest)
                print(f"[+] 已复制: {filename} -> {folder}/{new_name}")
            else:
                shutil.move(file_path, final_dest)
                print(f"[+] 已移动: {filename} -> {folder}/{new_name}")

        except Exception as e:
            print(f"[!] 无法处理 {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="按横竖版自动分类图片并重命名为6位Hash")
    parser.add_argument("path", nargs="?", default=".", help="目标文件夹路径 (默认为当前目录)")
    parser.add_argument("--keep", action="store_true", help="保留原文件 (即执行复制操作，默认是移动/删除原位)")
    
    args = parser.parse_args()
    
    # 转换绝对路径
    target_dir = os.path.abspath(args.path)
    if not os.path.isdir(target_dir):
        print(f"错误: 路径 '{target_dir}' 不存在")
    else:
        classify_images(target_dir, args.keep)
