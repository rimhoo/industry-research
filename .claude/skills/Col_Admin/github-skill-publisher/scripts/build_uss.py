#!/usr/bin/env python3
"""
USS Build Script — 将 SKILL.md 转换为多平台兼容包 (Universal Skill Standard v1.0)
用法: python3 scripts/build_uss.py <skill-dir>

生成文件:
  - prompt.md           纯 Markdown 注入版（无 frontmatter，任何平台可用）
  - prompt_compact.md   压缩版（≤800 token）
  - manifest.json       通用元数据 + 平台路由表
  - openai_tool.json    OpenAI function calling schema
"""

import os, json, re, sys
from pathlib import Path


def strip_frontmatter(text):
    """移除 YAML frontmatter，返回纯正文"""
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            return text[end+4:].lstrip('\n')
    return text


def extract_frontmatter(text):
    """提取 YAML frontmatter 中的 name 和 description"""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    result = {}
    name_m = re.search(r'^name:\s*(.+)$', fm_text, re.MULTILINE)
    if name_m:
        result['name'] = name_m.group(1).strip()
    desc_m = re.search(r'description:\s*[>|]?\s*\n((?:  .+\n?)+)', fm_text)
    if desc_m:
        desc = re.sub(r'  ', '', desc_m.group(1)).replace('\n', ' ').strip()
        result['description'] = desc
    else:
        desc_m = re.search(r'^description:\s*(.+)$', fm_text, re.MULTILINE)
        if desc_m:
            result['description'] = desc_m.group(1).strip()
    return result, text[end+4:].lstrip('\n')


def estimate_tokens(text):
    """粗略估算 token 数（中文≈1.5字/token，英文≈4字符/token）"""
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    others = len(text) - chinese
    return int(chinese / 1.5 + others / 4)


def make_compact(content, max_tokens=800):
    """生成压缩版：保留标题和核心框架，删减细节"""
    lines = content.split('\n')
    result = []
    token_count = 0

    for line in lines:
        if re.match(r'^#{1,3} ', line):
            result.append(line)
            token_count += estimate_tokens(line)
        elif line.startswith('|'):
            if '---' not in line:
                result.append(line)
                token_count += estimate_tokens(line)
            continue
        elif line.startswith('**') or ('**' in line and len(line) < 100):
            result.append(line)
            token_count += estimate_tokens(line)
        elif re.match(r'^(Step|步骤|\d+\.|[-•])\s', line.strip()):
            result.append(line)
            token_count += estimate_tokens(line)
        elif line.startswith('```') or (result and result[-1].startswith('```')):
            result.append(line)
            token_count += estimate_tokens(line)
        elif line.startswith('>'):
            result.append(line)
            token_count += estimate_tokens(line)
        elif line.strip() == '':
            result.append('')

        if token_count >= max_tokens:
            break

    result.append('\n---\n> 完整框架见 prompt.md')
    return '\n'.join(result)


def make_openai_tool(skill_id, name, description, content):
    """生成 OpenAI function calling schema"""
    return {
        "type": "function",
        "function": {
            "name": skill_id.replace('-', '_'),
            "description": description[:200] if description else name,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户的问题或分析请求"
                    },
                    "context": {
                        "type": "string",
                        "description": "背景信息（可选）"
                    }
                },
                "required": ["query"]
            }
        }
    }


def build_uss(skill_dir):
    """
    对 skill 目录执行 USS 构建，生成跨平台兼容文件。

    Args:
        skill_dir: str 或 Path，指向包含 SKILL.md 的 skill 目录

    Returns:
        dict: {
            "generated": [文件名列表],
            "tokens_full": int,
            "tokens_compact": int,
            "manifest": dict  # manifest.json 内容
        }
    """
    skill_path = Path(skill_dir)
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        print(f"  ERROR: {skill_md} not found")
        return None

    content = skill_md.read_text(encoding='utf-8')
    fm, body = extract_frontmatter(content)

    skill_id = fm.get('name', skill_path.name)
    description = fm.get('description', '')

    print(f"  Building USS: {skill_id}")
    generated = []

    # 1. prompt.md — 纯注入版
    prompt_content = f"# {skill_id}\n\n> 触发场景：{description[:100]}\n\n{body}"
    (skill_path / 'prompt.md').write_text(prompt_content, encoding='utf-8')
    full_tokens = estimate_tokens(prompt_content)
    generated.append('prompt.md')
    print(f"    prompt.md: ~{full_tokens} tokens")

    # 2. prompt_compact.md — 压缩版
    compact = make_compact(body, max_tokens=800)
    compact_content = f"# {skill_id} [精简版]\n\n{compact}"
    (skill_path / 'prompt_compact.md').write_text(compact_content, encoding='utf-8')
    compact_tokens = estimate_tokens(compact_content)
    generated.append('prompt_compact.md')
    print(f"    prompt_compact.md: ~{compact_tokens} tokens")

    # 3. openai_tool.json
    tool = make_openai_tool(skill_id, skill_id, description, body)
    tool['function']['system_prompt'] = prompt_content[:2000]
    (skill_path / 'openai_tool.json').write_text(
        json.dumps(tool, ensure_ascii=False, indent=2), encoding='utf-8')
    generated.append('openai_tool.json')
    print(f"    openai_tool.json: done")

    # 4. manifest.json
    manifest = {
        "skill_id": skill_path.name,
        "name": skill_id,
        "version": "1.0.0",
        "description": description,
        "triggers": [w for w in re.findall(r'[\u4e00-\u9fff]{2,6}', description)[:10]],
        "tags": [],
        "author": "",
        "created": "2026-06-12",
        "language": "zh-CN",
        "standard": "USS-1.0",
        "platforms": {
            "claude_code": "SKILL.md",
            "system_prompt": "prompt.md",
            "system_prompt_compact": "prompt_compact.md",
            "openai_tool": "openai_tool.json",
            "coze": "prompt.md",
            "openclaw": "prompt.md",
            "hermes": "prompt.md",
            "dify": "prompt.md",
            "langchain": "prompt.md"
        },
        "token_estimates": {
            "full": full_tokens,
            "compact": compact_tokens
        }
    }
    (skill_path / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    generated.append('manifest.json')
    print(f"    manifest.json: done")

    return {
        "generated": generated,
        "tokens_full": full_tokens,
        "tokens_compact": compact_tokens,
        "manifest": manifest
    }


def validate_uss_compliance(skill_path: Path) -> list[str]:
    """
    检查 skill 目录是否符合 USS 标准。
    返回缺失文件列表（空列表表示完全合规）。
    """
    required = ["SKILL.md", "prompt.md", "prompt_compact.md", "manifest.json"]
    missing = []
    for f in required:
        if not (skill_path / f).exists():
            missing.append(f)
    return missing


if __name__ == '__main__':
    if len(sys.argv) > 1:
        result = build_uss(sys.argv[1])
        if result:
            print(f"\nUSS build complete: {', '.join(result['generated'])}")
    else:
        print("用法: python scripts/build_uss.py <skill-dir>")
