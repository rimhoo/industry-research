#!/usr/bin/env python3
"""
validate_publish.py — 发布前验证 skill 结构

用法:
    python scripts/validate_publish.py <skill_path>
"""

import sys
from pathlib import Path

# 兼容直接运行和被 import
sys.path.insert(0, str(Path(__file__).parent))
from parse_skill_meta import parse_skill_meta, SkillMeta


def validate_skill(skill_path: Path) -> tuple[bool, SkillMeta | None, list[str]]:
    """
    验证 skill 目录是否满足发布要求。

    Returns:
        (valid: bool, meta: SkillMeta | None, errors: list[str])
    """
    skill_path = Path(skill_path)
    errors = []

    # 目录存在
    if not skill_path.exists():
        return False, None, [f"目录不存在：{skill_path}"]
    if not skill_path.is_dir():
        return False, None, [f"路径不是目录：{skill_path}"]

    # SKILL.md 存在
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, None, ["SKILL.md 不存在"]

    # 解析 meta
    try:
        meta = parse_skill_meta(skill_path)
    except Exception as e:
        return False, None, [f"SKILL.md 解析失败：{e}"]

    # name 必须存在
    if not meta.name:
        errors.append("SKILL.md frontmatter 缺少 'name' 字段")

    # description 必须存在且足够长
    if not meta.description:
        errors.append("SKILL.md frontmatter 缺少 'description' 字段")
    elif len(meta.description) < 20:
        errors.append(f"description 太短（{len(meta.description)} 字），建议至少 20 字以上")

    # 正文不能为空
    if len(meta.raw_body.strip()) < 50:
        errors.append("SKILL.md 正文内容太少，建议补充使用说明")

    # 文件状态报告（非错误，仅提示）
    missing = []
    for fname in ["README.md", "LICENSE", ".gitignore", "CHANGELOG.md"]:
        if not (skill_path / fname).exists():
            missing.append(fname)

    # USS 标准检查
    uss_files = ["prompt.md", "prompt_compact.md", "manifest.json", "openai_tool.json"]
    uss_missing = [f for f in uss_files if not (skill_path / f).exists()]

    valid = len(errors) == 0
    return valid, meta, errors


def main():
    if len(sys.argv) < 2:
        print("用法：python scripts/validate_publish.py <skill_path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    print(f"\n🔍 验证 skill：{skill_path}\n")

    valid, meta, errors = validate_skill(skill_path)

    if errors:
        print("❌ 验证失败：")
        for e in errors:
            print(f"   • {e}")
        sys.exit(1)

    print(f"✅ 验证通过")
    print(f"   name:        {meta.name}")
    print(f"   description: {meta.description[:80]}…" if len(meta.description) > 80 else f"   description: {meta.description}")
    print(f"   H2 章节:     {len(meta.h2_sections)} 个")
    print(f"   代码示例:    {len(meta.code_examples)} 个")

    # 文件状态
    print("\n📁 仓库文件状态：")
    for fname in ["README.md", "LICENSE", ".gitignore", "CHANGELOG.md"]:
        exists = (skill_path / fname).exists()
        icon = "✅" if exists else "⚠️  缺失（发布时将自动生成）"
        print(f"   {icon}  {fname}")

    print("\n📁 USS 全平台文件状态：")
    uss_files = ["prompt.md", "prompt_compact.md", "manifest.json", "openai_tool.json"]
    for fname in uss_files:
        exists = (skill_path / fname).exists()
        icon = "✅" if exists else "⚠️  缺失（发布时将自动生成）"
        print(f"   {icon}  {fname}")

    print()


if __name__ == "__main__":
    main()
