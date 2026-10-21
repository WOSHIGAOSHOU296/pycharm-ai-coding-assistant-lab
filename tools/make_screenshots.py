# -*- coding: utf-8 -*-
"""生成 5 张截图占位图（同名覆盖即可替换为真机截图）。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

FONT_CANDIDATES = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]


def font(size, bold=False):
    for p in (FONT_CANDIDATES if bold else FONT_CANDIDATES):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


SPECS = [
    ("01-pycharm-plugins.png", "图 1 · PyCharm 已安装插件列表",
     ["Settings -> Plugins -> Installed", "需可见 Claude Code / Comate / Copilot"]),
    ("02-api-config.png", "图 2 · API 地址与模型名",
     ["settings.json 的 env 段，或插件内模型下拉", "token 必须打码"]),
    ("03-dialog-explain.png", "图 3 · 对话：逐行解释代码",
     ["Claude Code 面板内提问 test.py", "截到解释正文"]),
    ("04-completion-test.png", "图 4 · 补全 / 测试生成",
     ["行内 ghost text，或 Agent 生成的 pytest 用例与运行结果"]),
    ("05-agent-task.png", "图 5 · Agent 任务：改代码 + 跑命令",
     ["面板时间线含 Bash / Read / Edit / 重跑"]),
]

W, H = 1600, 1000
for name, title, lines in SPECS:
    img = Image.new("RGB", (W, H), "#F5F7FA")
    d = ImageDraw.Draw(img)
    # 边框
    d.rectangle([0, 0, W - 1, H - 1], outline="#C9D3E0", width=2)
    # 虚线感的内部框
    d.rectangle([40, 40, W - 41, H - 41], outline="#DCE3EC", width=2)
    # 标题
    d.text((W / 2, H / 2 - 150), title, font=font(54, True), fill="#1F3A5F", anchor="mm")
    d.text((W / 2, H / 2 - 60), "待补真实截图（用真机截图覆盖同名文件）",
           font=font(34), fill="#8A97A8", anchor="mm")
    y = H / 2 + 30
    for ln in lines:
        d.text((W / 2, y), ln, font=font(30), fill="#A7B2C2", anchor="mm")
        y += 56
    d.text((W / 2, H - 90), name, font=font(26), fill="#B9C3D0", anchor="mm")
    img.save(OUT / name, "PNG")
    print("wrote", OUT / name)
