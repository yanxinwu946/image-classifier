import os
import shutil
import argparse

def filter_by_size(source_dir, threshold_mb, keep_original):
    # 转换为字节
    threshold_bytes = threshold_mb * 1024 * 1024
    target_dir = os.path.join(source_dir, "big")

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"[*] 正在扫描目录: {source_dir}")
    print(f"[*] 目标大小阈值: > {threshold_mb}MB")

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        
        # 排除文件夹本身和“big”目录
        if not os.path.isfile(file_path) or filename == "big":
            continue

        try:
            file_size = os.path.getsize(file_path)
            
            if file_size > threshold_bytes:
                dest_path = os.path.join(target_dir, filename)
                
                # 处理重名
                if os.path.exists(dest_path):
                    print(f"[-] 跳过已存在的文件: {filename}")
                    continue

                if keep_original:
                    shutil.copy2(file_path, dest_path)
                    print(f"[+] 已复制: {filename} ({file_size/1024/1024:.2f}MB)")
                else:
                    shutil.move(file_path, dest_path)
                    print(f"[+] 已移动: {filename} ({file_size/1024/1024:.2f}MB)")

        except Exception as e:
            print(f"[!] 无法处理 {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将大于指定大小的文件移至 big 目录")
    parser.add_argument("path", nargs="?", default=".", help="目标路径 (默认当前目录)")
    parser.add_argument("--size", type=float, default=3.0, help="大小阈值单位MB (默认 3)")
    parser.add_argument("--keep", action="store_true", help="保留原文件 (执行复制操作)")

    args = parser.parse_args()
    
    abs_path = os.path.abspath(args.path)
    if os.path.isdir(abs_path):
        filter_by_size(abs_path, args.size, args.keep)
    else:
        print(f"错误: 路径 '{abs_path}' 不存在")
