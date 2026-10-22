# 截图说明（6 张，全部真机实拍）

`screenshots/` 里现在放的是 **6 张真机截图**，全部在 `G:\PycharmProjects` 上用 PyCharm 2026.2.2 现场跑出来，没有示意图、没有合成图。

## 一、每张图是怎么来的

| 文件名 | 画面内容 | 怎么出的 |
| --- | --- | --- |
| `01-pycharm-plugins.png` | `设置 → 插件 → 已安装`：CC GUI (Claude Code, Codex and More) 0.5.7、Baidu Comate 4.14.0、GitHub Copilot 1.17.0、Qoder CN 2026.924 同屏，全部勾选启用 | `Ctrl+Alt+S` 直接落在插件页，选中 CC GUI 行后右侧详情显示 "Multi-engine GUI for Claude Code, Codex, OpenCode & more" |
| `02-api-config.png` | `settings.json` 的 `env` 段：`ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`，`ANTHROPIC_MODEL` / `DEFAULT_HAIKU` / `DEFAULT_OPUS` / `DEFAULT_SONNET` 四个别名全部 `deepseek-flash`；token 行显示为 `sk-••••` | 读真实配置 → 正则把 `sk-[A-Za-z0-9_\-]{8,}` 替换成圆点 → 脱敏副本写到临时目录再用记事本打开，注意**真实文件没被改动** |
| `03-dialog-explain.png` | CC GUI 面板里「第一部分：导入包（import）」逐条解释 numpy / matplotlib / sklearn / KMeans，左侧是 test.py | `Ctrl+Shift+A` → 输入 `CC GUI` → Enter 打开工具窗口 |
| `04-completion-test.png` | Agent 把生成的 `test_kmeans.py` 以 **diff 审查视图**回填：左「新文件」右「建议版本」，底部 `拒绝 / 始终应用 / 应用` | 面板派活："为 test.py 生成一份 pytest 用例，写到 test_kmeans.py，然后运行它；有失败就修到通过" |
| `05-agent-task.png` | 首跑失败后的诊断：`cluster_std=0.4` 与邻簇重叠 → ARI 上限只有 0.973 → 断言 0.99 不可达 → 改成 0.95 并加注释 | 同一次任务继续执行 |
| `06-agent-summary.png` | 收尾总结（含"`import inline` 不是标准库"的判断）+ 右下角「本次耗时 7:47 · 输入 527.5k / 输出 8.3k」 | 任务结束时的最终回答 |

## 二、复核这次任务的真实性

不看截图也能核：

- `G:\PycharmProjects\test_kmeans.py`（70 行，2026-10-22 17:32 生成）；
- `G:\PycharmProjects\.pytest_cache\v\cache\nodeids` 里有 8 条用例 id，`lastfailed` 内容为 `{}` —— 最后一次运行全过；
- `G:\PycharmProjects\test.py` 的修改时间仍是 2026-09-28，说明 Agent 说的"test.py 本身未改动"是真的。

## 三、要替换成自己重拍的版本

直接覆盖同名文件即可，手册按文件名引用；PPT 是构建时嵌图的，需要重跑一次：

```powershell
& "D:\deep seek\harness\DSH Desktop\resources\office-runtime\primary-runtime\dependencies\python\python.exe" tools\make_ppt.py
```

> 旧的 `README-截图指南.md`（占位图时代的指引）与 `tools/make_screenshots.py`（生成灰底占位图）保留在仓库里作历史，但**不要再跑 `make_screenshots.py`**，它会覆盖上面这 6 张真图。
