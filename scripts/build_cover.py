"""Render original, text-first publication diagrams. Requires Pillow and a CJK font."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
BG = "#f5f2e9"
INK = "#18221e"
MUTED = "#56645c"
LINE = "#d7ded4"
YELLOW = "#f3ce45"
GREEN = "#234f3e"


def font(size, bold=False):
    paths = ["C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
             "/System/Library/Fonts/PingFang.ttc",
             "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError("A CJK font is required.")


class Canvas:
    def __init__(self, height):
        self.im = Image.new("RGB", (1600, height), BG)
        self.d = ImageDraw.Draw(self.im)

    def text(self, x, y, label, size=32, fill=INK, bold=False):
        self.d.text((x, y), label, font=font(size, bold), fill=fill)

    def box(self, xy, fill="white", radius=28, outline=None):
        self.d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)

    def rule(self, y):
        self.d.line((80, y, 1520, y), fill=LINE, width=2)

    def pill(self, x, y, label, fill=GREEN, color="white", size=25):
        width = self.d.textlength(label, font=font(size, True)) + 44
        self.box((x, y, x + width, y + 48), fill, 24)
        self.text(x + 22, y + 6, label, size, color, True)
        return width

    def code(self, x, y, lines, width=1296):
        height = 32 + 48 * len(lines)
        self.box((x, y, x + width, y + height), INK, 18)
        for i, line in enumerate(lines):
            self.text(x + 24, y + 14 + i * 48, line, 29, "#e4f2e5")

    def save(self, name):
        target = ASSETS / name
        self.im.save(target, optimize=True)
        print(target)


def cover():
    c = Canvas(1000)
    c.pill(80, 64, "AI × 链上工具")
    c.text(1390, 74, "入门篇", 29, MUTED)
    c.text(78, 150, "用免费模型额度", 78, bold=True)
    c.box((74, 268, 1475, 385), YELLOW, 12)
    c.text(94, 275, "让爱马仕接上币安钱包", 92, bold=True)
    c.text(84, 416, "WorkBuddy AI  ×  Magpie  ×  Hermes", 39, GREEN, True)

    cards = [("01", "WorkBuddy AI", "模型额度"),
             ("02", "Magpie", "模型接线"),
             ("03", "Hermes", "理解和执行"),
             ("04", "Agentic Wallet", "授权与签名")]
    for i, (number, title, desc) in enumerate(cards):
        x = 80 + i * 368
        c.box((x, 513, x + 336, 728), "#ffffff", 25, LINE)
        c.text(x + 26, 531, number, 26, GREEN, True)
        c.text(x + 26, 579, title, 32, bold=True)
        c.text(x + 26, 639, desc, 31, MUTED)
        if i < 3:
            c.d.line((x + 343, 620, x + 359, 620), fill=GREEN, width=3)
            c.d.polygon([(x + 355, 613), (x + 365, 620), (x + 355, 627)], fill=GREEN)

    c.text(82, 770, "先查地址、看余额、拿报价", 42, bold=True)
    c.pill(984, 778, "附教程 + MIT 安装脚本", GREEN, size=26)
    c.rule(865)
    c.text(82, 892, "免费指模型额度；买币本金、Gas 和可能产生的交易服务费另计。", 27, MUTED)
    c.text(82, 941, "国际 WorkBuddy AI 为主 · 社区接入，以本人账号可用情况为准 · 2026.10", 23, MUTED)
    c.save("tutorial-cover.png")


def steps():
    c = Canvas(2000)
    c.pill(80, 58, "保存这张操作图")
    c.text(80, 135, "从安装到查余额", 77, bold=True)
    c.text(84, 242, "4 步接好爱马仕的钱包工具", 43, GREEN, True)
    c.text(84, 314, "先装 Node.js 24 LTS，解压配套源码包，在项目文件夹打开终端。", 29, MUTED)

    rows = [(390, 638, "1", "安装环境"),
            (664, 990, "2", "登录模型，保持 Magpie 运行"),
            (1016, 1428, "3", "另开终端：选模型，启动爱马仕"),
            (1454, 1798, "4", "扫码接钱包，先查地址和余额")]
    for top, bottom, number, title in rows:
        c.box((80, top, 1520, bottom), "white", 26, LINE)
        c.box((110, top + 29, 174, top + 93), YELLOW, 19)
        c.text(130, top + 31, number, 40, bold=True)
        c.text(198, top + 37, title, 39, bold=True)

    c.code(112, 509, ["node starter.mjs install"])
    c.text(118, 600, "首次需要下载依赖，保持终端开着。", 26, MUTED)

    c.code(112, 783, ["node starter.mjs workbuddy-login", "node starter.mjs magpie-ui"])
    c.text(118, 925, "在浏览器登录本人的国际 WorkBuddy AI 账号，核对额度。", 27, MUTED)

    c.code(112, 1135, ["node starter.mjs models",
                       "node starter.mjs set-model workbuddy-ai/真实模型ID",
                       "node starter.mjs agent"])
    c.text(118, 1324, "从实际列表复制模型 ID，替换占位文字；仍在同一项目文件夹。", 27, MUTED)
    c.text(118, 1371, "先让爱马仕回复一句话，确认模型能用，再连接钱包。", 27, MUTED)

    c.text(116, 1581, "在 Hermes 按包内教程发起钱包登录。", 33, GREEN, True)
    c.text(116, 1641, "核对官方链接与配对码 → 币安 App 确认 → 电脑显示 CONNECTED", 29)
    c.text(116, 1700, "之后只查 BSC 地址和余额。买币先看报价、费用，再明确确认。", 29, MUTED)

    c.rule(1844)
    c.text(84, 1870, "配套源码包内含完整教程、AI 代装提示词与排错说明。", 31, bold=True)
    c.text(84, 1928, "模型免费额度 ≠ 免费交易 · 社区接入，以本人账号可用情况为准 · 2026.10", 25, MUTED)
    c.save("tutorial-steps.png")


if __name__ == "__main__":
    cover()
    steps()
