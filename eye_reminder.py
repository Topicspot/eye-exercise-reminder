"""
Eye Exercise Reminder  v6.0
===========================
Reminds you to do eye exercises at a configurable interval.
The overlay window is invisible to screen-capture software
(Google Meet, Zoom, Teams, OBS) on Windows.

Requirements:
    pip install PyQt6

Usage:
    python eye_reminder.py        # with console log
    pythonw start.pyw             # silent, no console window
"""

# ── User-configurable constants ───────────────────────────────────────────────
DEFAULT_INTERVAL: int = 20       # minutes between reminders
SNOOZE_MINUTES: int   = 3        # minutes for "remind me later"
IMAGE_PATH: str       = "eye_exercises.png"   # relative to this script
SETTINGS_FILE: str    = "eye_reminder_settings.json"

# ── Colour palette (neon/cyberpunk dark theme) ────────────────────────────────
PALETTE: dict = {
    # Glass card background (RGBA tuples used by QPainter)
    "glass_top":  (8,   11,  28,  230),
    "glass_bot":  (14,  20,  48,  210),
    "border":     (70, 140, 255,   50),
    "glow":       (70, 140, 255,   22),
    # CSS colour strings
    "text":       "#dde6ff",
    "subtext":    "#6a7fa8",
    "dim":        "#2e3d58",
    "accent":     "#4fc3f7",
    "accent2":    "#81d4fa",
    # Action buttons
    "btn_ok":     "#1565d8",
    "btn_ok_hv":  "#1976f5",
    "btn_sn":     "#162236",
    "btn_sn_hv":  "#1e3450",
    "btn_sn_brd": "#263a58",
    # Language chip colours
    "chip":       "rgba(70,140,255,0.10)",
    "chip_hv":    "rgba(70,140,255,0.26)",
    "chip_sel":   "rgba(70,140,255,0.42)",
    "chip_brd":   "rgba(70,140,255,0.28)",
    # Misc
    "separator":  "rgba(70,140,255,0.16)",
    "picker_bg":  "rgba(10,16,40,0.95)",
}

# Short alias used in CSS f-strings throughout this file
C = PALETTE

# ── Font names (safe on all Windows versions) ─────────────────────────────────
FONT_SANS: str = "Segoe UI"
FONT_MONO: str = "Consolas"
CARD_RADIUS: int = 24   # global window corner radius in px

# ══════════════════════════════════════════════════════════════════════════════
# Translations  (12 languages)
# ══════════════════════════════════════════════════════════════════════════════
LANGS: dict = {
    "en": {
        "name": "English",       "flag": "EN",
        "title": "Eye Exercise Reminder",
        "sub":   "Set interval, then Start",
        "every": "Remind every",  "suffix": " min",    "quick": "Quick:",
        "start": "Start Reminder",
        "ok":    "OK",            "snooze": "Remind in {n} min",
        "drag":  "drag",          "no_img": "Image not found:\n{p}",
        "exit_tip": "Turn off program",
    },
    "uk": {
        "name": "Українська",    "flag": "UA",
        "title": "Нагадування для очей",
        "sub":   "Вибери інтервал і натисни Запустити",
        "every": "Нагадувати кожні", "suffix": " хв",  "quick": "Швидко:",
        "start": "Запустити нагадування",
        "ok":    "Окей",          "snooze": "Нагадати через {n} хв",
        "drag":  "тягни",         "no_img": "Файл не знайдено:\n{p}",
        "exit_tip": "Вимкнути програму",
    },
    "ru": {
        "name": "Русский",       "flag": "RU",
        "title": "Зарядка для глаз",
        "sub":   "Выбери интервал и нажми Запустить",
        "every": "Напоминать каждые", "suffix": " мин", "quick": "Быстро:",
        "start": "Запустить напоминалку",
        "ok":    "Окей",          "snooze": "Напомнить через {n} мин",
        "drag":  "тяни",          "no_img": "Файл не найден:\n{p}",
        "exit_tip": "Выключить программу",
    },
    "de": {
        "name": "Deutsch",       "flag": "DE",
        "title": "Augenübungs-Erinnerung",
        "sub":   "Intervall wählen, dann Starten",
        "every": "Erinnere alle", "suffix": " Min",    "quick": "Schnell:",
        "start": "Erinnerung starten",
        "ok":    "OK",            "snooze": "Erinnere in {n} Min",
        "drag":  "ziehen",        "no_img": "Datei fehlt:\n{p}",
        "exit_tip": "Programm beenden",
    },
    "es": {
        "name": "Español",       "flag": "ES",
        "title": "Recordatorio ocular",
        "sub":   "Elige intervalo y pulsa Iniciar",
        "every": "Recordar cada", "suffix": " min",    "quick": "Rápido:",
        "start": "Iniciar recordatorio",
        "ok":    "OK",            "snooze": "Recordar en {n} min",
        "drag":  "arrastrar",     "no_img": "Archivo no encontrado:\n{p}",
        "exit_tip": "Cerrar programa",
    },
    "fr": {
        "name": "Français",      "flag": "FR",
        "title": "Rappel exercices oculaires",
        "sub":   "Choisissez l'intervalle et Démarrez",
        "every": "Rappeler toutes les", "suffix": " min", "quick": "Vite:",
        "start": "Démarrer rappel",
        "ok":    "OK",            "snooze": "Rappel dans {n} min",
        "drag":  "glisser",       "no_img": "Fichier introuvable:\n{p}",
        "exit_tip": "Quitter le programme",
    },
    "it": {
        "name": "Italiano",      "flag": "IT",
        "title": "Promemoria esercizi oculari",
        "sub":   "Scegli intervallo e premi Avvia",
        "every": "Ricorda ogni",  "suffix": " min",    "quick": "Rapido:",
        "start": "Avvia promemoria",
        "ok":    "OK",            "snooze": "Ricorda tra {n} min",
        "drag":  "trascina",      "no_img": "File non trovato:\n{p}",
        "exit_tip": "Chiudi programma",
    },
    "zh": {
        "name": "中文",           "flag": "ZH",
        "title": "眼部锻炼提醒",
        "sub":   "设置间隔，然后开始",
        "every": "每隔",          "suffix": " 分钟",   "quick": "快速:",
        "start": "启动提醒",
        "ok":    "好的",          "snooze": "{n} 分钟后提醒",
        "drag":  "拖动",          "no_img": "图片未找到:\n{p}",
        "exit_tip": "关闭程序",
    },
    "ja": {
        "name": "日本語",         "flag": "JA",
        "title": "目のエクササイズ",
        "sub":   "間隔を設定してスタート",
        "every": "毎",            "suffix": " 分ごと", "quick": "クイック:",
        "start": "スタート",
        "ok":    "OK",            "snooze": "{n} 分後に通知",
        "drag":  "ドラッグ",      "no_img": "ファイル未検出:\n{p}",
        "exit_tip": "終了",
    },
    "pl": {
        "name": "Polski",        "flag": "PL",
        "title": "Przypomnienie o oczach",
        "sub":   "Wybierz interwał i uruchom",
        "every": "Przypomnij co", "suffix": " min",    "quick": "Szybko:",
        "start": "Uruchom przypomnienie",
        "ok":    "OK",            "snooze": "Przypomnij za {n} min",
        "drag":  "przeciągnij",   "no_img": "Plik nie znaleziony:\n{p}",
        "exit_tip": "Zamknij program",
    },
    "pt": {
        "name": "Português",     "flag": "PT",
        "title": "Lembrete de exercícios",
        "sub":   "Escolha intervalo e pressione Iniciar",
        "every": "Lembrar a cada", "suffix": " min",   "quick": "Rápido:",
        "start": "Iniciar lembrete",
        "ok":    "OK",            "snooze": "Lembrar em {n} min",
        "drag":  "arrastar",      "no_img": "Arquivo não encontrado:\n{p}",
        "exit_tip": "Fechar programa",
    },
    "tr": {
        "name": "Türkçe",        "flag": "TR",
        "title": "Göz Egzersizi Hatırlatıcı",
        "sub":   "Aralık seçin ve Başlat'a basın",
        "every": "Her",          "suffix": " dk'da",  "quick": "Hızlı:",
        "start": "Hatırlatıcıyı Başlat",
        "ok":    "Tamam",        "snooze": "{n} dk sonra hatırlat",
        "drag":  "sürükle",      "no_img": "Dosya bulunamadı:\n{p}",
        "exit_tip": "Programı kapat",
    },
}

