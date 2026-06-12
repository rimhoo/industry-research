---
name: github-skill-publisher
description: >
  Publish a Claude skill to GitHub with auto-generated bilingual (Chinese/English) documentation.
  Use this skill whenever the user wants to share, publish, upload, or release a skill to GitHub —
  whether created in Claude Code, Codex, or written by hand. Triggers on: "publish skill to GitHub",
  "push skill to repo", "share my skill", "upload skill", "release skill", "把skill发布到GitHub",
  "发布技能", "分享skill到GitHub". Automatically completes missing repo files, writes a professional
  bilingual README (中文为主，英文同步), and handles git init → commit → push in one flow.
---

# GitHub Skill Publisher

将 Claude skill 发布到 GitHub 的完整自动化流程：扫描结构 → USS 全平台打包 → 补齐缺失文件 → 生成双语 README → 推送到 GitHub。

---

## 工作流总览

```
扫描 skill 目录
    ↓
验证 SKILL.md 合规性
    ↓
提取元数据（name / description / features）
    ↓
[新增] USS 全平台打包（生成跨平台兼容文件）
    ├── prompt.md            纯 Markdown 注入版（任何 AI 平台可用）
    ├── prompt_compact.md    压缩版（≤800 token）
    ├── manifest.json        通用元数据 + 平台路由表
    └── openai_tool.json     OpenAI function calling schema
    ↓
生成缺失文件（README / LICENSE / .gitignore / CHANGELOG）
    ↓
生成双语 README.md（中文主体 + English section）
    ↓
git init → add → commit
    ↓
GitHub 仓库创建（gh CLI）或输出手动指引
    ↓
git push + 输出发布报告
```

---

## Step 1 — 扫描与诊断

读取 skill 目录，判断每个文件的存在状态：

```python
# 执行方式：python scripts/validate_publish.py <skill_path>
```

**必须存在**
- `SKILL.md` — 含合法 YAML frontmatter（name + description）

**标准仓库文件（缺失则生成）**
- `README.md` — 双语说明文档（本 skill 核心产出）
- `LICENSE` — 默认 MIT，可通过参数覆盖
- `.gitignore` — Python / Node / macOS 标准忽略规则
- `CHANGELOG.md` — 语义化版本变更日志初始模板

**可选但推荐**
- `scripts/` — 可执行脚本目录
- `references/` — 参考文档
- `assets/` — 静态资源

诊断输出示例：
```
✅ SKILL.md          合法（name: my-skill, description: 87字）
⚠️  README.md        缺失 → 将生成
⚠️  LICENSE          缺失 → 将生成（MIT）
✅ .gitignore        已存在
⚠️  CHANGELOG.md     缺失 → 将生成
```

---

## Step 2 — 解析 SKILL.md 元数据

从 SKILL.md 提取所有可用于生成文档的信息：

| 字段 | 来源 | 用途 |
|------|------|------|
| `name` | frontmatter | 仓库名、README 标题 |
| `description` | frontmatter | README 简介、GitHub About |
| `compatibility` | frontmatter（可选）| 依赖说明 |
| H2/H3 标题 | 正文结构 | README 功能列表 |
| 代码块注释 | 正文 | 使用示例 |

解析脚本：`scripts/parse_skill_meta.py`

---

## Step 3 — USS 全平台兼容打包（Universal Skill Standard v1.0）

发布前自动调用 `scripts/build_uss.py`，为 skill 生成跨平台兼容文件。

**生成文件：**

| 文件 | 适用平台 | 说明 |
|------|---------|------|
| `prompt.md` | Coze/扣子、OpenClaw、Hermes、Dify、LangChain、ChatGPT | 纯 Markdown，无 frontmatter，直接粘贴到系统提示 |
| `prompt_compact.md` | 有 token 限制的平台 | ≤800 token 压缩版，保留核心框架 |
| `manifest.json` | 通用元数据 | 平台路由表 + token 估算 |
| `openai_tool.json` | OpenAI GPT/Codex | function calling schema |

**USS 标准要求：**
- `prompt.md` 第一行：`# {技能名称}` 标题
- 第二行：`> 一句话定位（触发条件）`
- 禁止：YAML frontmatter、HTML 标签、外部链接依赖
- 所有内容自包含（不依赖 references/ 文件）
- `prompt_compact.md` ≤800 token，结尾标注「完整版见 prompt.md」

执行：`python scripts/build_uss.py <skill_path>`

---

## Step 4 — 生成双语 README.md
# {skill-name}

> {一句话简介（中文）}  
> *{One-liner in English}*

[badges 行]

## 这是什么 / What is this

## 功能特性 / Features  

## 快速上手 / Quick Start

## 使用场景 / When to Use

## 文件结构 / File Structure

## 参数说明 / Parameters（如有脚本）

## 版本历史 / Changelog

## 许可证 / License
```

**生成规则**
- 中文段落在前，英文紧跟其后（同一 section 内）
- 中文用自然流畅的技术写作风格，不用机器翻译腔
- badges 自动按实际内容生成（license / platform / Claude version）
- 代码示例从 SKILL.md 正文中提取或根据 description 推断

执行：`python scripts/gen_readme.py <skill_path> [--lang zh-en|en-zh|zh|en]`

---

## Step 5 — 生成补充文件

### LICENSE（MIT）
```
MIT License

