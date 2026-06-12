#!/usr/bin/env python3
"""
publish.py — GitHub Skill Publisher 主入口

用法:
    python scripts/publish.py <skill_path> [options]

示例:
    python scripts/publish.py ./my-skill
    python scripts/publish.py ./my-skill --author "Zhang San" --license mit --private
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

# 确保同目录下的模块可以被导入
sys.path.insert(0, str(Path(__file__).parent))

from validate_publish import validate_skill, SkillMeta
from gen_readme import generate_readme
from parse_skill_meta import parse_skill_meta
from build_uss import build_uss


# ─────────────────────────────────────────────
# ANSI 颜色（Windows 需 ENABLE_VIRTUAL_TERMINAL_PROCESSING）
# ─────────────────────────────────────────────
def _color(text: str, code: str) -> str:
    if os.name == "nt":
        return text  # Windows 终端直接返回纯文本
    return f"\033[{code}m{text}\033[0m"

GREEN  = lambda t: _color(t, "32")
YELLOW = lambda t: _color(t, "33")
RED    = lambda t: _color(t, "31")
CYAN   = lambda t: _color(t, "36")
BOLD   = lambda t: _color(t, "1")


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def run(cmd: list[str], cwd: Path = None, capture: bool = False) -> subprocess.CompletedProcess:
    """运行命令，失败时抛出异常。"""
    result = subprocess.run(
        cmd, cwd=cwd,
        capture_output=capture, text=True
    )
    return result


def check_gh_cli() -> bool:
    """检查 gh CLI 是否可用且已登录。"""
    try:
        r = run(["gh", "auth", "status"], capture=True)
        return r.returncode == 0
    except FileNotFoundError:
        return False


# ─────────────────────────────────────────────
# Token 优先级链(2026-06-11 增补)
# ─────────────────────────────────────────────
def get_github_token() -> str | None:
    """
    按优先级链读取 GitHub Token(NEVER 硬编码):
      1. GH_TOKEN 环境变量
      2. GITHUB_TOKEN 环境变量
      3. ~/.netrc 中 machine github.com 的 password 字段
      4. gh CLI credential helper(gh auth token)
    返回 None 表示未找到。
    """
    # 1 & 2: 环境变量
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token.strip()

    # 3: ~/.netrc
    netrc_path = Path.home() / "_netrc"
    if not netrc_path.exists():
        netrc_path = Path.home() / ".netrc"
    if netrc_path.exists():
        try:
            content = netrc_path.read_text(encoding="utf-8")
            # 解析 machine github.com 块中的 password 字段
            m = re.search(
                r"machine\s+github\.com[^]*?password\s+(\S+)",
                content,
                re.IGNORECASE,
            )
            if m:
                return m.group(1).strip()
        except Exception:
            pass

    # 4: gh CLI credential helper
    try:
        r = run(["gh", "auth", "token"], capture=True)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except FileNotFoundError:
        pass

    return None


def get_auth_status() -> dict:
    """
    返回当前可用认证方式的诊断信息(用于报告)。
    不暴露 token 本身,只暴露来源标签。
    """
    sources = []
    if os.environ.get("GH_TOKEN"):
        sources.append("GH_TOKEN env")
    if os.environ.get("GITHUB_TOKEN"):
        sources.append("GITHUB_TOKEN env")
    netrc_path = Path.home() / "_netrc"
    if not netrc_path.exists():
        netrc_path = Path.home() / ".netrc"
    if netrc_path.exists():
        try:
            content = netrc_path.read_text(encoding="utf-8")
            if re.search(r"machine\s+github\.com", content, re.IGNORECASE):
                sources.append("~/.netrc")
        except Exception:
            pass
    if check_gh_cli():
        sources.append("gh CLI")
    return {"sources": sources, "has_auth": bool(sources)}


def has_github_auth() -> bool:
    """检查是否有任何可用 GitHub 认证(token 或 gh CLI)。"""
    return get_github_token() is not None or check_gh_cli()


def get_git_username(skill_path: Path) -> str:
    """从 git config 获取用户名，用于 GitHub URL 推断。"""
    try:
        r = run(["git", "config", "user.name"], cwd=skill_path, capture=True)
        return r.stdout.strip() or "your-username"
    except Exception:
        return "your-username"


def git_is_initialized(path: Path) -> bool:
    r = run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path, capture=True)
    return r.returncode == 0


def git_has_remote(path: Path) -> bool:
    r = run(["git", "remote"], cwd=path, capture=True)
    return bool(r.stdout.strip())


# ─────────────────────────────────────────────
# 文件生成
# ─────────────────────────────────────────────
ASSETS_DIR = Path(__file__).parent.parent / "assets"

def generate_license(skill_path: Path, author: str, license_type: str = "mit") -> Path:
    """生成 LICENSE 文件。"""
    dest = skill_path / "LICENSE"
    if dest.exists():
        print(f"  {YELLOW('⚠')}  LICENSE 已存在，跳过")
        return dest

    template_path = ASSETS_DIR / "license_templates" / f"{license_type.lower()}.txt"
    if template_path.exists():
        content = template_path.read_text(encoding="utf-8")
    else:
        # 内置 MIT 模板（兜底）
        content = _mit_template()

    content = content.replace("{year}", str(date.today().year))
    content = content.replace("{author}", author or "Contributors")
    dest.write_text(content, encoding="utf-8")
    print(f"  {GREEN('✅')} LICENSE ({license_type.upper()}) 已生成")
    return dest


def generate_gitignore(skill_path: Path) -> Path:
    dest = skill_path / ".gitignore"
    if dest.exists():
        print(f"  {YELLOW('⚠')}  .gitignore 已存在，跳过")
        return dest

    template_path = ASSETS_DIR / "gitignore_template.txt"
    if template_path.exists():
        shutil.copy(template_path, dest)
    else:
        dest.write_text(_default_gitignore(), encoding="utf-8")
    print(f"  {GREEN('✅')} .gitignore 已生成")
    return dest


def generate_changelog(skill_path: Path, meta: SkillMeta) -> Path:
    dest = skill_path / "CHANGELOG.md"
    if dest.exists():
        print(f"  {YELLOW('⚠')}  CHANGELOG.md 已存在，跳过")
        return dest

    today = date.today().isoformat()
    desc_short = (meta.description[:120] + "…") if len(meta.description) > 120 else meta.description

    content = f"""# Changelog

