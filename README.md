# Eye Exercise Reminder

**English** · [Русский](docs/README.ru.md) · [简体中文](docs/README.zh-CN.md) · [Español](docs/README.es.md) · [Português](docs/README.pt-BR.md)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.x-green?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

**Eye Exercise Reminder** is a lightweight desktop overlay application for Windows built with Python and PyQt6. It periodically reminds you to perform eye exercises, helping to reduce eye strain during long screen sessions.

The reminder appears as a floating, always-on-top overlay window that displays an exercise instruction image. It is fully configurable, supports 12 languages, and can be launched silently without a console window.

## Features

| Feature | Details |
|---|---|
| Configurable interval | Set the reminder from 1 to 180 minutes |
| Snooze | Postpone the reminder by a fixed number of minutes |
| 12 languages | EN, UK, RU, DE, ES, FR, IT, ZH, JA, PL, PT, TR |
| Persistent settings | Language preference saved locally in JSON |
| Exercise image | Displays a local image file with eye exercise instructions |
| Neon/Cyberpunk UI | Dark-themed, animated overlay with glassmorphism effect |
| Silent launcher | Run without a console window using `start.pyw` |
| Always on top | The overlay stays above all other windows |
| Draggable | Move the overlay anywhere on screen |
| Screen-capture exclusion | On Windows 10 (2004+), attempts to hide the window from screen capture tools *(see Notes)* |

## Requirements

- **Python** 3.11 or newer
- **PyQt6**

```bash
pip install PyQt6
```

> No other third-party packages are required.

## Installation

1. **Clone or download** the repository:

```bash
git clone https://github.com/Topicspot/eye-exercise-reminder.git
cd eye-exercise-reminder
```

2. **Install the dependency:**

```bash
pip install PyQt6
```

3. **Place your exercise image** in the same folder as `eye_reminder.py`.  
   The default expected filename is `eye_exercises.png`.  
   You can change this in the constants at the top of `eye_reminder.py`.

## How to Run

**With console output** (recommended for first run / debugging):

```bash
python eye_reminder.py
```

**Silently, without a console window** (Windows only):

```bash
pythonw start.pyw
```

> `start.pyw` is a minimal launcher script. On Windows, files with the `.pyw` extension are executed by `pythonw.exe`, which suppresses the console window entirely.

#### Auto-start with Windows

To launch the app automatically when Windows starts:

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Create a shortcut to `start.pyw` in the folder that opens.

## Configuration

All configuration happens at startup through the **Setup Window** that appears when you first launch the app.

| Setting | How to change |
|---|---|
| **Reminder interval** | Use the `‹` / `›` picker or click a quick-pick button (1, 5, 10, 15, 20, 30, 45, 60 min) |
| **Language** | Click the `▶ 🌐 Language` toggle in the bottom bar to expand the selector |
| **Snooze duration** | Fixed at `SNOOZE_MINUTES = 3` in the source file |
| **Image file** | Set `IMAGE_PATH` at the top of `eye_reminder.py` |
| **Default interval** | Set `DEFAULT_INTERVAL` at the top of `eye_reminder.py` |

The selected language is automatically saved to `eye_reminder_settings.json` and restored on next launch.

## File Structure

```
eye-exercise-reminder/
├── eye_reminder.py              # Main application (all logic and UI)
├── start.pyw                    # Silent launcher for Windows (no console)
├── eye_exercises.png            # Exercise instruction image (required)
├── eye_reminder_settings.json   # Auto-generated on first run; stores language
└── README.md                    # This file
```

> `eye_reminder_settings.json` is created automatically. You do not need to create it manually.

## Privacy & Security

- **Local only.** Based on the source code, this application does not make any network requests and does not transmit data to any server.
- **Settings storage.** The only file written to disk is `eye_reminder_settings.json`, which stores your selected language code only.
- **No analytics.** There is no telemetry, crash reporting, or usage tracking of any kind.

## Notes & Disclaimer

#### Screen-Capture Exclusion (Windows)

When running on Windows, the application calls `SetWindowDisplayAffinity` with the `WDA_EXCLUDEFROMCAPTURE` flag. According to Microsoft documentation, this is intended to prevent a window from appearing in screen captures and recordings.

**Important caveats:**

- This feature requires **Windows 10 version 2004 or later**. On older versions of Windows, the call may have no effect or behave differently.
- Effectiveness may vary depending on the screen-capture software or method used.
- This feature is provided on a best-effort basis. **The application does not guarantee complete invisibility in all capture scenarios.**
- If the Windows API call fails (e.g., due to permissions or OS version), the app continues to work normally; stealth is treated as optional.

#### Fonts

The application uses `Segoe UI` and `Consolas`, which are standard Windows fonts. On non-Windows systems these may fall back to system defaults, potentially affecting the visual appearance.

## Troubleshooting

**The window doesn't appear after the interval:**
- Make sure you pressed **Start Reminder** in the Setup Window.
- Check the console output if you launched with `python eye_reminder.py`; it logs each timer event.

**The image is not displayed:**
- Verify that `eye_exercises.png` (or your custom filename) exists in the same directory as `eye_reminder.py`.
- Check that `IMAGE_PATH` at the top of the script matches your filename exactly.

**The app crashes when changing language:**
- Ensure you are using the latest version of this file: an earlier version had a known bug with layout teardown on language change that has since been fixed.

**Silent launch doesn't work:**
- `start.pyw` requires `pythonw.exe` to be on your PATH, which is included in a standard Python for Windows installation.
- Try running `pythonw start.pyw` from the command line first to check for errors.

**Screen-capture exclusion is not working:**
- This feature requires Windows 10 version 2004 or later.
- Some capture tools may not be affected by `WDA_EXCLUDEFROMCAPTURE`. This is a known OS-level limitation.

## Contributing

Contributions are welcome! Here are some ways you can help:

- **Report bugs** by opening an Issue
- **Improve translations** for existing languages
- **Add a new language** by adding an entry to the `LANGS` dictionary in `eye_reminder.py`
- **Add real screenshots** to the `docs/screenshots/` folder
- **Suggest features** via Issues or Discussions

Please keep pull requests focused on a single change and include a clear description.

## License

This project is released under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the full text.

---

## ☕ Support the author

This project is free and MIT-licensed. If it saved you time, you can send a coffee.

**USDT, Tron network (TRC-20) only:**

```
TS9ywGeSyKQxiCszdKCHLR8DRAsnYCosNN
```

<details>
<summary>Другие языки / Other languages</summary>

- **Українська:** проєкт безкоштовний. Якщо він заощадив вам час — можна підтримати автора,
  USDT у мережі Tron (TRC-20), адреса вище.
- **Русский:** проект бесплатный. Если он сэкономил вам время, можно поддержать автора,
  USDT в сети Tron (TRC-20), адрес выше.

</details>