Copyright (c) {year} {author}

Permission is hereby granted...
```
`--license apache|mit|gpl` 可切换协议。

### CHANGELOG.md
```markdown
# Changelog

## [1.0.0] - {today}

### Added
- 初始发布 / Initial release
- {从 SKILL.md description 提取的核心功能}
```

### .gitignore
标准模板，覆盖 Python / Node / macOS / Windows 常见忽略项。
完整模板见 `assets/gitignore_template.txt`。

---

## Step 6 — Git 操作

```bash
# 执行：python scripts/publish.py <skill_path> [options]
```

**自动检测场景**

| 场景 | 处理方式 |
|------|---------|
| 全新目录，无 .git | `git init` → 首次提交 |
| 已有 .git，无 remote | 添加 remote → push |
| 已有 .git + remote | 检测冲突 → pull rebase → push |

**提交信息格式**
```
feat: publish {skill-name} v{version}

- Auto-generated bilingual README
- Standard repo structure completed
- {来自 SKILL.md description 的一行摘要}
```

---

## Step 7 — GitHub 仓库创建

**优先使用 `gh` CLI（推荐）**
```bash
# 检测是否安装
gh --version

# 创建仓库
gh repo create {skill-name} \
  --public \
  --description "{description}" \
  --push \
  --source .
```

**`gh` 不可用时** → 输出手动操作指引：
```
1. 在 GitHub 创建仓库：https://github.com/new
   名称：{skill-name}
   描述：{description}（已复制到剪贴板）
   
2. 执行：
   git remote add origin https://github.com/{username}/{skill-name}.git
   git push -u origin main
```

---

## Step 8 — 发布报告

成功后输出：
```
╔══════════════════════════════════════════╗
║  🚀 Skill 发布成功                        ║
╠══════════════════════════════════════════╣
║  仓库    github.com/user/skill-name       ║
║  分支    main                             ║
║  提交    a1b2c3d feat: publish v1.0.0     ║
║  文件    6 个文件已推送                    ║
╠══════════════════════════════════════════╣
║  生成文件                                 ║
║  ✅ README.md    双语，892 字              ║
║  ✅ LICENSE      MIT 2025                 ║
║  ✅ CHANGELOG.md v1.0.0 初始版本          ║
║  ✅ .gitignore   标准模板                 ║
╚══════════════════════════════════════════╝
```

---

## 命令行快速参考

```bash
# 最简用法（全自动）
python scripts/publish.py ./my-skill

# 完整参数
python scripts/publish.py ./my-skill \
  --repo-name my-custom-name \     # 覆盖仓库名（默认用 skill name）
  --author "Your Name" \           # LICENSE 署名
  --license mit \                  # mit | apache | gpl（默认 mit）
  --lang zh-en \                   # README 语言顺序（默认 zh-en）
  --private \                      # 创建私有仓库
  --no-push \                      # 只生成文件，不推送
  --force-readme                   # 覆盖已存在的 README.md

# 只生成 README，不做 git 操作
python scripts/gen_readme.py ./my-skill --output ./README.md

# 只做诊断，不修改任何文件  
python scripts/validate_publish.py ./my-skill
```

---

## 注意事项

- `gh` CLI 路径：`F:\Program Files\GitHub CLI\gh.exe`（Windows 环境）
- 发布时通过 PowerShell 脚本调用 `gh`，需设置 `$env:GH_TOKEN`
- `--force-readme` 覆盖已有 README 前会先备份为 `README.md.bak`
- 如果 SKILL.md 的 description 很短（< 20字），会提示补充后再发布
- 私有仓库需要 GitHub Pro 或 organization 权限

---

## Step 9 — 返回仓库 URL 与本地同步元数据(2026-06-11 增补)

**发布成功后必须执行以下操作**:

### 8.1 返回仓库 URL 给用户

在 Step 8 发布报告中,必须明确输出:

```
✅ GitHub 仓库 URL: https://github.com/{owner}/{repo}
✅ 本地路径: ~/.claude/skills/{collection}/{skill-name}/SKILL.md
✅ 远端默认分支: {main | master}
```

### 8.2 写回仓库 URL 到本地 SKILL.md

为支持后续"远程实时同步"和"自动持久同步"(hooks/CI 监听),**发布成功后将仓库 URL 写回本地 SKILL.md 的 YAML frontmatter**:

```yaml
---
name: {skill-name}
description: ...
repository: https://github.com/{owner}/{repo}  # 新增字段
default_branch: main                             # 新增字段
published_at: 2026-06-11                         # 新增字段(ISO 8601)
---
```

**写入规则**:
- 使用 `Edit` 工具精确插入,不要破坏原有 frontmatter
- 如果 `repository` 字段已存在,询问用户是否更新
- 字段顺序按 `name → description → repository → default_branch → published_at` 排列

**目的**:
- 任何 AI 读到该 skill 时,立即知道远端位置
- 后续 `prp-commit`、`prp-pr` 等技能可直接读 `repository` 字段推送
- hooks/CI 可基于 `published_at` 字段做变更检测

### 8.3 远程实时同步指引(给用户)

在发布报告末尾追加:

```
📡 远程同步提示:
- 本地修改后,在 skill 目录下执行:
  git add . && git commit -m "..." && git push