所有重要更改都记录在此文件中。  
All notable changes to this project are documented here.

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，  
版本遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [1.0.0] - {today}

### Added / 新增

- 初始发布 — {meta.name}
- {desc_short}

"""
    dest.write_text(content, encoding="utf-8")
    print(f"  {GREEN('✅')} CHANGELOG.md 已生成")
    return dest


# ─────────────────────────────────────────────
# Git 操作
# ─────────────────────────────────────────────
def git_setup(skill_path: Path, meta: SkillMeta, repo_name: str):
    """初始化 git，添加所有文件，创建首次提交。"""
    initialized = git_is_initialized(skill_path)

    if not initialized:
        run(["git", "init", "-b", "main"], cwd=skill_path)
        print(f"  {GREEN('✅')} git init（分支：main）")
    else:
        print(f"  {CYAN('ℹ')}  已有 git 仓库")

    run(["git", "add", "-A"], cwd=skill_path)
    desc_oneline = meta.description[:72].replace('"', "'")
    commit_msg = (
        f"feat: publish {meta.name} v1.0.0\n\n"
        f"- Auto-generated bilingual README\n"
        f"- Standard repo structure completed\n"
        f"- {desc_oneline}"
    )
    result = run(["git", "commit", "-m", commit_msg], cwd=skill_path, capture=True)
    if result.returncode == 0:
        print(f"  {GREEN('✅')} git commit 完成")
    else:
        # 可能没有新变更
        print(f"  {CYAN('ℹ')}  {result.stdout.strip() or result.stderr.strip()}")


def push_with_gh(skill_path: Path, repo_name: str, meta: SkillMeta, private: bool) -> bool:
    """使用 gh CLI 创建仓库并推送。"""
    visibility = "--private" if private else "--public"
    desc = meta.description[:255].replace('"', "'")

    result = run(
        ["gh", "repo", "create", repo_name,
         visibility,
         "--description", desc,
         "--push", "--source", "."],
        cwd=skill_path, capture=True
    )
    if result.returncode == 0:
        url = result.stdout.strip().split("\n")[-1].strip()
        return url or f"https://github.com/{repo_name}"
    else:
        print(f"  {RED('✗')}  gh repo create 失败：{result.stderr.strip()}")
        return None


def push_manual_guide(skill_path: Path, repo_name: str, meta: SkillMeta, private: bool):
    """gh CLI 不可用时，输出手动操作指引。"""
    username = get_git_username(skill_path)
    visibility = "Private" if private else "Public"
    desc = meta.description[:255].replace('"', "'")

    print(f"""
{BOLD('── 手动发布步骤 ──────────────────────────────')}

