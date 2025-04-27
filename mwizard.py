import os
import argparse
from pathlib import Path

# 预定义的隐蔽映射表 (编码表)
ENCODE_MAP = {
    # 图片
    'jpg': 'a1b2', 'jpeg': 'c3d4', 'png': 'e5f6', 'gif': 'g7h8', 'webp': 'i9j0',
    # 文档
    'pdf': 'k1l2', 'doc': 'm3n4', 'docx': 'o5p6', 'xls': 'q7r8', 'xlsx': 's9t0',
    'ppt': 'u1v2', 'pptx': 'w3x4', 'txt': 'y5z6', 'csv': 'a7b8',
    # 压缩包
    'zip': 'c9d0', 'rar': 'e1f2', '7z': 'g3h4', 'tar': 'i5j6', 'gz': 'k7l8',
    # 媒体
    'mp3': 'm9n0', 'wav': 'o1p2', 'mp4': 'q3r4', 'avi': 's5t6', 'mkv': 'u7v8',
    # 可执行文件
    'exe': 'w9x0', 'msi': 'y1z2', 'dll': 'a3b4', 'sys': 'c5d6'
}

# 解码表（自动生成）
DECODE_MAP = {v: k for k, v in ENCODE_MAP.items()}

def encode_filename(filename):
    """编码文件名后缀"""
    ext = Path(filename).suffix[1:].lower()  # 获取不带点的后缀
    if ext in ENCODE_MAP:
        return f"{Path(filename).stem}.{ENCODE_MAP[ext]}"
    return filename

def decode_filename(filename):
    """解码文件名后缀"""
    ext = Path(filename).suffix[1:].lower()
    if ext in DECODE_MAP:
        return f"{Path(filename).stem}.{DECODE_MAP[ext]}"
    return filename

def process_path(target_path, operation, recursive=False):
    """处理文件或目录"""
    if os.path.isfile(target_path):
        original = target_path
        new_path = os.path.join(
            os.path.dirname(original),
            operation(os.path.basename(original))
        )
        if original != new_path:
            os.rename(original, new_path)
            print(f"Processed: {original} -> {new_path}")
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                original = os.path.join(root, file)
                new_path = os.path.join(
                    root,
                    operation(file)
                )
                if original != new_path:
                    os.rename(original, new_path)
                    print(f"Processed: {original} -> {new_path}")
            if not recursive:
                break
    else:
        print(f"Error: Path '{target_path}' does not exist")

def main():
    parser = argparse.ArgumentParser(
        description="文件后缀隐蔽映射工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  编码单个文件: %(prog)s -e file.jpg
  解码单个文件: %(prog)s -d file.a1b2
  编码目录: %(prog)s -e /path/to/dir -r
  解码目录: %(prog)s -d /path/to/dir"""
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', action='store_true', help="编码文件后缀")
    group.add_argument('-d', '--decode', action='store_true', help="解码文件后缀")
    
    parser.add_argument('path', help="文件或目录路径")
    parser.add_argument('-r', '--recursive', action='store_true', 
                       help="递归处理子目录（仅当路径为目录时有效）")
    
    args = parser.parse_args()
    
    operation = encode_filename if args.encode else decode_filename
    process_path(args.path, operation, args.recursive)

if __name__ == "__main__":
    main()