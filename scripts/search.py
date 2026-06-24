#!/usr/bin/env python3
"""
LLM Wiki 搜索工具

用法:
    python scripts/search.py "查询内容"
    python scripts/search.py --query "注意力机制" --max-results 5
"""

import os
import sys
import argparse
import yaml
import re
from pathlib import Path
from datetime import datetime

def load_frontmatter(file_path):
    """加载文件的 frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 YAML frontmatter
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                frontmatter_yaml = content[3:end].strip()
                frontmatter = yaml.safe_load(frontmatter_yaml)
                return frontmatter
    except Exception:
        pass
    return {}

def search_wiki(query, wiki_path='wiki', max_results=10, min_score=0.5):
    """搜索 wiki"""
    wiki_path = Path(wiki_path)
    results = []
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    # 遍历所有 markdown 文件
    for md_file in wiki_path.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 加载 frontmatter
            frontmatter = load_frontmatter(md_file)
            
            # 计算相关度分数
            score = 0
            content_lower = content.lower()
            
            # 标题匹配（权重最高）
            title = frontmatter.get('title', '').lower()
            if query_lower in title:
                score += 3
            for word in query_words:
                if word in title:
                    score += 1
            
            # 标签匹配
            tags = frontmatter.get('tags', [])
            for tag in tags:
                if isinstance(tag, str):
                    if query_lower in tag.lower():
                        score += 2
                    for word in query_words:
                        if word in tag.lower():
                            score += 0.5
            
            # 描述匹配
            description = frontmatter.get('description', '').lower()
            if query_lower in description:
                score += 2
            for word in query_words:
                if word in description:
                    score += 0.5
            
            # 内容匹配
            for word in query_words:
                count = content_lower.count(word)
                score += min(count * 0.1, 2)  # 最多加 2 分
            
            # 完整查询匹配
            if query_lower in content_lower:
                score += 1
            
            # 归一化分数
            score = min(score / 5, 1.0)
            
            if score >= min_score:
                # 提取摘要
                summary = ""
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('---') and not line.startswith('type:'):
                        summary = line[:200]
                        break
                
                results.append({
                    'file': str(md_file.relative_to(wiki_path)),
                    'title': frontmatter.get('title', md_file.stem),
                    'type': frontmatter.get('type', 'unknown'),
                    'score': score,
                    'summary': summary,
                    'tags': tags,
                })
        except Exception as e:
            continue
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:max_results]

def format_results(results, query):
    """格式化搜索结果"""
    if not results:
        print(f"🔍 未找到与 \"{query}\" 相关的内容")
        print("\n💡 提示:")
        print("  - 确保已导入资料到 raw/ 目录")
        print("  - 让 AI 处理资料并更新 wiki")
        print("  - 尝试不同的关键词")
        return
    
    print(f"🔍 搜索: \"{query}\"")
    print(f"📊 找到 {len(results)} 个结果:\n")
    
    for i, result in enumerate(results, 1):
        score_bar = "█" * int(result['score'] * 10) + "░" * (10 - int(result['score'] * 10))
        
        print(f"{i}. {result['title']}")
        print(f"   类型: {result['type']} | 分数: [{score_bar}] {result['score']:.2f}")
        print(f"   文件: {result['file']}")
        
        if result['tags']:
            tags_str = ", ".join(result['tags'][:5])
            print(f"   标签: {tags_str}")
        
        if result['summary']:
            print(f"   摘要: {result['summary'][:100]}...")
        
        print()

def main():
    parser = argparse.ArgumentParser(
        description='LLM Wiki 搜索工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/search.py "注意力机制"
  python scripts/search.py --query "Transformer" --max-results 5
  python scripts/search.py "深度学习" --min-score 0.3
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='搜索查询'
    )
    
    parser.add_argument(
        '--query', '-q',
        dest='query_flag',
        help='搜索查询（也可以直接作为位置参数）'
    )
    
    parser.add_argument(
        '--max-results', '-n',
        type=int,
        default=10,
        help='最大结果数 (默认: 10)'
    )
    
    parser.add_argument(
        '--min-score', '-s',
        type=float,
        default=0.3,
        help='最小分数 (默认: 0.3)'
    )
    
    parser.add_argument(
        '--wiki-path',
        default='wiki',
        help='Wiki 目录路径 (默认: wiki)'
    )
    
    args = parser.parse_args()
    
    query = args.query or args.query_flag
    
    if not query:
        parser.print_help()
        print("\n💡 提示: 输入你的问题进行搜索")
        return
    
    results = search_wiki(
        query,
        wiki_path=args.wiki_path,
        max_results=args.max_results,
        min_score=args.min_score,
    )
    
    format_results(results, query)

if __name__ == '__main__':
    main()