{CYAN('1.')} 在 GitHub 创建仓库（勾选 {visibility}）：
   https://github.com/new

   名称：{BOLD(repo_name)}
   描述：{desc}

{CYAN('2.')} 在终端执行：

   git remote add origin https://github.com/{username}/{repo_name}.git
   git push -u origin main

{CYAN('3.')} 完成后仓库地址：
   https://github.com/{username}/{repo_name}
{BOLD('──────────────────────────────────────────────')}
""")


# ─────────────────────────────────────────────
# 发布报告
# ─────────────────────────────────────────────
def print_report(skill_path: Path, meta: SkillMeta, repo_url: str, generated: list[str]):
    file_count = sum(1 for _ in skill_path.rglob("*") if _.is_file()
                     and ".git" not in _.parts)
    gen_lines = "\n".join(f"  ║  ✅ {f:<20}" for f in generated)
    report = f"""
{CYAN('╔══════════════════════════════════════════════╗')}
{CYAN('║')}  {GREEN('🚀 Skill 发布成功')}                             {CYAN('║')}
{CYAN('╠══════════════════════════════════════════════╣')}
{CYAN('║')}  仓库    {BOLD(repo_url or '（见上方手动步骤）'):<35}{CYAN('║')}
{CYAN('║')}  Skill   {meta.name:<35}{CYAN('║')}
{CYAN('║')}  文件    {str(file_count) + ' 个已提交':<35}{CYAN('║')}
{CYAN('╠══════════════════════════════════════════════╣')}
{CYAN('║')}  本次生成文件                                {CYAN('║')}
{gen_lines}
{CYAN('╚══════════════════════════════════════════════╝')}
"""
    print(report)


# ─────────────────────────────────────────────
# Frontmatter 写回(2026-06-11 增补,Step 8 实现)
# ─────────────────────────────────────────────
def update_skill_frontmatter(
    skill_path: Path,
    repo_url: str,
    default_branch: str = "main",
) -> bool:
    """
    发布成功后,将仓库元数据写回 SKILL.md 的 YAML frontmatter。

    新增/更新字段:
      - repository:    仓库 URL
      - default_branch: 默认分支
      - published_at:  发布日期(ISO 8601)

    写回是幂等的:重复执行会覆盖更新,不破坏原有字段。
    返回 True/False 表示是否成功。
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"  {YELLOW('⚠')}  SKILL.md 不存在,跳过 frontmatter 写回")
        return False

    content = skill_md.read_text(encoding="utf-8")
    today = date.today().isoformat()

    # 解析已有 frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not fm_match:
        print(f"  {YELLOW('⚠')}  SKILL.md 无 YAML frontmatter,跳过写回")
        return False

    fm_body = fm_match.group(1)
    rest = fm_match.group(2)

    # 解析已有字段(简单 key: value,支持单行 / 折叠列表)
    new_lines = []
    fields = {
        "repository": f'"{repo_url}"' if repo_url else None,
        "default_branch": f'"{default_branch}"',
        "published_at": f'"{today}"',
    }
    existing_keys = set()

    for line in fm_body.split("\n"):
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:", line)
        if m:
            existing_keys.add(m.group(1))
        new_lines.append(line)

    # 在 frontmatter 末尾追加缺失字段(name → description → repository → default_branch → published_at)
    insert_order = ["repository", "default_branch", "published_at"]
    insert_lines = []
    for key in insert_order:
        if key not in existing_keys and fields[key] is not None:
            insert_lines.append(f"{key}: {fields[key]}")

    if insert_lines:
        new_fm = fm_body.rstrip() + "\n" + "\n".join(insert_lines) + "\n"
        new_content = f"---\n{new_fm}---\n{rest}"
        skill_md.write_text(new_content, encoding="utf-8")
        print(f"  {GREEN('✅')} SKILL.md frontmatter 已写回(repository/default_branch/published_at)")
        return True
    else:
        print(f"  {CYAN('ℹ')}  SKILL.md frontmatter 已包含 repository 字段,跳过")
        return False


def detect_default_branch(skill_path: Path) -> str:
    """检测 skill 目录所在 git 仓库的默认分支。"""
    r = run(
        ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
        cwd=skill_path,
        capture=True,
    )
    if r.returncode == 0 and r.stdout.strip():
        # 输出形如 "origin/main",取后半段
        return r.stdout.strip().split("/")[-1]
    # 兜底:看本地分支列表
    r2 = run(["git", "branch", "--list"], cwd=skill_path, capture=True)
    if r2.returncode == 0:
        branches = [b.strip().lstrip("* ") for b in r2.stdout.splitlines() if b.strip()]
        for preferred in ("main", "master"):
            if preferred in branches:
                return preferred
        if branches:
            return branches[0]
    return "main"


