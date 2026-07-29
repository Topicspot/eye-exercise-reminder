# Eye Exercise Reminder

[English](../README.md) · [Русский](README.ru.md) · **简体中文** · [Español](README.es.md) · [Português](README.pt-BR.md)

**Eye Exercise Reminder** 是一款基于 Python 和 PyQt6 的轻量级 Windows 桌面悬浮窗应用。
它会定期提醒你做眼保健操，帮助减轻长时间面对屏幕造成的眼睛疲劳。

提醒以置顶悬浮窗的形式出现，显示一张护眼操示意图。应用完全可配置，支持 12 种语言，
并且可以在无控制台窗口的静默模式下启动。

## 功能

| 功能 | 说明 |
|---|---|
| 可配置间隔 | 提醒间隔可设置为 1 到 180 分钟 |
| 稍后提醒 | 将提醒推迟固定的分钟数 |
| 12 种语言 | EN、UK、RU、DE、ES、FR、IT、ZH、JA、PL、PT、TR |
| 设置持久化 | 语言偏好保存在本地 JSON 文件中 |
| 置顶显示 | 悬浮窗始终位于其他窗口之上 |
| 可拖动 | 悬浮窗可移动到屏幕任意位置 |
| 静默启动 | 通过 `start.pyw` 启动，无控制台窗口 |

## 安装与运行

需要 Python 3.11+，唯一的第三方依赖是 PyQt6。

```bash
git clone https://github.com/Topicspot/eye-exercise-reminder.git
cd eye-exercise-reminder
pip install PyQt6
python eye_reminder.py    # 带控制台输出运行
pythonw start.pyw         # 静默运行（仅 Windows）
```

护眼操示意图（默认 `eye_exercises.png`）需与 `eye_reminder.py` 放在同一目录。

完整文档（配置、隐私说明、故障排查）见[英文 README](../README.md)。

## 许可证

MIT。
