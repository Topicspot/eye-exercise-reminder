```markdown
# Eye Exercise Reminder 👁

> **This README is written in two languages: English first, Russian second.**
> **Этот README написан на двух языках: сначала английский, затем русский.**

---

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.x-green?logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🇬🇧 English

### Overview

**Eye Exercise Reminder** is a lightweight desktop overlay application for Windows built with Python and PyQt6. It periodically reminds you to perform eye exercises, helping to reduce eye strain during long screen sessions.

The reminder appears as a floating, always-on-top overlay window that displays an exercise instruction image. It is fully configurable, supports 12 languages, and can be launched silently without a console window.

---

### ✨ Features

| Feature | Details |
|---|---|
| ⏱ Configurable interval | Set the reminder from 1 to 180 minutes |
| 🕒 Snooze | Postpone the reminder by a fixed number of minutes |
| 🌐 12 languages | EN, UK, RU, DE, ES, FR, IT, ZH, JA, PL, PT, TR |
| 💾 Persistent settings | Language preference saved locally in JSON |
| 🖼 Exercise image | Displays a local image file with eye exercise instructions |
| 🎨 Neon/Cyberpunk UI | Dark-themed, animated overlay with glassmorphism effect |
| 🔇 Silent launcher | Run without a console window using `start.pyw` |
| 📌 Always on top | The overlay stays above all other windows |
| 🖱 Draggable | Move the overlay anywhere on screen |
| 🔒 Screen-capture exclusion | On Windows 10 (2004+), attempts to hide the window from screen capture tools *(see Notes)* |

---

### 📋 Requirements

- **Python** 3.11 or newer
- **PyQt6**

```bash
pip install PyQt6
```

> No other third-party packages are required.

---

### 📦 Installation

1. **Clone or download** the repository:

```bash
git clone https://github.com/your-username/eye-reminder.git
cd eye-reminder
```

2. **Install the dependency:**

```bash
pip install PyQt6
```

3. **Place your exercise image** in the same folder as `eye_reminder.py`.  
   The default expected filename is `eye_exercises.png`.  
   You can change this in the constants at the top of `eye_reminder.py`.

---

### ▶ How to Run

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

---

### ⚙ Configuration

All configuration happens at startup through the **Setup Window** that appears when you first launch the app.

| Setting | How to change |
|---|---|
| **Reminder interval** | Use the `‹` / `›` picker or click a quick-pick button (1, 5, 10, 15, 20, 30, 45, 60 min) |
| **Language** | Click the `▶ 🌐 Language` toggle in the bottom bar to expand the selector |
| **Snooze duration** | Fixed at `SNOOZE_MINUTES = 3` in the source file |
| **Image file** | Set `IMAGE_PATH` at the top of `eye_reminder.py` |
| **Default interval** | Set `DEFAULT_INTERVAL` at the top of `eye_reminder.py` |

The selected language is automatically saved to `eye_reminder_settings.json` and restored on next launch.

---

### 📁 File Structure

```
eye-reminder/
├── eye_reminder.py              # Main application (all logic and UI)
├── start.pyw                    # Silent launcher for Windows (no console)
├── eye_exercises.png            # Exercise instruction image (required)
├── eye_reminder_settings.json   # Auto-generated on first run; stores language
└── README.md                    # This file
```

> `eye_reminder_settings.json` is created automatically. You do not need to create it manually.

---

### 🖼 Screenshots

> *(Screenshots will be added here. Contributions welcome.)*

| Setup Window | Reminder Popup |
|---|---|
| ![Setup Window](docs/screenshots/setup_window.png) | ![Reminder Popup](docs/screenshots/reminder_popup.png) |

*Placeholder — actual screenshots not yet included in this repository.*

---

### 🔒 Privacy & Security

- **Local only.** Based on the source code, this application does not make any network requests and does not transmit data to any server.
- **Settings storage.** The only file written to disk is `eye_reminder_settings.json`, which stores your selected language code only.
- **No analytics.** There is no telemetry, crash reporting, or usage tracking of any kind.

---

### 📝 Notes & Disclaimer

#### Screen-Capture Exclusion (Windows)

When running on Windows, the application calls `SetWindowDisplayAffinity` with the `WDA_EXCLUDEFROMCAPTURE` flag. According to Microsoft documentation, this is intended to prevent a window from appearing in screen captures and recordings.

**Important caveats:**

- This feature requires **Windows 10 version 2004 or later**. On older versions of Windows, the call may have no effect or behave differently.
- Effectiveness may vary depending on the screen-capture software or method used.
- This feature is provided on a best-effort basis. **The application does not guarantee complete invisibility in all capture scenarios.**
- If the Windows API call fails (e.g., due to permissions or OS version), the app continues to work normally — stealth is treated as optional.

#### Fonts

The application uses `Segoe UI` and `Consolas`, which are standard Windows fonts. On non-Windows systems these may fall back to system defaults, potentially affecting the visual appearance.

---

### 🛠 Troubleshooting

**The window doesn't appear after the interval:**
- Make sure you pressed **Start Reminder** in the Setup Window.
- Check the console output if you launched with `python eye_reminder.py` — it logs each timer event.

**The image is not displayed:**
- Verify that `eye_exercises.png` (or your custom filename) exists in the same directory as `eye_reminder.py`.
- Check that `IMAGE_PATH` at the top of the script matches your filename exactly.

**The app crashes when changing language:**
- Ensure you are using the latest version of this file — an earlier version had a known bug with layout teardown on language change that has since been fixed.

**Silent launch doesn't work:**
- `start.pyw` requires `pythonw.exe` to be on your PATH, which is included in a standard Python for Windows installation.
- Try running `pythonw start.pyw` from the command line first to check for errors.

**Screen-capture exclusion is not working:**
- This feature requires Windows 10 version 2004 or later.
- Some capture tools may not be affected by `WDA_EXCLUDEFROMCAPTURE`. This is a known OS-level limitation.

---

### 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 **Report bugs** by opening an Issue
- 🌍 **Improve translations** for existing languages
- ➕ **Add a new language** by adding an entry to the `LANGS` dictionary in `eye_reminder.py`
- 🖼 **Add real screenshots** to the `docs/screenshots/` folder
- 💡 **Suggest features** via Issues or Discussions

Please keep pull requests focused on a single change and include a clear description.

---

### 📄 License

This project is released under the **MIT License**.

> A `LICENSE` file has not yet been added to this repository. If you intend to use or distribute this software, please check with the author or add a `LICENSE` file before publishing.

---

---

## 🇷🇺 Русский

### Обзор

**Eye Exercise Reminder** — это лёгкое настольное приложение-оверлей для Windows, созданное на Python и PyQt6. Оно периодически напоминает вам о необходимости выполнять упражнения для глаз, помогая снизить усталость при длительной работе за экраном.

Напоминание появляется в виде плавающего окна поверх всех остальных окон и отображает изображение с инструкциями по упражнениям. Приложение полностью настраиваемо, поддерживает 12 языков и может запускаться в тихом режиме — без окна консоли.

---

### ✨ Возможности

| Функция | Описание |
|---|---|
| ⏱ Настраиваемый интервал | Установка напоминания от 1 до 180 минут |
| 🕒 Отложить | Перенос напоминания на фиксированное количество минут |
| 🌐 12 языков | EN, UK, RU, DE, ES, FR, IT, ZH, JA, PL, PT, TR |
| 💾 Сохранение настроек | Выбранный язык сохраняется локально в JSON-файле |
| 🖼 Изображение упражнений | Отображает локальный файл с инструкциями по упражнениям |
| 🎨 Неон/Киберпанк интерфейс | Тёмная тема, анимированный оверлей с эффектом стекла |
| 🔇 Тихий запуск | Запуск без окна консоли через `start.pyw` |
| 📌 Поверх всех окон | Оверлей всегда отображается поверх других окон |
| 🖱 Перетаскивание | Окно можно переместить в любое место экрана |
| 🔒 Скрытие при захвате экрана | На Windows 10 (2004+) предпринимается попытка скрыть окно от инструментов захвата экрана *(см. Примечания)* |

---

### 📋 Требования

- **Python** версии 3.11 или новее
- **PyQt6**

```bash
pip install PyQt6
```

> Никаких других сторонних пакетов не требуется.

---

### 📦 Установка

1. **Клонируйте или скачайте** репозиторий:

```bash
git clone https://github.com/your-username/eye-reminder.git
cd eye-reminder
```

2. **Установите зависимость:**

```bash
pip install PyQt6
```

3. **Поместите изображение упражнений** в ту же папку, что и `eye_reminder.py`.  
   По умолчанию ожидается файл с именем `eye_exercises.png`.  
   Имя файла можно изменить в константах в начале `eye_reminder.py`.

---

### ▶ Запуск

**С выводом в консоль** (рекомендуется при первом запуске или для отладки):

```bash
python eye_reminder.py
```

**В тихом режиме, без окна консоли** (только Windows):

```bash
pythonw start.pyw
```

> `start.pyw` — минимальный скрипт-запускатор. На Windows файлы с расширением `.pyw` выполняются через `pythonw.exe`, что полностью подавляет окно консоли.

#### Автозапуск вместе с Windows

Чтобы приложение запускалось автоматически при входе в систему:

1. Нажмите `Win + R`, введите `shell:startup` и нажмите Enter.
2. Создайте ярлык на файл `start.pyw` в открывшейся папке.

---

### ⚙ Настройка

Все настройки выполняются при запуске через **окно настройки**, которое появляется при первом запуске приложения.

| Настройка | Как изменить |
|---|---|
| **Интервал напоминания** | Кнопки `‹` / `›` или кнопки быстрого выбора (1, 5, 10, 15, 20, 30, 45, 60 мин) |
| **Язык** | Нажмите `▶ 🌐 Язык` в нижней панели для открытия списка языков |
| **Длительность отсрочки** | Фиксируется в `SNOOZE_MINUTES = 3` в исходном коде |
| **Файл изображения** | Задаётся в `IMAGE_PATH` в начале `eye_reminder.py` |
| **Интервал по умолчанию** | Задаётся в `DEFAULT_INTERVAL` в начале `eye_reminder.py` |

Выбранный язык автоматически сохраняется в `eye_reminder_settings.json` и восстанавливается при следующем запуске.

---

### 📁 Структура файлов

```
eye-reminder/
├── eye_reminder.py              # Основное приложение (вся логика и интерфейс)
├── start.pyw                    # Тихий запускатор для Windows (без консоли)
├── eye_exercises.png            # Изображение с упражнениями (обязательно)
├── eye_reminder_settings.json   # Создаётся автоматически; хранит язык
└── README.md                    # Этот файл
```

> Файл `eye_reminder_settings.json` создаётся автоматически. Создавать его вручную не нужно.

---

### 🖼 Скриншоты

> *(Скриншоты будут добавлены здесь. Приветствуются вклады.)*

| Окно настройки | Окно напоминания |
|---|---|
| ![Окно настройки](docs/screenshots/setup_window.png) | ![Окно напоминания](docs/screenshots/reminder_popup.png) |

*Заглушка — реальные скриншоты пока не добавлены в репозиторий.*

---

### 🔒 Конфиденциальность и безопасность

- **Только локально.** На основании исходного кода приложение не выполняет сетевых запросов и не передаёт никакие данные на серверы.
- **Хранение настроек.** Единственный файл, записываемый на диск, — `eye_reminder_settings.json`. В нём хранится только код выбранного языка.
- **Без аналитики.** Приложение не содержит телеметрии, отчётов об ошибках или отслеживания использования.

---

### 📝 Примечания и отказ от ответственности

#### Скрытие при захвате экрана (Windows)

При запуске на Windows приложение вызывает `SetWindowDisplayAffinity` с флагом `WDA_EXCLUDEFROMCAPTURE`. Согласно документации Microsoft, этот флаг предназначен для того, чтобы предотвратить появление окна на скриншотах и в записях экрана.

**Важные оговорки:**

- Функция требует **Windows 10 версии 2004 или новее**. На более старых версиях вызов может не иметь эффекта или работать иначе.
- Эффективность зависит от используемого программного обеспечения для захвата экрана.
- Функция реализована по принципу «лучших усилий». **Приложение не гарантирует полную невидимость во всех сценариях захвата.**
- Если вызов Windows API не удаётся (например, из-за разрешений или версии ОС), приложение продолжает работать в обычном режиме — скрытие является необязательной функцией.

#### Шрифты

Приложение использует `Segoe UI` и `Consolas` — стандартные шрифты Windows. На других операционных системах они могут быть заменены системными шрифтами по умолчанию, что может повлиять на внешний вид интерфейса.

---

### 🛠 Устранение неполадок

**Окно не появляется после истечения интервала:**
- Убедитесь, что вы нажали кнопку **Запустить напоминалку** в окне настройки.
- Проверьте вывод консоли при запуске через `python eye_reminder.py` — каждое событие таймера записывается в лог.

**Изображение не отображается:**
- Убедитесь, что файл `eye_exercises.png` (или ваш пользовательский файл) находится в той же папке, что и `eye_reminder.py`.
- Проверьте, что значение `IMAGE_PATH` в начале скрипта совпадает с именем вашего файла.

**Приложение падает при смене языка:**
- Убедитесь, что вы используете последнюю версию файла — в более ранней версии была известная ошибка при перестройке интерфейса после смены языка, которая была исправлена.

**Тихий запуск не работает:**
- Для `start.pyw` требуется, чтобы `pythonw.exe` был доступен через PATH. Он включён в стандартную установку Python для Windows.
- Сначала попробуйте запустить `pythonw start.pyw` из командной строки для проверки ошибок.

**Скрытие при захвате экрана не работает:**
- Эта функция требует Windows 10 версии 2004 или новее.
- Некоторые инструменты захвата могут не реагировать на флаг `WDA_EXCLUDEFROMCAPTURE`. Это известное ограничение на уровне операционной системы.

---

### 🤝 Участие в разработке

Вклад в проект приветствуется! Вот несколько способов помочь:

- 🐛 **Сообщайте об ошибках**, открывая Issue
- 🌍 **Улучшайте переводы** для существующих языков
- ➕ **Добавляйте новые языки**, добавив запись в словарь `LANGS` в `eye_reminder.py`
- 🖼 **Добавляйте скриншоты** в папку `docs/screenshots/`
- 💡 **Предлагайте функции** через Issues или Discussions

Пожалуйста, делайте pull request сфокусированными на одном изменении и включайте понятное описание.

---

### 📄 Лицензия

Этот проект распространяется под лицензией **MIT**.

> Файл `LICENSE` ещё не добавлен в репозиторий. Если вы планируете использовать или распространять это программное обеспечение, пожалуйста, уточните у автора или добавьте файл `LICENSE` перед публикацией.
```