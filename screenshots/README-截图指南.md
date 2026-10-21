# 截图指南（5 张占位图 → 真机替换）

`screenshots/` 里现在放的是 5 张**占位图**（灰底、写着"待补真实截图"）。它们只是为了让手册和 PPT 的版式先跑通，**必须用真机截图覆盖同名文件**才算完成提交物。

## 一、拍哪 5 张

| 文件名 | 拍什么 | 对应提交物 |
| --- | --- | --- |
| `01-pycharm-plugins.png` | PyCharm `Settings → Plugins → Installed` 列表，能看清 Claude Code 已启用（对照组的 Comate / Copilot 也入镜更好） | 手册第 3 章「安装步骤」配图 |
| `02-api-config.png` | `settings.json` 的 `env` 段，或用记事本打开配置文件的画面；**token 必须打码** | 手册第 4 章「配置步骤」 |
| `03-dialog-explain.png` | Claude Code 面板里提问 test.py、截到解释正文 | 验证截图 1（对话） |
| `04-completion-test.png` | 行内补全的 ghost text，**或** Agent 生成的 pytest 用例 + 运行结果 | 验证截图 2（补全/测试生成） |
| `05-agent-task.png` | 面板时间线里同时出现 Bash / Read / Edit 之类工具调用 | 验证截图 3（Agent 任务） |

## 二、怎么拍才"可复现"

- **窗口宽度 ≥ 1200px**，否则文字截图后糊成一片，手册里看不清字。
- 截**整个 PyCharm 窗口**，别只截中间那块 —— 别人要靠左侧工程树、顶部文件名判断你在哪个文件里操作。
- 涉及密钥/路径的图，用画图工具涂黑，别让 `sk-` 开头的串进仓库。
- 统一用 PNG，文件名一字不改（手册和 PPT 都是按名字引用的）。

## 三、拍完怎么让它生效

1. **手册**：把图拖进 `01-操作指南手册.md` 对应位置（`![图 1 · ...](screenshots/01-pycharm-plugins.png)` 这样的引用已经写好了，覆盖文件即自动生效）。
2. **PPT**：图片是构建时嵌入的，需要重跑一次脚本刷新：

```powershell
& "D:\deep seek\harness\DSH Desktop\resources\office-runtime\primary-runtime\dependencies\python\python.exe" tools\make_ppt.py
```

3. 若只改了某几张，重跑也无妨 —— 脚本每次整份重建，10 页版式是确定的。

## 四、占位图本身怎么重新生成

```powershell
& "<同一个 python>" tools\make_screenshots.py
```

会把 5 张灰底占位图重新画一遍（**会覆盖你拍好的真图**，拍完就别再跑了）。