def commit_frontmatter_update(skill_path: Path) -> bool:
    """SKILL.md frontmatter 写回后,自动 commit + push(若有远端)。"""
    if not git_is_initialized(skill_path):
        return False

    r = run(["git", "add", "SKILL.md"], cwd=skill_path, capture=True)
    if r.returncode != 0:
        return False

    # 检查是否有实际变更
    diff = run(["git", "diff", "--cached", "--quiet"], cwd=skill_path, capture=True)
    if diff.returncode == 0:
        # 无变更
        return False

    msg = "chore(skill): write repository/default_branch/published_at to frontmatter"
    run(["git", "commit", "-m", msg], cwd=skill_path, capture=True)

    # 若有远端,推送
    if git_has_remote(skill_path):
        branch = detect_default_branch(skill_path)
        push = run(
            ["git", "push", "origin", branch],
            cwd=skill_path,
            capture=True,
        )
        if push.returncode == 0:
            print(f"  {GREEN('✅')} 同步提交已推送到 origin/{branch}")
            return True
        else:
            print(f"  {YELLOW('⚠')}  本地已 commit,但 push 失败:{push.stderr.strip()}")
            return False
    return True


def install_post_commit_hook(skill_path: Path) -> bool:
    """
    安装 git post-commit hook,每次 commit 后自动 push。
    不依赖 Claude Code,用 git 原生机制,可靠且跨版本。
    """
    hooks_dir = skill_path / ".git" / "hooks"
    if not hooks_dir.exists():
        print(f"  {YELLOW('⚠')}  .git/hooks 不存在,跳过 post-commit hook 安装")
        return False

    hook_path = hooks_dir / "post-commit"
    content = """#!/bin/bash
# post-commit hook — 每次 git commit 后自动 push 到 origin
# 由 github-skill-publisher 自动安装
set -e
branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "master")
if git remote | grep -q origin; then
    git push origin "$branch" 2>/dev/null || true
fi
"""
    hook_path.write_text(content, encoding="utf-8")
    # 设置可执行权限(Windows 跳过)
    try:
        hook_path.chmod(0o755)
    except Exception:
        pass
    print(f"  {GREEN('✅')} git post-commit hook 已安装(commit 即 push)")
    return True


# ─────────────────────────────────────────────
# 内置模板（兜底，不依赖 assets 文件）
# ─────────────────────────────────────────────
def _mit_template() -> str:
    return """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def _default_gitignore() -> str:
    return """# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
.env
*.egg-info/
dist/
build/

# Node
node_modules/
.npm
*.log

# macOS
.DS_Store
.AppleDouble

