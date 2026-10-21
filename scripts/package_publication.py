"""Create a publication folder and ZIP from explicitly approved artifacts."""
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / "output"
DESTINATION = OUTPUT / "X发布包-爱马仕币安钱包"
SOURCES = {
    "01-复制到X专用.html": ROOT / "docs" / "X-PASTE.html",
    "01-长文正文.txt": ROOT / "docs" / "X-LONGPOST.txt",
    "01-长文加粗预览.html": ROOT / "docs" / "X-LONGPOST.html",
    "01-长文加粗稿.md": ROOT / "docs" / "X-LONGPOST.md",
    "02-封面.png": ROOT / "assets" / "tutorial-cover.png",
    "03-四步操作图.png": ROOT / "assets" / "tutorial-steps.png",
    "04-给读者的开源安装包.zip": OUTPUT / "hermes-agentic-wallet-starter-0.1.0.zip",
}
NOTE = """发布方式

1. 用浏览器打开 01-复制到X专用.html，点击“复制正文（含加粗与空行）”。
   回到 X，在正文编辑区域选中并替换旧稿，再正常按 Ctrl+V 粘贴，检查空行和加粗。
   此版本保留原长文，段落使用实际换行，不依赖网页段距。复制按钮只复制正文，不包括工具栏。
   X 长推文支持原生加粗和斜体，不要依赖 Markdown 的 ** 符号自动转换。
   若加粗未保留，按预览稿选中相应文字，再用 X 编辑器的加粗功能。
   01-长文正文.txt 是不含 Markdown 标记的备用纯文本；01-长文加粗稿.md 是排版源稿。
2. 先上传 02-封面.png，再上传 03-四步操作图.png。
3. 文末按“评论「钱包」领取”编写，没有未填写的仓库链接。
4. 有读者领取时，给他 04-给读者的开源安装包.zip；附带的完整教程和提示词在 docs/ 里。

请只给读者发 04 这个源码 ZIP，不要发你电脑上的 .runtime 目录、登录链接或配对页面。
公开仓库：https://github.com/0xsissi/hermes-agentic-wallet-starter
本工具不会自动发布推特或发送私信。

验证范围：Windows 环境安装、技能加载、安装脚本检查已经验证；
WorkBuddy 账号登录到 Hermes 的实际模型调用，需要使用读者本人的账号测试。
图示由代码原创绘制，不是运行结果截图。
"""


def main():
    for source in SOURCES.values():
        if not source.is_file():
            raise RuntimeError(f"Missing publication file: {source}")
    DESTINATION.mkdir(exist_ok=True)
    for name, source in SOURCES.items():
        shutil.copyfile(source, DESTINATION / name)
    (DESTINATION / "00-发布说明.txt").write_text(NOTE, encoding="utf-8")
    bundle = OUTPUT / "X发布包-爱马仕币安钱包.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in ["00-发布说明.txt", *SOURCES]:
            archive.write(DESTINATION / name, f"X发布包-爱马仕币安钱包/{name}")
    print(bundle)
    print(f"{len(SOURCES) + 1} files, {bundle.stat().st_size} bytes")


if __name__ == "__main__":
    main()
