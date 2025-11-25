# OpenMind 环境配置指南

本项目支持使用 uv（推荐，速度极快）或 poetry 进行依赖管理。

由于项目包含 PyTorch 和 CUDA 依赖，建议在配置前确认显卡驱动已正确安装。

## 方案一：使用 UV (推荐)

`uv` 是一个基于 Rust 的极速 Python 包管理器，支持 PEP 621 标准。

### 1. 安装 uv

如果尚未安装，请在终端运行：

```
# macOS/Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (PowerShell)
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

### 2. 创建并激活环境

**选项 A：在当前目录下创建（推荐）**

```
cd uv_environment
uv venv .venv --python 3.10

# 激活
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows
```

**选项 B：在指定位置创建**

```
uv venv ~/venvs/openmind_uv --python 3.10

# 激活
source ~/venvs/openmind_uv/bin/activate
```

### 3. 同步依赖

此步骤会根据 `pyproject.toml` 和 `uv.lock` 安装所有依赖（包括 CUDA 版本的 PyTorch）。

```
# 安装所有依赖（包含 dev 组）
uv sync

# 如果已激活环境，确保同步到当前环境
uv sync --active

# 仅安装生产环境依赖
# uv sync --no-dev
```

### 4. 常用命令大全

**📦 依赖管理**

```
uv add numpy                # 添加最新版依赖
uv add pandas==2.2.0        # 添加指定版本
uv add "package>=1.0"       # 添加版本约束
uv add --dev pytest         # 添加开发依赖 (添加到 dev 组)
uv remove numpy             # 移除依赖
uv lock                     # 仅更新 uv.lock 文件但不安装
uv pip tree                 # 查看已安装包的依赖树 (类似 pipdeptree)
uv pip list                 # 列出当前环境所有包

uv add --active <package>   # 在当前环境安装包
uv sync --active --python 3.12.6
```

**🚀 运行与执行**

```
uv run script.py            # 在虚拟环境中运行脚本 (无需显式激活)
uv run python               # 进入虚拟环境的 Python 交互式终端
# 临时环境运行 (不污染当前环境)
uv run --with requests script.py
```

**🐍 Python 版本管理**

```
uv python list              # 列出可用的 Python 版本
uv python install 3.11      # 下载并安装特定 Python 版本
uv python pin 3.11          # 将当前项目锁定到 Python 3.11
```

**🛠️ 维护与清理**

```
uv cache clean              # 清理 uv 的全局缓存
uv self update              # 更新 uv 自身到最新版
```

## 方案二：使用 Poetry (传统方式)

**注意**：当前的 `pyproject.toml` 采用了新的 PEP 621 标准。建议使用 Poetry 1.8+ 版本。

### 1. 安装与配置

```
# 安装
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -

# 配置：将虚拟环境创建在项目根目录
poetry config virtualenvs.in-project true
```

### 2. 安装与使用

```
# 安装依赖
poetry install

# 激活环境
poetry shell
```

### 3. 常用命令大全

**📦 依赖管理**

```
poetry add numpy            # 添加依赖
poetry add --group dev pytest # 添加开发依赖
poetry remove numpy         # 移除依赖
poetry update               # 更新所有依赖到符合约束的最新版
poetry lock                 # 仅生成/更新 poetry.lock 文件
```

**🔍 查看与检查**

```
poetry show                 # 列出已安装的包
poetry show --tree          # 显示依赖树结构 (非常有用，排查冲突神器)
poetry show --outdated      # 检查有哪些包可以更新
poetry check                # 检查 pyproject.toml 配置是否有效
```

**🏗️ 运行与构建**

```
poetry run python app.py    # 在虚拟环境中运行命令
poetry build                # 构建源码包和 Wheel 包
# 导出 requirements.txt (常用于 Docker 构建)
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

**🔧 环境管理**

```
poetry env info             # 查看当前环境路径和信息
poetry env list             # 列出该项目所有关联的虚拟环境
poetry env remove python    # 删除当前虚拟环境
```

## 方案三：Conda + UV (混合模式)

适用于习惯使用 Conda 管理 Python 版本，但希望利用 uv 加速包安装的场景。

```
# 1. 创建并激活 Conda 环境
conda create -n openmind_env python=3.10 -y
conda activate openmind_env

# 2. 安装 uv
pip install uv

# 3. 使用 uv 安装依赖到当前 Conda 环境
# --system 参数表示安装到当前系统/环境，而非创建新 venv
uv sync --system
# 或者旧版命令：uv pip install -r pyproject.toml
```

## 代码质量检查 (Pre-commit)

本仓库已配置钩子，覆盖 Python (Ruff/MyPy)、C++ (Clang)、Bash (ShellCheck) 及 Markdown 检查。

### 1. 安装与初始化

```
# 安装工具
uv pip install pre-commit ruff mypy  # 或者 pip install ...

# 安装 Git 钩子
pre-commit install
```

### 2. 准备 C++ 编译数据库 (仅 C++ 开发需要)

`clang-tidy` 依赖编译数据库，需先生成 `compile_commands.json`：

```
bash scripts/build_project.sh
```

### 3. 执行检查

由于配置了 `manual` 阶段，请使用以下命令进行**全量检查与自动修复**：

```bash
# 推荐：运行所有手动阶段的钩子 (Ruff, Clang-format, MyPy 等)
pre-commit run --hook-stage manual -a
```

- **常规全量检查**：`pre-commit run -a` (仅运行基础钩子)
- **临时跳过某检查**：`SKIP=clang-tidy-conda pre-commit run --hook-stage manual -a`

### 4.pre-commit常用命令

```bash
pre-commit autoupdate  # 自动更新pre-commit配置版本号，容易造成一些版本不兼容
```

## 其他常用工具

### Ruff (Python 规范)

项目使用 Ruff 进行极速 Lint 和格式化：

```
ruff check .   # 检查代码问题
ruff format .  # 格式化代码
```

### Algorithms (算法包)

环境集成了 `algorithms` 包，可直接调用通用算法实现：

```
from algorithms.sort import merge_sort
# 使用相关算法功能
```

## 常见问题 (FAQ)

1. **uv sync 速度慢？**

   - 检查 `pyproject.toml` 中的 `[[tool.uv.index]]`，默认已配置阿里云镜像。

1. **CUDA 版本不匹配？**

   - 当前配置强制使用 CUDA 12.4 (`cu124`)。如果显卡驱动较旧，请升级驱动或在 `pyproject.toml` 中修改为 `cu118`。

1. **验证 PyTorch 安装**

   ```
   uv run python -c "import torch; print(f'Torch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
   ```

   预期输出：`Torch: 2.5.1+cu124, CUDA: True`
