# PyCharm AI 编程助手实训 · 交付包

> 课程任务：为 PyCharm 配置一款 AI 编程助手，完成代码阅读、解释、补全与任务自动化，并产出「操作指南手册 + 功能验证截图 + 对比分析报告 + 分享 PPT」。

## 一、方案判定结论（先看这里）

**你现在配置的是「方案二：桌面 Agent + IDE 插件模式」。**

判定依据（均来自本机实测，非推测）：

| 证据 | 位置 | 说明 |
| --- | --- | --- |
| IDE 里装的是 Agent 类插件 | `%APPDATA%\JetBrains\PyCharm2026.2\plugins\idea-claude-code-gui`（v0.5.7） | 插件本身不含模型，它是一层「交互窗口 + 桥接」，把会话交给外部 Agent 进程 |
| 桌面侧确有 Agent 主程序 | `C:\Users\16218\AppData\Roaming\npm\claude.ps1`，`claude --version` → `2.1.283 (Claude Code)` | 真正干活（读写文件、跑命令）的是这个 CLI Agent，插件只是它的窗口 |
| 插件在真实项目里跑过 | `G:\PycharmProjects\.idea\claudeCodeTabState.xml` | `provider=claude`、`model=claude-sonnet-5[1m]`、`permissionMode=default`、`cwd=G:\PycharmProjects`，说明会话是从 IDE 内发起的 |
| 走的是自建/第三方端点 | `C:\Users\16218\.claude\settings.json` | `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`，模型别名全部映射到 `deepseek-flash`，属于典型的「Agent 侧统一配 API、IDE 侧只做界面」 |

**注意：** 任务书里方案二的代表工具写的是「AionClaw 桌面客户端 + PyCharm 插件」，你机器上装的是同架构的 **Claude Code（CLI Agent）+ PyCharm「Claude Code」插件**。工具品牌不同、技术路线完全一致（Agent 主进程执行 + IDE 插件作交互窗口），因此按方案二写。

同时，你机器上还装着**方案一（纯 IDE 插件）**的三款：百度 Comate 4.14.0、GitHub Copilot 1.17.0、Qoder CN 2026.917。它们正好是方案一的「对照组」，第 02 份报告里的对比不是纸上谈兵——两侧都在这台机器上跑过。

## 二、交付物清单

| 序号 | 文件 | 对应任务书要求 |
| --- | --- | --- |
| 1 | [`01-操作指南手册.md`](01-操作指南手册.md) | 提交物 1：操作指南手册（Markdown，含 8 个必备章节 + 配图位） |
| 2 | [`02-对比分析报告.md`](02-对比分析报告.md) | 提交物 3：对比分析报告（1500 字左右，含实测数据） |
| 3 | [`03-分享PPT.pptx`](03-分享PPT.pptx) | 提交物 4：5 分钟分享 PPT（10 页，可现场操作） |
| 4 | [`screenshots/`](screenshots/) | 提交物 2：功能验证截图（**6 张，全部为本机真机实拍**） |
| 5 | [`assets/环境快照.md`](assets/环境快照.md) | 环境取证记录，答辩被问「你怎么证明」时直接翻这份 |

## 三、截图（已补齐，全部真机实拍）

6 张图都是在 `G:\PycharmProjects` 这台机器上现场跑出来的，没有一张是示意图或合成图：

| 文件名 | 画面 | 出处 |
| --- | --- | --- |
| `01-pycharm-plugins.png` | PyCharm「插件 → 已安装」：CC GUI 0.5.7 + Comate 4.14.0 + Copilot 1.17.0 + Qoder CN 同屏 | `Ctrl+Alt+S` |
| `02-api-config.png` | `settings.json` 的 `env` 段：端点、模型别名（**token 已打码为 `sk-•••`**） | 脱敏副本在记事本中放大 |
| `03-dialog-explain.png` | 面板内「第一部分：导入包（import）」逐条解释 numpy / matplotlib / sklearn | CC GUI 工具窗口 |
| `04-completion-test.png` | Agent 生成 `test_kmeans.py`，以 **diff 审查视图**回填 IDE（拒绝 / 始终应用 / 应用） | 面板派活后自动弹出 |
| `05-agent-task.png` | 首跑失败 → 判定"断言 0.99 不可达" → 改 0.95 并加注释 → 重跑 | 同上，任务继续 |
| `06-agent-summary.png` | 收尾总结 + 本次扣费口径：耗时 7:47、输入 527.5k / 输出 8.3k | 同上，任务结束 |

> 想替换成自己重拍的版本，直接覆盖同名文件即可，手册与 PPT 会按文件名自动对上（PPT 需重跑 `tools/make_ppt.py` 重新嵌图）。

## 四、提交到 GitHub

已推送至：**https://github.com/WOSHIGAOSHOU296/pycharm-ai-coding-assistant-lab**（**私有**仓库）。

设为私有的原因：包内含姓名、学号与真实配置画面，公开前请自行确认。要交给老师看，两条路：

- 仓库页 `Settings → General → Danger Zone → Change visibility → Make public`（一键转公开）；
- 或者 `Settings → Collaborators → Add people` 把老师账号加为协作者（保持私有）。

后续改动再推：

```bash
cd "D:\deep seek\workplace\PyCharm-AI编程助手实训"
git add . && git commit -m "docs: 更新截图"
git push
```

> 本机凭据来自 Git Credential Manager（账号 `WOSHIGAOSHOU296`），HTTPS 推送免密；SSH 亦可（`~/.ssh/id_ed25519` 已验证）。

## 五、安全提示

- `.claude/settings.json` 里的 `ANTHROPIC_AUTH_TOKEN`（`sk-****…`）是**真实密钥**，交付包内一律以 `sk-****（已脱敏）` 呈现；截图时务必打码，不要把这个仓库设成公开后带着密钥。
- 仓库已带 `.gitignore`，排除截图原图缓存与临时文件。
