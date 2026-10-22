# -*- coding: utf-8 -*-
"""生成 5 张分享 PPT（方案二：桌面 Agent + IDE 插件）。

可重复运行：screenshots/ 下的同名图片被真机截图覆盖后，重跑本脚本即可刷新 PPT。
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "screenshots"
OUT = ROOT / "03-分享PPT.pptx"

INK = RGBColor(0x14, 0x21, 0x3D)
ACCENT = RGBColor(0x2F, 0x6F, 0xEB)
ACCENT_DK = RGBColor(0x1B, 0x4A, 0xA8)
LIGHT = RGBColor(0xEE, 0xF3, 0xFC)
GREY = RGBColor(0x6B, 0x72, 0x80)
LINE = RGBColor(0xD6, 0xDE, 0xEA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Microsoft YaHei"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def tb(slide, x, y, w, h, text, size=16, bold=False, color=INK, align=PP_ALIGN.LEFT,
       font=FONT, line_spacing=None, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return box


def rect(slide, x, y, w, h, fill=LIGHT, line=None, radius=False):
    shp = slide.shapes.add_shape(
        5 if radius else 1, Inches(x), Inches(y), Inches(w), Inches(h)  # 5=ROUNDED_RECTANGLE
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def new_slide(title, kicker=None, page=None):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, 13.333, 0.10, fill=ACCENT)
    if kicker:
        tb(s, 0.75, 0.42, 11, 0.32, kicker, 12, True, ACCENT)
        tb(s, 0.75, 0.72, 11.8, 0.62, title, 29, True, INK)
    else:
        tb(s, 0.75, 0.55, 11.8, 0.7, title, 30, True, INK)
    rect(s, 0.75, 1.42, 0.9, 0.055, fill=ACCENT)
    if page:
        tb(s, 12.2, 6.95, 0.5, 0.3, str(page), 11, False, GREY, PP_ALIGN.RIGHT)
    return s


def _units(text):
    """按 em 估算行宽：全角 1.0、半角 0.52。"""
    return sum(1.0 if ord(ch) > 0x2E80 else 0.52 for ch in text)


def _lines(text, width_in, size):
    capacity = width_in * 72.0 / size
    import math
    return max(1, math.ceil(_units(text) / capacity))


def bullet_block(slide, x, y, w, items, size=16, gap=0.16, lead_color=ACCENT_DK):
    """items: list of (lead, body) —— lead 加粗彩色，body 常规。"""
    cy = y
    for lead, body in items:
        dot = slide.shapes.add_shape(9, Inches(x), Inches(cy + size / 72.0 * 0.42), Inches(0.09), Inches(0.09))
        dot.fill.solid()
        dot.fill.fore_color.rgb = ACCENT
        dot.line.fill.background()
        box = slide.shapes.add_textbox(Inches(x + 0.28), Inches(cy), Inches(w - 0.28), Inches(0.6))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = lead
        r1.font.size = Pt(size)
        r1.font.bold = True
        r1.font.color.rgb = lead_color
        r1.font.name = FONT
        r2 = p.add_run()
        r2.text = body
        r2.font.size = Pt(size)
        r2.font.color.rgb = INK
        r2.font.name = FONT
        lines = _lines(lead + body, w - 0.28, size)
        cy += lines * size * 1.52 / 72.0 + gap
    return cy


def table(slide, x, y, w, rows, col_w, header_fill=ACCENT_DK, size=13, row_h=0.42):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    t = shape.table
    for i, cw in enumerate(col_w):
        t.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        t.rows[r].height = Inches(row_h)
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = ""
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = str(val)
            run.font.size = Pt(size)
            run.font.name = FONT
            if r == 0:
                run.font.bold = True
                run.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill
            else:
                run.font.color.rgb = INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r % 2 else LIGHT
    return t


def shot(slide, x, y, w, h, name, caption):
    p = SHOTS / name
    if p.exists():
        slide.shapes.add_picture(str(p), Inches(x), Inches(y), width=Inches(w))
    else:
        rect(slide, x, y, w, h, fill=LIGHT, line=LINE)
        tb(slide, x, y + h / 2 - 0.2, w, 0.4, "（截图缺失）" + name, 12, False, GREY, PP_ALIGN.CENTER)
    tb(slide, x, y + h + 0.08, w, 0.3, caption, 11, False, GREY)


# ---------------------------------------------------------------- 1 封面
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, fill=INK)
rect(s, 0, 0, 13.333, 0.18, fill=ACCENT)
tb(s, 0.95, 1.55, 11.5, 0.4, "AI 编程助手配置实训 · 方案二", 15, True, RGBColor(0x8F, 0xB6, 0xFF))
tb(s, 0.95, 2.05, 11.6, 1.4, "为 PyCharm 配置\n桌面 Agent + IDE 插件", 40, True, WHITE, line_spacing=1.15)
rect(s, 0.95, 3.95, 1.1, 0.06, fill=ACCENT)
tb(s, 0.95, 4.25, 11.2, 0.9,
   "Claude Code Agent（v2.1.283） + PyCharm 插件「Claude Code」（v0.5.7）", 18, False, RGBColor(0xC7, 0xD3, 0xE6))
tb(s, 0.95, 5.55, 11, 0.4, "肖俊涛 · 2405100606", 16, True, WHITE)
tb(s, 0.95, 5.98, 11, 0.4, "PyCharm 2026.2.2 (PY-262.10315.174) · Windows · 2026-10-21", 13, False,
   RGBColor(0x9F, 0xAF, 0xC6))

# ---------------------------------------------------------------- 2 先回答：这是方案几
s = new_slide("先回答一个问题：我现在配的是方案几？", "判定结论", 2)
rect(s, 0.75, 1.75, 11.85, 0.95, fill=LIGHT)
tb(s, 0.98, 1.92, 11.4, 0.6,
   "方案二：桌面 Agent + IDE 插件模式", 24, True, ACCENT_DK)
tb(s, 0.98, 2.30, 11.4, 0.4,
   "任务书写的代表工具是 AionClaw；本机装的是同架构的 Claude Code + PyCharm 插件，路线一致", 12, False, GREY)

cards = [
    ("证据 1", "插件本身不含模型", "plugins\\idea-claude-code-gui v0.5.7 —— 只是交互窗口 + 桥接层"),
    ("证据 2", "外部确有 Agent 主程序", "claude --version → 2.1.283，落在 AppData\\Roaming\\npm"),
    ("证据 3", "会话从 IDE 内发起", ".idea\\claudeCodeTabState.xml：provider=claude，model=claude-sonnet-5[1m]"),
    ("证据 4", "API 收口在 Agent 侧", "settings.json：BASE_URL 指向 /anthropic 兼容端点，模型别名统一映射"),
]
cx, cy = 0.75, 2.95
for i, (tag, head, body) in enumerate(cards):
    x = cx + (i % 2) * 6.05
    y = cy + (i // 2) * 1.85
    rect(s, x, y, 5.75, 1.62, fill=WHITE, line=LINE, radius=True)
    tb(s, x + 0.28, y + 0.18, 1.2, 0.3, tag, 11, True, ACCENT)
    tb(s, x + 0.28, y + 0.5, 5.2, 0.36, head, 16, True, INK)
    tb(s, x + 0.28, y + 0.95, 5.2, 0.5, body, 11.5, False, GREY)

# ---------------------------------------------------------------- 3 为什么选方案二
s = new_slide("为什么选方案二：任务形态决定了工具形态", "选型理由", 3)
bullet_block(s, 0.75, 1.75, 6.05, [
    ("读陌生工程，第一步是「把链路读出来」。", "方案一只能解释打开着的那个文件，Agent 能自己把 parser → matcher → api 走一遍。"),
    ("读完之后紧接着是改造：改代码、加用例、跑测试。", "这是任务级动作，需要连续执行 + 看懂报错再回头改，只有 Agent 有这双手。"),
    ("API 只需收口一处。", "Agent 侧一份 settings.json 定死端点/密钥/模型别名，IDE 侧不再各自配。"),
], size=15)
rect(s, 7.15, 1.75, 5.45, 2.55, fill=INK)
tb(s, 7.45, 1.98, 4.9, 0.32, "一句话选型逻辑", 12, True, RGBColor(0x8F, 0xB6, 0xFF))
tb(s, 7.45, 2.42, 4.9, 1.6, "行级、跟随光标的工作\n交给 IDE；\n任务级、跨文件的工作\n交给 Agent。", 17, True, WHITE, line_spacing=1.3)
rect(s, 7.15, 4.6, 5.45, 2.05, fill=LIGHT)
tb(s, 7.45, 4.8, 4.9, 0.32, "本机还有方案一的对照组", 12, True, ACCENT_DK)
tb(s, 7.45, 5.18, 4.95, 1.3,
   "Comate 4.14.0 / Copilot 1.17.0 / Qoder CN 2026.917\n都在同一台机器、同一个工程里跑过——\n对比数据来自实测，不是查资料。", 12.5, False, INK, line_spacing=1.35)

# ---------------------------------------------------------------- 4 安装三步
s = new_slide("安装：先装手，再装窗口", "实施路径", 4)
steps = [
    ("STEP 1", "装 Node 与 CLI", "npm i -g @anthropic-ai/claude-code\nclaude --version → 2.1.283", "Agent 主程序：读写文件、跑命令"),
    ("STEP 2", "PyCharm 装插件", "Settings → Plugins →\n搜 Claude Code → Install → 重启", "交互窗口 + 上下文桥接"),
    ("STEP 3", "打开面板握手", "右侧 Claude Code 图标 →\n生成 .idea\\claudeCodeTabState.xml", "握手成功的证据文件"),
]
for i, (tag, head, code, note) in enumerate(steps):
    x = 0.75 + i * 4.03
    rect(s, x, 1.75, 3.75, 3.05, fill=WHITE, line=LINE, radius=True)
    tb(s, x + 0.28, 1.95, 3.2, 0.3, tag, 11, True, ACCENT)
    tb(s, x + 0.28, 2.28, 3.25, 0.4, head, 17, True, INK)
    tb(s, x + 0.28, 2.82, 3.25, 0.95, code, 11.5, False, ACCENT_DK, line_spacing=1.35)
    tb(s, x + 0.28, 4.08, 3.25, 0.5, note, 11, False, GREY)
    if i < 2:
        tb(s, x + 3.78, 2.95, 0.3, 0.4, ">", 20, True, LINE)
table(s, 0.75, 5.0, 11.85, [
    ["组件", "版本 / 路径", "作用"],
    ["PyCharm", "2026.2.2 · PY-262.10315.174", "解释器、调试、诊断、上下文来源"],
    ["插件 idea-claude-code-gui", "0.5.7", "会话界面，把改动以 diff 回填"],
    ["Claude Code CLI", "2.1.283 · Node v24.17.0", "执行：Read / Write / Edit / Bash"],
], [3.7, 4.4, 3.75], row_h=0.42, size=12)

# ---------------------------------------------------------------- 5 配置
s = new_slide("配置：API 地址、模型名、角色分工", "关键配置", 5)
rect(s, 0.75, 1.75, 6.1, 2.3, fill=RGBColor(0x0F, 0x17, 0x2A))
tb(s, 0.98, 1.92, 5.6, 0.3, "C:\\Users\\16218\\.claude\\settings.json", 10.5, False, RGBColor(0x8F, 0xB6, 0xFF))
tb(s, 0.98, 2.28, 5.7, 1.6,
   '"ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",\n'
   '"ANTHROPIC_AUTH_TOKEN": "sk-****（脱敏）",\n'
   '"ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-flash"', 11.5, False, RGBColor(0xC9, 0xE3, 0xFF), line_spacing=1.45)
table(s, 0.75, 4.25, 6.1, [
    ["插件下拉显示", "实际模型"],
    ["Sonnet", "deepseek-flash"],
    ["Opus / Haiku / 兜底", "deepseek-flash"],
], [3.1, 3.0], row_h=0.38, size=12)
tb(s, 0.75, 5.45, 6.1, 0.75,
   "模型名以网关回显为准：历史会话计费记录里服务端返回的是 DeepSeek-V4-Pro。", 11, False, GREY, line_spacing=1.3)

rect(s, 7.2, 1.75, 5.4, 0.5, fill=ACCENT_DK)
tb(s, 7.2, 1.83, 5.4, 0.34, "角色分工", 13, True, WHITE, PP_ALIGN.CENTER)
roles = [("IDE（PyCharm）", "给上下文：解释器、断点、诊断、Git 视图"),
         ("插件（GUI）", "给界面：会话渲染、diff 回填、上下文投递"),
         ("Agent（CLI）", "给手脚：读写文件、执行命令、多步编排")]
ry = 2.4
for name, desc in roles:
    rect(s, 7.2, ry, 5.4, 1.15, fill=LIGHT if name.startswith("插件") else WHITE, line=LINE)
    tb(s, 7.42, ry + 0.14, 2.1, 0.34, name, 13, True, ACCENT_DK)
    tb(s, 7.42, ry + 0.55, 4.95, 0.5, desc, 11.5, False, INK, line_spacing=1.25)
    ry += 1.25
tb(s, 7.2, 6.25, 5.4, 0.35, "一句话：IDE 给上下文，插件给界面，Agent 给手脚。", 11.5, True, GREY)

# ---------------------------------------------------------------- 6 验证一：对话
s = new_slide("验证一：对话 —— 代码逐行解释", "功能验证 1/3", 6)
bullet_block(s, 0.75, 1.75, 5.35, [
    ("提问：", "「这一段代码有什么问题」——回答按「第一部分：导入包」逐条展开，即逐行解释"),
    ("输入：", "G:\\PycharmProjects\\test.py（KMeans 四簇聚类示例）"),
    ("结果：", "讲清 make_blobs 的 n_features=2 是为二维可视化服务、centers 必须是 4 个 2 维点、fit_predict 一步完成拟合+打标"),
    ("价值：", "把「隐含约束」讲出来，而不只是翻译语法"),
], size=13.5, gap=0.42)
shot(s, 6.35, 1.75, 6.25, 3.91, "03-dialog-explain.png", "Claude Code 面板内的逐行解释")

# ---------------------------------------------------------------- 7 验证二、三
s = new_slide("验证二、三：测试生成 + Agent 闭环", "功能验证 2/3 · 3/3", 7)
for i, (nm, cap) in enumerate([
    ("04-completion-test.png", "① 生成 test_kmeans.py，diff 审查后「应用」"),
    ("05-agent-task.png", "② 首跑失败 → 判定断言 0.99 不可达 → 改 0.95"),
    ("06-agent-summary.png", "③ 收尾：8 用例全过，耗时 7:47 / 输入 527.5k"),
]):
    x = 0.75 + i * 4.15
    shot(s, x, 1.70, 3.85, 2.41, nm, cap)
tb(s, 0.75, 4.55, 12.0, 1.0,
   "补全只需要 0.5 秒给我一行代码；这套流程用了 7 分 47 秒 —— 它自己建文件、装 pytest、跑测试、\n"
   "看懂失败原因、把断言改成可达的值。时间花在「执行」上，而不是「敲字」上。",
   13, False, INK, line_spacing=1.45)
tb(s, 0.75, 5.95, 12.0, 0.6,
   "三张图是同一个任务的连续三段：下发 → 落盘（人工审查 diff）→ 收敛。全程没有复制过一次报错。",
   11.5, False, GREY)

# ---------------------------------------------------------------- 8 对比
s = new_slide("对比：建议层 vs 执行层", "方案一 vs 方案二", 8)
table(s, 0.75, 1.75, 11.85, [
    ["维度", "方案一（纯 IDE 插件）", "方案二（Agent + 插件）"],
    ["执行主体", "IDE 进程内的客户端，无执行权", "IDE 外的独立进程，有文件与命令执行权"],
    ["响应节奏", "0.5–1.5 秒内出补全（Comate 配置）", "单轮 API 约 80 秒，任务总时长可达数分钟"],
    ["上下文范围", "当前文件 + 约 30 行相邻上下文", "整个工程，可自行 Read / Grep 任意文件"],
    ["典型输入", "「补全这个函数」「解释这段」", "「跑通 test.py，报错就修好」"],
    ["主要成本", "订阅费固定，风险约等于零", "按 token 计费（单轮约 3 万 input），改错有代价"],
], [2.35, 4.6, 4.9], row_h=0.62, size=12.5)
rect(s, 0.75, 6.05, 11.85, 0.75, fill=LIGHT)
tb(s, 1.0, 6.2, 11.4, 0.45,
   "结论：不是替代关系 —— 方案一守「写」这一段，方案二覆盖「读进来」与「跑出去」两端。", 13.5, True, ACCENT_DK)

# ---------------------------------------------------------------- 9 踩坑 + 心得
s = new_slide("踩过的坑，和如果重来", "复盘", 9)
tb(s, 0.75, 1.72, 5.5, 0.34, "真实踩坑（均有报错/痕迹为证）", 13, True, ACCENT_DK)
pits = [
    ("%matplotlib inline 报 SyntaxError", "魔法命令只在 .ipynb 有效"),
    ("sklearn 私有模块 _samples_generator", "公开 API 是 datasets.make_blobs"),
    ("面板空白 / 找不到 claude", "插件只是窗口，CLI 必须先在 PATH"),
    ("第三方端点 401 / model not found", "URL 要带 /anthropic、四个别名要写全"),
    ("中文注释乱码（鏇存敼…）", "File Encodings 三项统一 UTF-8"),
]
py = 2.12
for t, c in pits:
    rect(s, 0.75, py, 5.55, 0.78, fill=WHITE, line=LINE)
    tb(s, 0.95, py + 0.10, 5.2, 0.3, t, 11.5, True, INK)
    tb(s, 0.95, py + 0.42, 5.2, 0.3, c, 10.5, False, GREY)
    py += 0.88
rect(s, 6.7, 1.72, 5.9, 2.05, fill=INK)
tb(s, 6.95, 1.9, 5.4, 0.3, "使用心得", 12, True, RGBColor(0x8F, 0xB6, 0xFF))
tb(s, 6.95, 2.28, 5.4, 1.35,
   "① 「问」和「派活」是两种交互，别混用。\n"
   "② 让 Agent 先 Read + 说计划，再放开写权限。\n"
   "③ 读码用默认模式，机械活用 acceptEdits。", 12, False, WHITE, line_spacing=1.45)
rect(s, 6.7, 3.97, 5.9, 2.55, fill=LIGHT)
tb(s, 6.95, 4.14, 5.4, 0.3, "如果重来：换插件侧，不换 Agent 侧", 12, True, ACCENT_DK)
tb(s, 6.95, 4.55, 5.45, 1.9,
   "「插件 + 外部 CLI」的版本耦合与上下文延迟是真实摩擦；\n"
   "一体化 IDE（Qoder / Trae 一类）把三个件收进一个发布包。\n"
   "但选型的分界线不变：任务里有没有「执行」这一环。\n"
   "所以重来一次换的只是窗口，Agent 那双手不动。", 11, False, INK, line_spacing=1.45)

# ---------------------------------------------------------------- 10 收尾
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, fill=INK)
rect(s, 0, 0, 13.333, 0.18, fill=ACCENT)
tb(s, 0.95, 2.2, 11.5, 0.4, "5 分钟分享 · 现场可操作", 14, True, RGBColor(0x8F, 0xB6, 0xFF))
tb(s, 0.95, 2.7, 11.4, 1.2, "谢谢，欢迎提问", 44, True, WHITE)
tb(s, 0.95, 3.95, 11.4, 1.0,
   "一个可以直接复现的结论：\n先装手（Agent），再装窗口（插件），配置收口到 settings.json 一处。",
   15, False, RGBColor(0xC7, 0xD3, 0xE6), line_spacing=1.45)
tb(s, 0.95, 5.9, 11.4, 0.4, "肖俊涛 · 2405100606 · 2026-10-21", 12, False, RGBColor(0x9F, 0xAF, 0xC6))

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
