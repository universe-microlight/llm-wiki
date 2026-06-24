#!/usr/bin/env python3
"""
LLM Wiki 健康检查工具

用法:
    python scripts/lint.py
    python scripts/lint.py --fix
    python scripts/lint.py --verbose
"""

import os
import sys
import argparse
import yaml
import re
from pathlib import Path
from datetime import datetime, timedelta

def load_frontmatter(file_path):
    """加载文件的 frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                frontmatter_yaml = content[3:end].strip()
                frontmatter = yaml.safe_load(frontmatter_yaml)
                return frontmatter, content
    except Exception:
        pass
    return {}, ""

def find_all_references(content):
    """找到所有 [[reference]] 引用"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)

def find_all_pages(wiki_path):
    """找到所有页面"""
    pages = {}
    for md_file in Path(wiki_path).rglob('*.md'):
        # 生成 slug
        slug = md_file.stem.lower().replace(' ', '-').replace('_', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        pages[slug] = md_file
    return pages

def check_dead_links(wiki_path, verbose=False):
    """检查死链"""
    issues = []
    all_pages = find_all_pages(wiki_path)
    
    for md_file in Path(wiki_path).rglob('*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            references = find_all_references(content)
            
            for ref in references:
                ref_slug = ref.lower().replace(' ', '-').replace('_', '-')
                ref_slug = ''.join(c for c in ref_slug if c.isalnum() or c == '-')
                
                if ref_slug not in all_pages:
                    issues.append({
                        'type': 'dead_link',
                        'file': str(md_file.relative_to(wiki_path)),
                        'reference': ref,
                        'message': f"死链: [[{ref}] 指向不存在的页面"
                    })
        except Exception:
            continue
    
    return issues

def check_orphan_pages(wiki_path, verbose=False):
    """检查孤立页面"""
    issues = []
    all_pages = find_all_pages(wiki_path)
    referenced_pages = set()
    
    # 收集所有被引用的页面
    for md_file in Path(wiki_path).rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            references = find_all_references(content)
            for ref in references:
                ref_slug = ref.lower().replace(' ', '-').replace('_', '-')
                ref_slug = ''.join(c for c in ref_slug if c.isalnum() or c == '-')
                referenced_pages.add(ref_slug)
        except Exception:
            continue
    
    # 检查孤立页面
    for slug, file_path in all_pages.items():
        if slug not in referenced_pages and slug not in ['index', 'log']:
            issues.append({
                'type': 'orphan_page',
                'file': str(file_path.relative_to(wiki_path)),
                'message': f"孤立页面: 未被任何页面引用"
            })
    
    return issues

def check_stale_pages(wiki_path, threshold_days=180, verbose=False):
    """检查过期页面"""
    issues = []
    threshold_date = datetime.now() - timedelta(days=threshold_days)
    
    for md_file in Path(wiki_path).rglob('*.md'):
        try:
            frontmatter, content = load_frontmatter(md_file)
            
            timestamp = frontmatter.get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    try:
                        update_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if update_date.replace(tzinfo=None) < threshold_date:
                            issues.append({
                                'type': 'stale_page',
                                'file': str(md_file.relative_to(wiki_path)),
                                'message': f"过期页面: 超过 {threshold_days} 天未更新",
                                'last_updated': timestamp
                            })
                    except ValueError:
                        pass
        except Exception:
            continue
    
    return issues

def check_frontmatter(wiki_path, verbose=False):
    """检查 frontmatter 格式"""
    issues = []
    required_fields = ['type', 'title', 'timestamp']
    
    for md_file in Path(wiki_path).rglob('*.md'):
        try:
            frontmatter, content = load_frontmatter(md_file)
            
            if not frontmatter:
                issues.append({
                    'type': 'missing_frontmatter',
                    'file': str(md_file.relative_to(wiki_path)),
                    'message': "缺少 frontmatter"
                })
                continue
            
            for field in required_fields:
                if field not in frontmatter:
                    issues.append({
                        'type': 'missing_field',
                        'file': str(md_file.relative_to(wiki_path)),
                        'field': field,
                        'message': f"缺少必需字段: {field}"
                    })
        except Exception:
            continue
    
    return issues

def check_content_length(wiki_path, min_length=100, verbose=False):
    """检查内容长度"""
    issues = []
    
    for md_file in Path(wiki_path).rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 去除 frontmatter
            if content.startswith('---'):
                end = content.find('---', 3)
                if end != -1:
                    content = content[end+3:].strip()
            
            if len(content) < min_length:
                issues.append({
                    'type': 'short_content',
                    'file': str(md_file.relative_to(wiki_path)),
                    'length': len(content),
                    'min_length': min_length,
                    'message': f"内容过短: {len(content)} < {min_length} 字符"
                })
        except Exception:
            continue
    
    return issues

def run_lint(wiki_path='wiki', fix=False, verbose=False, threshold_days=180):
    """运行健康检查"""
    print("🏥 LLM Wiki 健康检查\n")
    
    all_issues = []
    
    # 1. 死链检查
    print("🔗 检查死链...")
    dead_links = check_dead_links(wiki_path, verbose)
    all_issues.extend(dead_links)
    if dead_links:
        print(f"   ❌ 发现 {len(dead_links)} 个死链")
    else:
        print("   ✅ 无死链")
    
    # 2. 孤立页面检查
    print("\n📄 检查孤立页面...")
    orphans = check_orphan_pages(wiki_path, verbose)
    all_issues.extend(orphans)
    if orphans:
        print(f"   ⚠️  发现 {len(orphans)} 个孤立页面")
    else:
        print("   ✅ 无孤立页面")
    
    # 3. 过期页面检查
    print(f"\n📅 检查过期页面 (>{threshold_days}天)...")
    stale = check_stale_pages(wiki_path, threshold_days, verbose)
    all_issues.extend(stale)
    if stale:
        print(f"   ⚠️  发现 {len(stale)} 个过期页面")
    else:
        print("   ✅ 无过期页面")
    
    # 4. Frontmatter 检查
    print("\n📋 检查 frontmatter...")
    frontmatter_issues = check_frontmatter(wiki_path, verbose)
    all_issues.extend(frontmatter_issues)
    if frontmatter_issues:
        print(f"   ❌ 发现 {len(frontmatter_issues)} 个格式问题")
    else:
        print("   ✅ frontmatter 格式正确")
    
    # 5. 内容长度检查
    print("\n📏 检查内容长度...")
    short_content = check_content_length(wiki_path, verbose=verbose)
    all_issues.extend(short_content)
    if short_content:
        print(f"   ⚠️  发现 {len(short_content)} 个过短页面")
    else:
        print("   ✅ 内容长度正常")
    
    # 汇总
    print("\n" + "="*50)
    print(f"📊 检查完成: 共发现 {len(all_issues)} 个问题")
    
    if all_issues:
        print("\n问题列表:")
        for i, issue in enumerate(all_issues, 1):
            print(f"\n{i}. [{issue['type']}] {issue['file']}")
            print(f"   {issue['message']}")
            if verbose and 'reference' in issue:
                print(f"   引用: [[{issue['reference']}]")
        
        print("\n💡 建议:")
        print("  - 让 AI 修复死链和孤立页面")
        print("  - 更新过期页面的内容")
        print("  - 补充过短页面的内容")
        
        return False
    else:
        print("\n🎉 知识库状态良好！")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='LLM Wiki 健康检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/lint.py
  python scripts/lint.py --fix
  python scripts/lint.py --verbose --threshold-days 90
        """
    )
    
    parser.add_argument(
        '--fix',
        action='store_true',
        help='自动修复问题（开发中）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息'
    )
    
    parser.add_argument(
        '--wiki-path',
        default='wiki',
        help='Wiki 目录路径 (默认: wiki)'
    )
    
    parser.add_argument(
        '--threshold-days',
        type=int,
        default=180,
        help='过期天数阈值 (默认: 180)'
    )
    
    args = parser.parse_args()
    
    if args.fix:
        print("⚠️  自动修复功能开发中...")
        print("💡 当前版本只检查问题，不自动修复")
        print()
    
    success = run_lint(
        wiki_path=args.wiki_path,
        fix=args.fix,
        verbose=args.verbose,
        threshold_days=args.threshold_days,
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