# Display order for the language selector grid
LANG_ORDER: list = [
    "en", "uk", "ru", "de", "es", "fr",
    "it", "zh", "ja", "pl", "pt", "tr",
]

# ══════════════════════════════════════════════════════════════════════════════
# Standard-library imports
# ══════════════════════════════════════════════════════════════════════════════
import json
import os
import sys
import ctypes
import time
import threading

# Suppress Qt DirectWrite warnings for legacy raster fonts on Windows
os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.fonts.warning=false")

# ══════════════════════════════════════════════════════════════════════════════
# Settings persistence
# ══════════════════════════════════════════════════════════════════════════════

def _settings_path() -> str:
    """Return the absolute path to the JSON settings file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), SETTINGS_FILE)


def load_settings() -> dict:
    """Load settings from disk; return {} if the file is missing or corrupt."""
    try:
        with open(_settings_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def save_settings(data: dict) -> None:
    """Persist settings to disk (silently ignores write errors)."""
    try:
        with open(_settings_path(), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# Qt imports
# ══════════════════════════════════════════════════════════════════════════════
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import (
    QEasingCurve,
    QObject,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)

# ══════════════════════════════════════════════════════════════════════════════
# Windows-specific stealth helpers
# ══════════════════════════════════════════════════════════════════════════════
IS_WIN: bool = sys.platform == "win32"

if IS_WIN:
    _GWL_EXSTYLE            = -20
    _WS_EX_LAYERED          = 0x00080000   # required for WDA and opacity
    _WS_EX_TOOLWINDOW       = 0x00000080   # hides window from taskbar
    _WDA_EXCLUDEFROMCAPTURE = 0x00000011   # invisible to screen-capture tools
    _user32 = ctypes.windll.user32


def apply_stealth(hwnd: int) -> None:
    """
    Make the window invisible to screen-capture software (Meet, Zoom, OBS).

    Uses WDA_EXCLUDEFROMCAPTURE — a Windows 10 (2004+) API that excludes
    the window from desktop capture without affecting mouse interactivity.

    WS_EX_TRANSPARENT is intentionally NOT used: it redirects all mouse events
    to the window beneath at the OS level, making every button unclickable.
    """
    if not IS_WIN:
        return
    try:
        current = _user32.GetWindowLongW(hwnd, _GWL_EXSTYLE)
        _user32.SetWindowLongW(
            hwnd, _GWL_EXSTYLE,
            current | _WS_EX_LAYERED | _WS_EX_TOOLWINDOW,
        )
        _user32.SetWindowDisplayAffinity(hwnd, _WDA_EXCLUDEFROMCAPTURE)
    except Exception:
        pass   # stealth is best-effort; the app still works without it

# ══════════════════════════════════════════════════════════════════════════════
# Cross-thread timer
# ══════════════════════════════════════════════════════════════════════════════

class _TimerSignal(QObject):
    """Carries the timeout signal across the thread boundary."""
    fired = pyqtSignal()


class AppTimer:
    """
    Wraps threading.Timer and delivers the timeout to the Qt UI thread via
    a pyqtSignal.  Calling QTimer.singleShot() directly from a background
    thread is silently ignored by PyQt6, so this signal-based approach is
    the only correct solution.
    """

    def __init__(self, callback) -> None:
        self._sig   = _TimerSignal()
        self._sig.fired.connect(callback)
        self._timer: threading.Timer | None = None

    def schedule(self, minutes: float) -> None:
        """Cancel any running timer and start a new one."""
        self.cancel()
        self._timer = threading.Timer(minutes * 60, self._sig.fired.emit)
        self._timer.daemon = True
        self._timer.start()

    def cancel(self) -> None:
        """Stop the pending timer if one is running."""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

# ══════════════════════════════════════════════════════════════════════════════
# Shared drawing helpers
# ══════════════════════════════════════════════════════════════════════════════

def _make_font(size: int, bold: bool = False, mono: bool = False) -> QFont:
    """Return a QFont using Windows-safe font names."""
    font = QFont(FONT_MONO if mono else FONT_SANS)
    font.setPixelSize(size)
    if bold:
        font.setWeight(QFont.Weight.Bold)
    return font


def _paint_glass_card(widget: QWidget, radius: int = CARD_RADIUS) -> None:
    """
    Draw the glassmorphism window background:
      • 6-layer outer neon glow
      • Dark gradient glass body (top → bottom)
      • Top-edge shimmer (white 18 % → 0)
      • 1.2 px neon border
      • 1 px inner white highlight

    WA_TranslucentBackground handles the alpha channel, so no setMask() is
    needed — rounded edges are fully anti-aliased at any DPI.
    """
    p = QPainter(widget)
    p.setRenderHints(
        QPainter.RenderHint.Antialiasing
        | QPainter.RenderHint.SmoothPixmapTransform
    )
    inset = 10
    rect  = QRectF(widget.rect()).adjusted(inset, inset, -inset, -inset)

    # Outer glow (6 concentric rings, fading outward)
    gr, gg, gb, _ = C["glow"]
    for i in range(6, 0, -1):
        exp = float(i) * 2.0
        pen = QPen(QColor(gr, gg, gb, 4 * i), exp * 1.1)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(pen)
        p.drawRoundedRect(
            rect.adjusted(-exp, -exp, exp, exp),
            radius + exp * 0.5, radius + exp * 0.5,
        )

    # Glass body
    path = QPainterPath()
    path.addRoundedRect(rect, radius, radius)

    grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
    grad.setColorAt(0.0, QColor(*C["glass_top"]))
    grad.setColorAt(1.0, QColor(*C["glass_bot"]))
    p.fillPath(path, grad)

    shimmer = QLinearGradient(
        rect.topLeft(), QPointF(rect.left(), rect.top() + 60)
    )
    shimmer.setColorAt(0.0, QColor(255, 255, 255, 18))
    shimmer.setColorAt(1.0, QColor(255, 255, 255, 0))
    p.fillPath(path, shimmer)

    # Neon border
    br, bg, bb, ba = C["border"]
    bpen = QPen(QColor(br, bg, bb, ba), 1.2)
    bpen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(bpen)
    p.drawRoundedRect(
        rect.adjusted(0.6, 0.6, -0.6, -0.6), radius - 0.5, radius - 0.5
    )

    # Inner highlight (top-edge glint)
    p.setPen(QPen(QColor(255, 255, 255, 14), 1.0))
    p.drawRoundedRect(rect.adjusted(1, 1, -1, -1), radius - 1, radius - 1)
    p.end()


def _make_separator(parent: QWidget | None = None) -> QWidget:
    """Return a 1 px horizontal separator line styled to match the palette."""
    w = QWidget(parent)
    w.setFixedHeight(1)
    w.setStyleSheet(f"background:{C['separator']};border:none;")
    return w


def _fade_window(
    widget: QWidget,
    start: float,
    end: float,
    duration_ms: int,
    on_done=None,
) -> None:
    """Animate window opacity from *start* to *end* over *duration_ms* ms."""
    anim = QPropertyAnimation(widget, b"windowOpacity", widget)
    anim.setDuration(duration_ms)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(
        QEasingCurve.Type.OutCubic if end > start else QEasingCurve.Type.InQuad
    )
    if on_done is not None:
        anim.finished.connect(on_done)
    anim.start()
    widget._anim = anim  # prevent garbage collection before animation ends


def _center_on_screen(widget: QWidget) -> None:
    """Move *widget* to the centre of the primary display."""
    widget.adjustSize()
    geo = QApplication.primaryScreen().availableGeometry()
    widget.move(
        geo.center().x() - widget.width()  // 2,
        geo.center().y() - widget.height() // 2,
    )


def _format_next_time(minutes: float) -> str:
    """Return a HH:MM clock string for *minutes* from now."""
    return time.strftime("%H:%M", time.localtime(time.time() + minutes * 60))

# ══════════════════════════════════════════════════════════════════════════════
# GlowButton — pill-shaped animated button
# ══════════════════════════════════════════════════════════════════════════════

class GlowButton(QPushButton):
    """
    Pill-shaped button with smooth hover glow animation.

    Qt stylesheets don't support CSS transitions, so the hover effect is
    emulated by a 12 ms QTimer that increments a blend factor (0 → 1 on
    mouse enter, 1 → 0 on leave) and repaints the button each tick.
    """

    def __init__(
        self,
        text: str,
        bg_color: str,
        bg_hover: str,
        height: int = 48,
        min_width: int | None = None,
        radius: int | None = None,
        border_color: str | None = None,
        font_size: int = 12,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self._col_bg    = QColor(bg_color)
        self._col_hover = QColor(bg_hover)
        self._col_brd   = QColor(border_color) if border_color else None
        self._radius    = radius if radius is not None else height // 2
        self._font_size = font_size
        self._hover_t   = 0.0   # blend factor: 0 = resting, 1 = fully hovered
        self._pressed   = False

        self._hover_timer = QTimer(self)
        self._hover_timer.setInterval(12)
        self._hover_timer.timeout.connect(self._advance_hover)

        self.setFixedHeight(height)
        if min_width:
            self.setMinimumWidth(min_width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # Make Qt treat the button as transparent — all drawing done in paintEvent
        self.setStyleSheet(
            "QPushButton{background:transparent;border:none;color:transparent;}"
        )

    @staticmethod
    def _lerp_color(a: QColor, b: QColor, t: float) -> QColor:
        """Linearly interpolate between two QColors by factor *t* (0–1)."""
        return QColor(
            int(a.red()   + (b.red()   - a.red())   * t),
            int(a.green() + (b.green() - a.green()) * t),
            int(a.blue()  + (b.blue()  - a.blue())  * t),
            int(a.alpha() + (b.alpha() - a.alpha()) * t),
        )

    def _advance_hover(self) -> None:
        target = 1.0 if self.underMouse() else 0.0
        step   = 0.08
        delta  = target - self._hover_t
        if abs(delta) <= step:
            self._hover_t = target
            self._hover_timer.stop()
        else:
            self._hover_t += step if delta > 0 else -step
        self.update()

    # -- Qt event overrides ---------------------------------------------------

    def enterEvent(self, event) -> None:
        self._hover_timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._hover_timer.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, _) -> None:
        p    = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(3, 3, -3, -3)
        t    = self._hover_t

        bg = self._lerp_color(self._col_bg, self._col_hover, t)
        if self._pressed:
            bg = bg.darker(130)

        # Glow halo — only visible while hovering
        if t > 0.05:
            glow_a = int(t * 55)
            for i in range(4, 0, -1):
                gp = QPen(
                    QColor(
                        self._col_hover.red(),
                        self._col_hover.green(),
                        self._col_hover.blue(),
                        glow_a * i // 4,
                    ),
                    float(i) * 2.0,
                )
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(gp)
                p.drawRoundedRect(
                    rect.adjusted(-i, -i, i, i),
                    self._radius + i, self._radius + i,
                )

        # Button fill
        p.setBrush(QBrush(bg))
        if self._col_brd:
            brd = self._lerp_color(self._col_brd, self._col_brd.lighter(140), t)
            p.setPen(QPen(brd, 1.2))
        else:
            p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, self._radius, self._radius)

        # Button text
        p.setPen(QColor(255, 255, 255, 230 if not self._pressed else 180))
        p.setFont(_make_font(self._font_size, bold=True))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        p.end()

# ══════════════════════════════════════════════════════════════════════════════
# ExitButton — ⛔ styled with CSS only
# ══════════════════════════════════════════════════════════════════════════════

class ExitButton(QPushButton):
    """
    Simple ⛔ exit button.  Pure CSS styling — no custom paintEvent needed.
    The tooltip shows the translated "Turn off program" string.
    """

    _STYLE = """
        QPushButton {
            background: rgba(60, 10, 10, 0.55);
            border: 1px solid rgba(200, 60, 60, 0.45);
            border-radius: 10px;
            font-size: 18px;
        }
        QPushButton:hover {
            background: rgba(180, 30, 30, 0.70);
            border-color: rgba(255, 80, 80, 0.80);
        }
        QPushButton:pressed {
            background: rgba(220, 20, 20, 0.85);
        }
    """

    def __init__(
        self,
        tooltip: str = "Turn off program",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__("⛔", parent)
        self.setFixedSize(34, 34)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setStyleSheet(self._STYLE)

    def update_tooltip(self, text: str) -> None:
        self.setToolTip(text)

# ══════════════════════════════════════════════════════════════════════════════
# MinutePicker  ‹  020 min  ›
# ══════════════════════════════════════════════════════════════════════════════

class MinutePicker(QWidget):
    """
    Horizontal pill control for selecting a minute value (1–180).
    Both ‹ and › step by exactly 1.  Mouse wheel also steps by 1.
    Quick-pick buttons in SetupWindow jump directly to preset values.
    """

    value_changed = pyqtSignal(int)

    _BTN_CSS = (
        f"QPushButton{{"
        f"background:rgba(70,140,255,0.13);color:{PALETTE['accent']};"
        f"border:1px solid rgba(70,140,255,0.32);"
        f"font:700 20px \"{FONT_SANS}\";"
        f"min-width:48px;max-width:48px;min-height:48px;max-height:48px;}}"
        f"QPushButton:hover{{background:rgba(70,140,255,0.32);color:white;"
        f"border-color:rgba(70,140,255,0.70);}}"
        f"QPushButton:pressed{{background:rgba(70,140,255,0.52);}}"
    )

    def __init__(
        self,
        value: int = 20,
        suffix: str = " min",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._value  = max(1, min(180, value))
        self._suffix = suffix
        self._build()

    def _build(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._btn_dec = QPushButton("‹")
        self._btn_dec.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._btn_dec.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_dec.setStyleSheet(
            self._BTN_CSS
            + "QPushButton{border-radius:24px 0 0 24px;border-right:none;}"
        )
        self._btn_dec.clicked.connect(self.decrement)

        self._label = QLabel(self._format())
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setFixedHeight(48)
        self._label.setMinimumWidth(130)
        self._label.setStyleSheet(
            f"QLabel{{background:{C['picker_bg']};color:{C['accent2']};"
            f"border-top:1px solid rgba(70,140,255,0.32);"
            f"border-bottom:1px solid rgba(70,140,255,0.32);"
            f"border-left:none;border-right:none;border-radius:0px;"
            f"font:700 18px \"{FONT_MONO}\";}}"
        )

        self._btn_inc = QPushButton("›")
        self._btn_inc.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._btn_inc.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_inc.setStyleSheet(
            self._BTN_CSS
            + "QPushButton{border-radius:0 24px 24px 0;border-left:none;}"
        )
        self._btn_inc.clicked.connect(self.increment)

        layout.addWidget(self._btn_dec)
        layout.addWidget(self._label)
        layout.addWidget(self._btn_inc)

    # -- Public API -----------------------------------------------------------

    def value(self) -> int:
        return self._value

    def setValue(self, v: int) -> None:
        self._set(v)

    def set_suffix(self, suffix: str) -> None:
        self._suffix = suffix
        self._label.setText(self._format())

    def increment(self) -> None:
        self._set(self._value + 1)

    def decrement(self) -> None:
        self._set(self._value - 1)

    # -- Internal -------------------------------------------------------------

    def _format(self) -> str:
        return f"  {self._value:>3}{self._suffix}  "

    def _set(self, v: int) -> None:
        clamped = max(1, min(180, v))
        if clamped != self._value:
            self._value = clamped
            self._label.setText(self._format())
            self.value_changed.emit(self._value)

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            self.increment()
        else:
            self.decrement()

# ══════════════════════════════════════════════════════════════════════════════
# LangGrid — collapsible language selector
# ══════════════════════════════════════════════════════════════════════════════

class LangGrid(QWidget):
    """
    Collapsible language picker displayed as a 3-column scrollable grid.

    A single toggle button (▶ / ▼) shows and hides the grid panel.
    The panel starts collapsed to minimise vertical space.  After the user
    selects a language the panel automatically collapses again.
    """

    lang_changed = pyqtSignal(str)

    # CSS template for individual language chip buttons
    _CHIP_TPL = (
        "QPushButton{{background:{bg};color:{cl};"
        "border:1px solid {brd};border-radius:10px;"
        "padding:0 8px;font:{fw} 10px \"{font}\";text-align:left;}}"
        "QPushButton:hover{{background:{hv};color:white;"
        "border-color:rgba(70,140,255,0.70);}}"
    )

    def __init__(self, current_lang: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._current  = current_lang
        self._buttons: dict = {}
        self._expanded = False
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Toggle button (always visible)
        self._toggle_btn = QPushButton(self._toggle_label())
        self._toggle_btn.setFixedHeight(30)
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._toggle_btn.setStyleSheet(
            f"QPushButton{{background:{C['chip']};color:{C['accent2']};"
            f"border:1px solid {C['chip_brd']};border-radius:10px;"
            f"padding:0 12px;font:600 10px \"{FONT_SANS}\";text-align:left;}}"
            f"QPushButton:hover{{background:{C['chip_hv']};color:white;"
            f"border-color:rgba(70,140,255,0.65);}}"
        )
        self._toggle_btn.clicked.connect(self._toggle)
        layout.addWidget(self._toggle_btn)

        # Collapsible panel (hidden by default)
        self._panel = QWidget()
        self._panel.setVisible(False)

        panel_vl = QVBoxLayout(self._panel)
        panel_vl.setContentsMargins(0, 0, 0, 0)
        panel_vl.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFixedHeight(118)
        scroll.setStyleSheet(
            f"QScrollArea{{background:rgba(10,14,35,0.96);"
            f"border:1px solid rgba(70,140,255,0.30);border-radius:14px;}}"
            f"QScrollBar:vertical{{background:rgba(70,140,255,0.06);"
            f"width:5px;margin:4px 2px;border-radius:3px;}}"
            f"QScrollBar::handle:vertical{{background:rgba(70,140,255,0.40);"
            f"border-radius:3px;min-height:20px;}}"
            f"QScrollBar::handle:vertical:hover{{background:rgba(70,140,255,0.75);}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}"
        )

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background:transparent;border:none;")
        grid = QGridLayout(grid_widget)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setSpacing(5)

        cols = 3
        for idx, code in enumerate(LANG_ORDER):
            info = LANGS[code]
            btn  = QPushButton(f"{info['flag']}  {info['name']}")
            btn.setFixedHeight(30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(self._chip_css(code == self._current))
            btn.clicked.connect(lambda _checked, c=code: self._select(c))
            grid.addWidget(btn, idx // cols, idx % cols)
            self._buttons[code] = btn

        scroll.setWidget(grid_widget)
        panel_vl.addWidget(scroll)
        layout.addWidget(self._panel)

    # -- Internal -------------------------------------------------------------

    def _toggle_label(self) -> str:
        arrow = "▼" if self._expanded else "▶"
        return f"{arrow}  🌐  {LANGS[self._current]['name']}"

    def _chip_css(self, selected: bool) -> str:
        return self._CHIP_TPL.format(
            bg   = C["chip_sel"] if selected else C["chip"],
            cl   = "white"       if selected else C["text"],
            brd  = "rgba(70,140,255,0.65)" if selected else C["chip_brd"],
            fw   = "700"         if selected else "400",
            hv   = C["chip_hv"],
            font = FONT_SANS,
        )

    def _toggle(self) -> None:
        """Show or hide the language grid."""
        self._expanded = not self._expanded
        self._panel.setVisible(self._expanded)
        self._toggle_btn.setText(self._toggle_label())

    def _select(self, code: str) -> None:
        """Handle a chip click — update highlight, collapse, emit signal."""
        if code == self._current:
            # Clicking the active language just closes the panel
            self._expanded = False
            self._panel.setVisible(False)
            self._toggle_btn.setText(self._toggle_label())
            return

        # Move the highlight
        self._buttons[self._current].setStyleSheet(self._chip_css(False))
        self._current = code
        self._buttons[code].setStyleSheet(self._chip_css(True))

        # Auto-collapse after selection
        self._expanded = False
        self._panel.setVisible(False)
        self._toggle_btn.setText(self._toggle_label())

        self.lang_changed.emit(code)

    # -- Public API -----------------------------------------------------------

    def set_current(self, code: str) -> None:
        """Update the highlighted chip without emitting lang_changed."""
        if code == self._current:
            return
        self._buttons[self._current].setStyleSheet(self._chip_css(False))
        self._current = code
        self._buttons[code].setStyleSheet(self._chip_css(True))
        self._toggle_btn.setText(self._toggle_label())

    @property
    def current(self) -> str:
        return self._current

# ══════════════════════════════════════════════════════════════════════════════
# BottomBar — language selector + exit button row
# ══════════════════════════════════════════════════════════════════════════════

class BottomBar(QWidget):
    """
    Reusable footer present in both SetupWindow and EyePopup.
    Contains the collapsible LangGrid and the ExitButton.
    """

    lang_changed = pyqtSignal(str)
    exit_clicked = pyqtSignal()

    def __init__(self, lang: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._lang = lang
        self.setStyleSheet("background:transparent;")
        self._build()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(8)

        self._lang_grid = LangGrid(self._lang)
        self._lang_grid.lang_changed.connect(self._on_lang_selected)
        row.addWidget(self._lang_grid, stretch=1)

        self._exit_btn = ExitButton(LANGS[self._lang].get("exit_tip", "Exit"))
        self._exit_btn.clicked.connect(self.exit_clicked.emit)
        row.addWidget(self._exit_btn)

        layout.addLayout(row)

    def _on_lang_selected(self, code: str) -> None:
        self._lang = code
        self._exit_btn.update_tooltip(LANGS[code].get("exit_tip", "Exit"))
        self.lang_changed.emit(code)

    def update_lang(self, code: str) -> None:
        """Sync the bar when a language change originates elsewhere."""
        self._lang = code
        self._exit_btn.update_tooltip(LANGS[code].get("exit_tip", "Exit"))
        self._lang_grid.set_current(code)

# ══════════════════════════════════════════════════════════════════════════════
# BaseCard — shared window base
# ══════════════════════════════════════════════════════════════════════════════

class BaseCard(QWidget):
    """
    Frameless, translucent, always-on-top window with:
      • Glassmorphism background painted in paintEvent
      • Drag-to-move (click and drag anywhere on the card)
      • Fade-in animation; stealth applied 120 ms after show
    """

    def __init__(self) -> None:
        super().__init__()
        self._drag_pos = None
        self._anim     = None
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setContentsMargins(14, 14, 14, 14)

    def show_card(self) -> None:
        """Centre on screen, apply stealth, then fade in."""
        _center_on_screen(self)
        self.setWindowOpacity(0.0)
        self.show()
        QTimer.singleShot(120, lambda: apply_stealth(int(self.winId())))
        _fade_window(self, 0.0, 0.97, 300)

    def paintEvent(self, _) -> None:
        _paint_glass_card(self)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(
                self.pos() + event.globalPosition().toPoint() - self._drag_pos
            )
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, _) -> None:
        self._drag_pos = None

# ══════════════════════════════════════════════════════════════════════════════
# SetupWindow
# ══════════════════════════════════════════════════════════════════════════════

class SetupWindow(BaseCard):
    """
    Initial configuration overlay.

    Layout:
      Header (👁 title)
      Subtitle
      ── separator ──
      Interval picker row
      Quick-pick chips
      ── separator ──
      ▶ Start Reminder button
      ── separator ──
      BottomBar (LangGrid ▶▼ + ExitButton)

    On language change the inner content is rebuilt using the safe
    setParent(None) teardown pattern to avoid crashing Qt.
    """

    def __init__(self, lang: str, on_start) -> None:
        super().__init__()
        self._lang     = lang
        self._on_start = on_start

        # Outer layout is created once — only _inner is replaced on lang change
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(0)

        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        outer.addWidget(self._inner)

        self._rebuild()
        self.show_card()

    # -- UI construction ------------------------------------------------------

    def _rebuild(self) -> None:
        """
        Replace the inner widget with freshly translated content.

        Safe teardown: reparent the old inner widget to a throwaway QWidget
        so that Qt garbage-collects the entire old subtree.  Calling
        deleteLater() on a layout that still has a parent crashes Qt.
        """
        T = LANGS[self._lang]

        old = self._inner
        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        self.layout().replaceWidget(old, self._inner)
        old.setParent(None)   # safe: Qt handles the cleanup

        vl = QVBoxLayout(self._inner)
        vl.setContentsMargins(12, 8, 12, 8)
        vl.setSpacing(0)

        # Header
        vl.addWidget(self._build_header(T))

        # Subtitle
        sub = QLabel(T["sub"])
        sub.setStyleSheet(
            f"color:{C['subtext']};font:10px \"{FONT_SANS}\";background:transparent;"
        )
        vl.addWidget(sub)
        vl.addSpacing(16)
        vl.addWidget(_make_separator())
        vl.addSpacing(18)

        # Interval picker
        vl.addLayout(self._build_interval_row(T))
        vl.addSpacing(12)

        # Quick-pick chips
        vl.addLayout(self._build_quickpick_row(T))
        vl.addSpacing(22)
        vl.addWidget(_make_separator())
        vl.addSpacing(16)

        # Start button
        self._btn_start = GlowButton(
            f"▶  {T['start']}",
            C["btn_ok"], C["btn_ok_hv"],
            height=52, min_width=260, font_size=13,
        )
        self._btn_start.clicked.connect(self._do_start)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self._btn_start)
        btn_row.addStretch()
        vl.addLayout(btn_row)
        vl.addSpacing(18)
        vl.addWidget(_make_separator())
        vl.addSpacing(14)

        # Bottom bar
        self._bottom_bar = BottomBar(self._lang)
        self._bottom_bar.lang_changed.connect(self._on_lang_changed)
        self._bottom_bar.exit_clicked.connect(QApplication.quit)
        vl.addWidget(self._bottom_bar)

    def _build_header(self, T: dict) -> QWidget:
        hdr = QWidget()
        hdr.setStyleSheet("background:transparent;")
        hdr.setFixedHeight(44)
        row = QHBoxLayout(hdr)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        eye = QLabel("👁")
        eye.setStyleSheet("font-size:22px;background:transparent;")
        row.addWidget(eye)
        title = QLabel(T["title"])
        title.setStyleSheet(
            f"color:{C['accent']};font:700 14px \"{FONT_SANS}\";background:transparent;"
        )
        row.addWidget(title)
        row.addStretch()
        return hdr

    def _build_interval_row(self, T: dict) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(14)
        lbl = QLabel(T["every"])
        lbl.setStyleSheet(
            f"color:{C['text']};font:13px \"{FONT_SANS}\";background:transparent;"
        )
        row.addWidget(lbl)
        self._picker = MinutePicker(DEFAULT_INTERVAL, T["suffix"])
        row.addWidget(self._picker)
        row.addStretch()
        return row

    def _build_quickpick_row(self, T: dict) -> QHBoxLayout:
        chip_css = (
            f"QPushButton{{background:{C['chip']};color:{C['accent']};"
            f"border:1px solid {C['chip_brd']};border-radius:15px;"
            f"font:600 10px \"{FONT_SANS}\";}}"
            f"QPushButton:hover{{background:{C['chip_hv']};color:white;"
            f"border-color:rgba(70,140,255,0.65);}}"
            f"QPushButton:pressed{{background:{C['chip_sel']};}}"
        )
        row = QHBoxLayout()
        row.setSpacing(5)
        lbl = QLabel(T["quick"])
        lbl.setStyleSheet(
            f"color:{C['subtext']};font:10px \"{FONT_SANS}\";background:transparent;"
        )
        row.addWidget(lbl)
        for v in [1, 5, 10, 15, 20, 30, 45, 60]:
            btn = QPushButton(str(v))
            btn.setFixedSize(40, 30)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(chip_css)
            btn.clicked.connect(lambda _checked, val=v: self._picker.setValue(val))
            row.addWidget(btn)
        row.addStretch()
        return row

    # -- Slots ----------------------------------------------------------------

    def _on_lang_changed(self, code: str) -> None:
        self._lang = code
        cfg = load_settings()
        cfg["lang"] = code
        save_settings(cfg)
        prev = self._picker.value()
        self._rebuild()
        self._picker.setValue(prev)
        self._picker.set_suffix(LANGS[code]["suffix"])
        self.adjustSize()

    def _do_start(self) -> None:
        minutes = self._picker.value()
        _fade_window(
            self, self.windowOpacity(), 0.0, 240,
            on_done=lambda: (self.close(), self._on_start(minutes, self._lang)),
        )

# ══════════════════════════════════════════════════════════════════════════════
# EyePopup — exercise reminder overlay
# ══════════════════════════════════════════════════════════════════════════════

class EyePopup(BaseCard):
    """
    Exercise reminder overlay.  Appears when the AppTimer fires.
    Has full feature parity with SetupWindow (language switcher + exit button).
    """

    def __init__(
        self,
        lang: str,
        interval: int,
        on_ok,
        on_snooze,
        on_lang_change,
    ) -> None:
        super().__init__()
        self._lang      = lang
        self._interval  = interval
        self._on_ok     = on_ok
        self._on_snooze = on_snooze
        self._on_lc     = on_lang_change

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(0)

        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        outer.addWidget(self._inner)

        self._rebuild()
        self.show_card()

    # -- UI construction ------------------------------------------------------

    def _rebuild(self) -> None:
        """Same safe teardown pattern as SetupWindow._rebuild."""
        T = LANGS[self._lang]

        old = self._inner
        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        self.layout().replaceWidget(old, self._inner)
        old.setParent(None)

        vl = QVBoxLayout(self._inner)
        vl.setContentsMargins(12, 8, 12, 8)
        vl.setSpacing(0)

        # Header
        vl.addWidget(self._build_header(T))

        # Subtitle + drag hint
        sub_row = QHBoxLayout()
        sub_row.setSpacing(0)
        sub = QLabel("Take a short break — your eyes deserve rest.")
        sub.setStyleSheet(
            f"color:{C['subtext']};font:10px \"{FONT_SANS}\";background:transparent;"
        )
        sub.setWordWrap(True)
        drag = QLabel(f"  ···  {T['drag']}")
        drag.setStyleSheet(
            f"color:{C['dim']};font:9px \"{FONT_SANS}\";background:transparent;"
        )
        sub_row.addWidget(sub)
        sub_row.addStretch()
        sub_row.addWidget(drag)
        vl.addLayout(sub_row)
        vl.addSpacing(12)
        vl.addWidget(_make_separator())
        vl.addSpacing(14)

        # Exercise image
        vl.addWidget(self._build_image_label(T))
        vl.addSpacing(14)
        vl.addWidget(_make_separator())
        vl.addSpacing(16)

        # OK / Snooze buttons
        vl.addLayout(self._build_button_row(T))
        vl.addSpacing(18)
        vl.addWidget(_make_separator())
        vl.addSpacing(14)

        # Bottom bar
        self._bottom_bar = BottomBar(self._lang)
        self._bottom_bar.lang_changed.connect(self._on_lang_changed)
        self._bottom_bar.exit_clicked.connect(QApplication.quit)
        vl.addWidget(self._bottom_bar)

    def _build_header(self, T: dict) -> QWidget:
        hdr = QWidget()
        hdr.setStyleSheet("background:transparent;")
        hdr.setFixedHeight(44)
        row = QHBoxLayout(hdr)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        eye = QLabel("👁")
        eye.setStyleSheet("font-size:22px;background:transparent;")
        row.addWidget(eye)
        title = QLabel(T["title"])
        title.setStyleSheet(
            f"color:{C['accent']};font:700 14px \"{FONT_SANS}\";background:transparent;"
        )
        row.addWidget(title)
        row.addStretch()
        return hdr

    def _build_image_label(self, T: dict) -> QLabel:
        img_path = (
            IMAGE_PATH
            if os.path.isabs(IMAGE_PATH)
            else os.path.join(
                os.path.dirname(os.path.abspath(__file__)), IMAGE_PATH
            )
        )
        lbl = QLabel()
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("background:transparent;")

        if os.path.exists(img_path):
            px = QPixmap(img_path)
            if not px.isNull():
                lbl.setPixmap(
                    px.scaled(
                        QSize(580, 360),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                lbl.setText(T["no_img"].format(p=img_path))
                lbl.setStyleSheet(
                    f"color:{C['subtext']};font:11px \"{FONT_SANS}\";"
                )
        else:
            lbl.setText(T["no_img"].format(p=img_path))
            lbl.setStyleSheet(
                f"color:{C['subtext']};font:11px \"{FONT_SANS}\";"
            )
        return lbl

    def _build_button_row(self, T: dict) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(14)
        row.addStretch()

        self._btn_ok = GlowButton(
            f"✓  {T['ok']}",
            C["btn_ok"], C["btn_ok_hv"],
            height=52, min_width=140, font_size=13,
        )
        self._btn_ok.clicked.connect(self._do_ok)
        row.addWidget(self._btn_ok)

        self._btn_snooze = GlowButton(
            f"🕒  {T['snooze'].format(n=SNOOZE_MINUTES)}",
            C["btn_sn"], C["btn_sn_hv"],
            height=52, min_width=240, font_size=12,
            border_color=C["btn_sn_brd"],
        )
        self._btn_snooze.clicked.connect(self._do_snooze)
        row.addWidget(self._btn_snooze)

        row.addStretch()
        return row

    # -- Slots ----------------------------------------------------------------

    def _on_lang_changed(self, code: str) -> None:
        self._lang = code
        cfg = load_settings()
        cfg["lang"] = code
        save_settings(cfg)
        self._on_lc(code)   # keep EyeReminderApp in sync
        self._rebuild()
        self.adjustSize()

    def _do_ok(self) -> None:
        _fade_window(
            self, self.windowOpacity(), 0.0, 200,
            on_done=lambda: (self.close(), self._on_ok()),
        )

    def _do_snooze(self) -> None:
        _fade_window(
            self, self.windowOpacity(), 0.0, 200,
            on_done=lambda: (self.close(), self._on_snooze()),
        )

# ══════════════════════════════════════════════════════════════════════════════
# Console banner and logging
# ══════════════════════════════════════════════════════════════════════════════

def _print_banner() -> None:
    """Print a coloured startup banner (skipped automatically in windowless mode)."""
    RST = "\033[0m"; BOLD = "\033[1m"; CYAN = "\033[96m"
    BLU = "\033[94m"; GRN  = "\033[92m"; YEL  = "\033[93m"
    DIM = "\033[2m";  WHT  = "\033[97m"

    if IS_WIN:
        try:   # enable ANSI on legacy Windows terminals (cmd.exe / old PowerShell)
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass

    W = 54

    def cen(text: str, col: str = WHT) -> str:
        pad = W - len(text)
        return f"{BLU}|{RST}{' ' * (pad // 2)}{col}{BOLD}{text}{RST}{' ' * (pad - pad // 2)}{BLU}|{RST}"

    def lft(text: str, col: str = DIM) -> str:
        return f"{BLU}|{RST}  {col}{text}{RST}{' ' * max(W - 2 - len(text), 0)}{BLU}|{RST}"

    lines = [
        f"{BLU}+{'=' * W}+{RST}",
        cen(""),
        cen("EYE EXERCISE REMINDER  v6.0", CYAN),
        cen("Cyber-Premium Edition",       DIM),
        cen(""),
        f"{BLU}+{'=' * W}+{RST}",
        cen(""),
        lft(f"Default interval : {DEFAULT_INTERVAL} min", GRN),
        lft(f"Snooze interval  : {SNOOZE_MINUTES} min",   YEL),
        lft(f"Image file       : {IMAGE_PATH}",           DIM),
        lft(f"Settings file    : {SETTINGS_FILE}",        DIM),
        cen(""),
        f"{BLU}+{'=' * W}+{RST}",
        cen(""),
        lft("Setup window opening...", CYAN),
        cen(""),
        f"{BLU}+{'=' * W}+{RST}",
        f"  {DIM}Press Ctrl+C or close this window to stop.{RST}",
    ]
    print()
    for line in lines:
        print(line)
    print()


def _log(message: str, level: str = "W") -> None:
    """Print a timestamped coloured log line to stdout."""
    colours = {"GR": "\033[92m", "CY": "\033[96m", "YL": "\033[93m", "W": "\033[97m"}
    RST = "\033[0m"; DIM = "\033[2m"
    stamp = time.strftime("%H:%M:%S")
    print(f"  {colours.get(level, '')}{message}{RST}  {DIM}({stamp}){RST}")

# ══════════════════════════════════════════════════════════════════════════════
# EyeReminderApp — application controller
# ══════════════════════════════════════════════════════════════════════════════

class EyeReminderApp:
    """
    Top-level controller.  Owns the QApplication, the AppTimer, and the
    references to the active overlay windows.

    Flow:
      1. SetupWindow opens immediately.
      2. User confirms → _on_setup_confirmed → AppTimer.schedule().
      3. Timer fires → _show_popup → EyePopup appears.
      4. User clicks OK / Snooze → timer re-scheduled → back to step 3.
    """

    def __init__(self) -> None:
        _print_banner()

        self._app = QApplication(sys.argv)
        self._app.setQuitOnLastWindowClosed(False)

        if IS_WIN:
            # Give the process its own taskbar identity (avoids "Python" label)
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "eye_reminder.app.6.0"
                )
            except Exception:
                pass

        cfg            = load_settings()
        self._lang     = cfg.get("lang", "en")
        self._interval = DEFAULT_INTERVAL
        self._popup: EyePopup | None = None
        self._timer    = AppTimer(self._show_popup)

        SetupWindow(self._lang, self._on_setup_confirmed)
        sys.exit(self._app.exec())

    # -- SetupWindow callback -------------------------------------------------

    def _on_setup_confirmed(self, minutes: int, lang: str) -> None:
        self._interval = minutes
        self._lang     = lang
        cfg = load_settings()
        cfg["lang"] = lang
        save_settings(cfg)
        _log(
            f"Started — interval: {minutes} min  |  lang: {lang}"
            f"  |  first reminder at {_format_next_time(minutes)}",
            "GR",
        )
        self._timer.schedule(minutes)

    # -- Timer callback -------------------------------------------------------

    def _show_popup(self) -> None:
        if self._popup and self._popup.isVisible():
            self._popup.raise_()
            return
        _log("Showing reminder popup", "CY")
        self._popup = EyePopup(
            lang           = self._lang,
            interval       = self._interval,
            on_ok          = self._on_popup_ok,
            on_snooze      = self._on_popup_snooze,
            on_lang_change = self._on_lang_from_popup,
        )

    # -- EyePopup callbacks ---------------------------------------------------

    def _on_lang_from_popup(self, code: str) -> None:
        """Keep the controller in sync when language changes inside the popup."""
        self._lang = code

    def _on_popup_ok(self) -> None:
        _log(
            f"OK — next at {_format_next_time(self._interval)} "
            f"(in {self._interval} min)",
            "GR",
        )
        self._timer.schedule(self._interval)

    def _on_popup_snooze(self) -> None:
        _log(
            f"Snooze — next at {_format_next_time(SNOOZE_MINUTES)} "
            f"(in {SNOOZE_MINUTES} min)",
            "YL",
        )
        self._timer.schedule(SNOOZE_MINUTES)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    EyeReminderApp()