# Windows
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Skill packaging artifacts
*.skill
evals/
"""


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="将 Claude skill 发布到 GitHub"
    )
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("--repo-name", help="GitHub 仓库名（默认用 skill name）")
    parser.add_argument("--author", default="", help="LICENSE 署名")
    parser.add_argument("--license", default="mit", choices=["mit", "apache", "gpl"],
                        help="开源协议（默认 mit）")
    parser.add_argument("--lang", default="zh-en", choices=["zh-en", "en-zh", "zh", "en"],
                        help="README 语言顺序（默认 zh-en）")
    parser.add_argument("--private", action="store_true", help="创建私有仓库")
    parser.add_argument("--no-push", action="store_true", help="只生成文件，不推送")
    parser.add_argument("--force-readme", action="store_true", help="覆盖已有 README.md")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()

    print(f"\n{BOLD('── GitHub Skill Publisher ────────────────────')}")
    print(f"  Skill 路径:{skill_path}\n")

    # Step 0: 认证诊断(2026-06-11 增补)
    print(BOLD("▶ Step 0  认证检查"))
    auth = get_auth_status()
    if auth["has_auth"]:
        for src in auth["sources"]:
            print(f"  {GREEN('✅')} {src}")
    else:
        print(f"  {RED('✗')}  未找到任何 GitHub 认证源")
        print(f"  {YELLOW('ℹ')}  请按以下任一方式配置:")
        print(f"       1. 设置环境变量:export GH_TOKEN=ghp_xxx...")
        print(f"       2. 配置 ~/.netrc:https://github.com/settings/tokens")
        print(f"       3. 运行:gh auth login")
        sys.exit(1)
    print()

    # Step 1: 验证
    print(BOLD("▶ Step 1  验证 SKILL.md"))
    valid, meta, errors = validate_skill(skill_path)
    if not valid:
        for e in errors:
            print(f"  {RED('✗')}  {e}")
        sys.exit(1)
    print(f"  {GREEN('✅')} name: {meta.name}")
    print(f"  {GREEN('✅')} description: {meta.description[:60]}…\n")

    # Step 1.5: USS 全平台构建（Universal Skill Standard）
    print(BOLD("▶ Step 1.5 USS 全平台兼容打包"))
    uss_result = build_uss(skill_path)
    if uss_result is None:
        print(f"  {RED('✗')}  USS 构建失败，请检查 SKILL.md 格式")
        sys.exit(1)
    uss_generated = uss_result["generated"]
    print(f"  {GREEN('✅')} USS 标准文件: {', '.join(uss_generated)}")
    print(f"  {GREEN('✅')} token 估算: full ~{uss_result['tokens_full']}, compact ~{uss_result['tokens_compact']}")
    print()

    repo_name = args.repo_name or meta.name
    generated = list(uss_generated)  # 包含 prompt.md, prompt_compact.md, manifest.json, openai_tool.json

    # Step 2: 生成缺失文件
    print(BOLD("▶ Step 2  补齐仓库文件"))
    generate_license(skill_path, args.author, args.license)
    generated.append("LICENSE")
    generate_gitignore(skill_path)
    generated.append(".gitignore")
    generate_changelog(skill_path, meta)
    generated.append("CHANGELOG.md")
    print()

    # Step 3: 生成 README
    print(BOLD("▶ Step 3  生成双语 README.md"))
    readme_path = skill_path / "README.md"
    if readme_path.exists() and not args.force_readme:
        print(f"  {YELLOW('⚠')}  README.md 已存在,跳过(--force-readme 可覆盖)")
    else:
        if readme_path.exists():
            shutil.copy(readme_path, skill_path / "README.md.bak")
            print(f"  {CYAN('ℹ')}  已备份旧 README → README.md.bak")
        generate_readme(skill_path, meta, lang=args.lang)
        generated.append("README.md")
    print()

    if args.no_push:
        print(f"{GREEN('✅')} 文件生成完毕(--no-push 模式,未执行 git 操作)")
        return

    # Step 4: Git 操作
    print(BOLD("▶ Step 4  Git 提交"))
    git_setup(skill_path, meta, repo_name)
    print()

    # Step 5: 推送
    print(BOLD("▶ Step 5  推送到 GitHub"))
    repo_url = None
    if not git_has_remote(skill_path):
        if check_gh_cli():
            print(f"  {CYAN('ℹ')}  使用 gh CLI 创建仓库:{repo_name}")
            repo_url = push_with_gh(skill_path, repo_name, meta, args.private)
            if repo_url:
                print(f"  {GREEN('✅')} 推送成功:{repo_url}")
        else:
            print(f"  {YELLOW('⚠')}  未检测到 gh CLI,切换到手动模式")
            push_manual_guide(skill_path, repo_name, meta, args.private)
    else:
        branch = detect_default_branch(skill_path)
        run(["git", "push", "-u", "origin", branch], cwd=skill_path)
        # 推断 URL
        r = run(["git", "remote", "get-url", "origin"], cwd=skill_path, capture=True)
        if r.returncode == 0:
            remote = r.stdout.strip()
            if remote.startswith("git@"):
                # git@github.com:user/repo.git → https://github.com/user/repo
                m = re.match(r"git@github\.com:(.+?)(?:\.git)?$", remote)
                repo_url = f"https://github.com/{m.group(1)}" if m else remote
            elif remote.startswith("https://"):
                repo_url = re.sub(r"\.git$", "", remote)
        print(f"  {GREEN('✅')} git push 完成")

    # Step 6: 写回 SKILL.md frontmatter + 同步 commit(2026-06-11 增补)
    if repo_url:
        print(BOLD("▶ Step 6  写回 SKILL.md frontmatter(支持自动同步)"))
        branch = detect_default_branch(skill_path)
        if update_skill_frontmatter(skill_path, repo_url, branch):
            if commit_frontmatter_update(skill_path):
                print(f"  {GREEN('✅')} 自动同步链路已建立,后续本地修改可一键 push")
        print()

    # Step 6.5: 安装 git post-commit hook(自动 push,不依赖 Claude Code)
    print(BOLD("▶ Step 6.5  安装 git post-commit hook(自动 push)"))
    install_post_commit_hook(skill_path)
    print()

    # Step 7: 报告
    print_report(skill_path, meta, repo_url, generated)


if __name__ == "__main__":
    main()
