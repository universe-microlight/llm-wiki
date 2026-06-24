#!/usr/bin/env python3
"""
LLM Wiki 资料导入脚本

用法:
    python scripts/ingest.py <file_or_directory>
    python scripts/ingest.py --url <url>
    python scripts/ingest.py raw/papers/
"""

import os
import sys
import argparse
import yaml
import hashlib
from datetime import datetime
from pathlib import Path

# 支持的文件类型
SUPPORTED_TYPES = {
    '.pdf': 'pdf',
    '.docx': 'word',
    '.doc': 'word',
    '.pptx': 'powerpoint',
    '.ppt': 'powerpoint',
    '.md': 'markdown',
    '.txt': 'text',
    '.html': 'html',
    '.htm': 'html',
    '.csv': 'csv',
    '.json': 'json',
    '.xml': 'xml',
    '.yaml': 'yaml',
    '.yml': 'yaml',
}

def get_file_type(file_path):
    """获取文件类型"""
    ext = Path(file_path).suffix.lower()
    return SUPPORTED_TYPES.get(ext, 'unknown')

def calculate_hash(file_path):
    """计算文件哈希"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()[:12]

def extract_text(file_path):
    """提取文件文本内容"""
    file_type = get_file_type(file_path)
    
    try:
        if file_type == 'markdown' or file_type == 'text':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_type == 'pdf':
            try:
                from pypdf import PdfReader
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                print("⚠️  需要安装 pypdf: pip install pypdf")
                return None
        
        elif file_type == 'word':
            try:
                from docx import Document
                doc = Document(file_path)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except ImportError:
                print("⚠️  需要安装 python-docx: pip install python-docx")
                return None
        
        elif file_type == 'html':
            try:
                from bs4 import BeautifulSoup
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    return soup.get_text()
            except ImportError:
                print("⚠️  需要安装 beautifulsoup4: pip install beautifulsoup4")
                return None
        
        else:
            print(f"⚠️  暂不支持 {file_type} 类型")
            return None
            
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

def create_summary_stub(file_path, text_content):
    """创建摘要存根"""
    file_name = Path(file_path).stem
    file_hash = calculate_hash(file_path)
    
    # 创建 frontmatter
    frontmatter = {
        'type': 'summary',
        'title': f"{file_name} - 摘要",
        'resource': str(file_path),
        'tags': ['auto-generated'],
        'timestamp': datetime.now().isoformat() + 'Z',
        'status': 'pending',  # 等待 AI 处理
        'file_hash': file_hash,
    }
    
    # 创建内容
    content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)}---

# {file_name}

## 概述

> ⚠️ 此摘要待 AI 生成。请让 AI 阅读原始资料并更新此页面。

## 原始资料信息

- **文件**: `{file_path}`
- **类型**: {get_file_type(file_path)}
- **大小**: {os.path.getsize(file_path)} bytes
- **导入时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 待处理

- [ ] 阅读原始资料
- [ ] 生成摘要
- [ ] 提取关键概念
- [ ] 建立交叉引用
- [ ] 更新索引

## 原文预览

```
{text_content[:500] if text_content else '无法提取文本'}
```
"""
    
    return content

def ingest_file(file_path, wiki_path='wiki'):
    """导入单个文件"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    if file_path.suffix.lower() not in SUPPORTED_TYPES:
        print(f"⚠️  不支持的文件类型: {file_path.suffix}")
        return False
    
    print(f"📥 导入: {file_path}")
    
    # 提取文本
    text_content = extract_text(file_path)
    
    # 创建摘要存根
    summary_content = create_summary_stub(file_path, text_content)
    
    # 生成摘要文件名
    slug = file_path.stem.lower().replace(' ', '-').replace('_', '-')
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')[:50]
    summary_path = Path(wiki_path) / 'summaries' / f"{slug}.md"
    
    # 确保目录存在
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入摘要
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ 摘要已创建: {summary_path}")
    print(f"💡 下一步: 让 AI 阅读 {file_path} 并更新 {summary_path}")
    
    return True

def ingest_directory(dir_path, wiki_path='wiki'):
    """导入目录中的所有文件"""
    dir_path = Path(dir_path)
    
    if not dir_path.is_dir():
        print(f"❌ 目录不存在: {dir_path}")
        return False
    
    print(f"📁 扫描目录: {dir_path}")
    
    success_count = 0
    total_count = 0
    
    for file_path in dir_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_TYPES:
            total_count += 1
            if ingest_file(file_path, wiki_path):
                success_count += 1
    
    print(f"\n📊 导入完成: {success_count}/{total_count} 个文件")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='LLM Wiki 资料导入工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/ingest.py raw/papers/transformer.pdf
  python scripts/ingest.py raw/articles/
  python scripts/ingest.py --url https://example.com/article
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        help='文件或目录路径'
    )
    
    parser.add_argument(
        '--url',
        help='从 URL 导入'
    )
    
    parser.add_argument(
        '--wiki-path',
        default='wiki',
        help='Wiki 目录路径 (默认: wiki)'
    )
    
    args = parser.parse_args()
    
    if args.url:
        print(f"🌐 URL 导入: {args.url}")
        print("⚠️  URL 导入功能开发中...")
        print("💡 临时方案: 使用浏览器保存网页到 raw/ 目录")
        return
    
    if not args.path:
        parser.print_help()
        print("\n💡 提示: 将文件放入 raw/ 目录，然后运行此脚本")
        return
    
    path = Path(args.path)
    
    if path.is_file():
        ingest_file(path, args.wiki_path)
    elif path.is_dir():
        ingest_directory(path, args.wiki_path)
    else:
        print(f"❌ 路径不存在: {path}")

if __name__ == '__main__':
    main()
