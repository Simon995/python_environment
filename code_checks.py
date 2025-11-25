import subprocess
import sys

# 定义两种排除模式格式：正则表达式（用于支持正则的工具）和glob模式（用于支持glob的工具）
EXCLUDE_REGEX = (
    r".*/(train|file)(/.*)?"  # 精确匹配train或file目录及其子目录（正则表达式）
)
EXCLUDE_GLOB = "train,file,**/train/**,**/file/**"  # 显式包含顶层目录的Glob模式


def run_isort():
    """Run isort (使用Glob模式排除)"""
    print("Running isort...")
    subprocess.run(
        [
            "isort",
            ".",
            "--profile",
            "black",
            "--line-length",
            "119",
            "--skip",
            EXCLUDE_GLOB,
        ],
        check=True,
    )


def run_black():
    """Run black (使用正则表达式排除)"""
    print("Running black...")
    subprocess.run(
        [
            "black",
            ".",
            "--target-version",
            "py311",
            "--line-length",
            "119",
            "--exclude",
            EXCLUDE_REGEX,
        ],
        check=True,
    )


def run_flake8():
    """Run flake8 (使用改进的Glob模式排除)"""
    print("Running flake8...")
    subprocess.run(
        [
            "flake8",
            ".",
            "--max-line-length",
            "119",
            "--ignore",
            "E203,E231,E501,W503,W504,E401,E402,E741",
            "--exclude",
            EXCLUDE_GLOB,  # 传递显式包含顶层目录的Glob模式
        ],
        check=True,
    )


def run_mypy():
    """Run mypy (使用正则表达式排除)"""
    print("Running mypy...")
    subprocess.run(
        [
            "mypy",
            ".",
            "--ignore-missing-imports",
            "--disallow-untyped-calls",
            "--disallow-untyped-defs",
            "--exclude",
            EXCLUDE_REGEX,  # mypy使用正则表达式
        ],
        check=True,
    )


def run_pylint():
    """Run pylint (使用正则表达式排除)"""
    print("Running pylint...")
    subprocess.run(
        [
            "pylint",
            ".",
            "--max-line-length",
            "119",
            "--disable",
            "C0111",
            "--ignore-patterns",
            EXCLUDE_REGEX,  # pylint使用正则表达式
        ],
        check=True,
    )


def run_bandit():
    """Run bandit (使用glob模式排除)"""
    print("Running bandit...")
    subprocess.run(
        [
            "bandit",
            "-r",
            ".",
            "--severity",
            "HIGH",
            "--confidence",
            "HIGH",
            "--exclude",
            EXCLUDE_GLOB,  # bandit使用glob模式
        ],
        check=True,
    )


def main():
    """Main function to run all checks (按执行顺序编排)"""
    try:
        run_isort()  # 先执行导入排序
        run_black()  # 再执行代码格式化
        run_flake8()  # 基础代码检查
        # run_mypy()    # 类型检查（根据需要取消注释）
        # run_pylint()  # 深度代码质量检查（根据需要取消注释）
        # run_bandit()  # 安全扫描（根据需要取消注释）
    except subprocess.CalledProcessError as e:
        print(f"\033[31mError: {e.cmd[0]} failed with code {e.returncode}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