- 或使用 prp-commit 技能(自动读取 repository 字段推送)
- 自动持久同步需配置 hooks(用 update-config / hookify 技能)
  监听 SKILL.md / scripts/ / references/ 变更 → 自动 commit + push
```

---

## 认证与 Token 管理(2026-06-11 增补)

### ⚠️ 安全红线

**绝对禁止**将 GitHub Personal Access Token 明文写入:
- `SKILL.md` 或任何 skill 文件
- `publish.py` 等脚本文件
- `.gitignore` 之外的配置文件
- 任何会被 git 跟踪的文件
- 任何会被 AI 读入上下文的文件

**Token 一旦写入上述文件,会立即:**
1. 被 git 跟踪 → 推送到 GitHub 时公开
2. 被 AI 加载到上下文 → 在对话中泄露
3. 被分享/截图/记录 → 永久泄露
4. GitHub 自动检测并撤销该 token

### ✅ 正确做法:环境变量 + 优先级链

**Token 优先级链**(从高到低):

| 优先级 | 来源 | 适用场景 |
|--------|------|----------|
| 1 | `GH_TOKEN` 环境变量 | 临时单次使用 |
| 2 | `GITHUB_TOKEN` 环境变量 | GitHub Actions / Codespaces |
| 3 | `~/.netrc` 文件(machine github.com) | 长期多仓库使用 |
| 4 | git credential helper(`gh auth login` 配置) | 长期多仓库使用(推荐) |
| 5 | SSH key(`~/.ssh/id_ed25519` + GitHub SSH 配置) | 高级用户 |

**推荐配置**(长期多仓库):

```bash
# Windows PowerShell(永久)
[System.Environment]::SetEnvironmentVariable("GH_TOKEN", "ghp_xxx...", "User")

# Windows Git Bash
echo 'export GH_TOKEN="ghp_xxx..."' >> ~/.bashrc

# macOS / Linux
echo 'export GH_TOKEN="ghp_xxx..."' >> ~/.zshrc
```

**单次使用**(不写入任何文件):

```bash
GH_TOKEN=ghp_xxx... python scripts/publish.py ./my-skill
# 或
git push https://x-access-token:ghp_xxx...@github.com/owner/repo.git master
```

### publish.py 改造要求

`publish.py` 等脚本读取 token 时,必须按优先级链:

```python
import os
token = (
    os.environ.get("GH_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
    or _read_netrc_token()      # 从 ~/.netrc 读
    or _read_gh_credential()   # 从 gh credential helper 读
)
if not token:
    sys.exit("❌ 未找到 GitHub Token。请设置 GH_TOKEN 环境变量或运行 gh auth login")
```

**禁止行为**:
- ❌ `--token ghp_xxx...` 命令行参数(会留在 shell history)
- ❌ `token = "ghp_xxx..."` 硬编码
- ❌ 提示"请把 token 发给我"然后写入文件
- ❌ 写入 `.env` 文件但不加入 `.gitignore`

---

## 参考文件

- `scripts/publish.py` — 主入口，协调全流程
- `scripts/gen_readme.py` — 双语 README 生成器（核心）
- `scripts/build_uss.py` — USS 全平台兼容打包器
- `scripts/validate_publish.py` — 结构验证器
- `scripts/parse_skill_meta.py` — SKILL.md 元数据解析
- `references/readme_guide.md` — README 写作规范与示例
- `assets/gitignore_template.txt` — .gitignore 标准模板
- `assets/license_templates/` — MIT / Apache / GPL 协议模板

---

## 增量更新历史

### v2.0.0 (2026-06-12)
- **新增 USS 全平台兼容打包**(Universal Skill Standard v1.0):发布前自动生成 `prompt.md` / `prompt_compact.md` / `manifest.json` / `openai_tool.json`
- **新增 `scripts/build_uss.py`**:从 SKILL.md 自动提取元数据,生成跨平台适配文件
- **更新 `publish.py`**:Step 1.5 嵌入 USS 构建流程,发布即全平台兼容
- **更新 `validate_publish.py`**:新增 USS 文件状态检查
- **更新 SKILL.md**:Step 3 改为 USS 打包,后续步骤重新编号(Step 4→Step 9)
- **背景**:用户要求任何发布的 skill 都能在 Claude Code / Cursor / Copilot / Codex / OpenClaw / Hermes / Coze / Dify / LangChain 等平台直接使用

### v1.1.0 (2026-06-11)
- **新增 Step 9**:发布成功后返回仓库 URL,写回本地 SKILL.md frontmatter
- **新增认证与 Token 管理**:强制使用环境变量优先级链,禁止明文存储
- **背景**:industry-research 推送时用户已提供 token,为避免 SKILL.md 中明文记录 token 导致泄露,补全安全红线 + 正确做法
