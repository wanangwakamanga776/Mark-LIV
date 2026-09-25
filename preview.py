"""Standalone visual preview for the MARK LIV desktop HUD.

Run with: python preview.py
This launches the real PyQt6 interface without starting Gemini, audio capture,
or any assistant actions. It is safe to use before downloading/configuring the
full assistant.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from ui import JarvisUI


DEMO_LOG = [
    "SYS: Preview mode enabled. Live services are paused.",
    "SYS: HUD rendering online.",
    "JARVIS: Good evening. All systems are standing by.",
    "You: Show me the interface preview.",
    "JARVIS: The desktop HUD is ready for configuration.",
]


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    ui = JarvisUI(str(Path(__file__).parent / "assets" / "face.png"))
    window = ui._win

    # The normal app shows setup when credentials are missing. Preview mode
    # intentionally skips that gate so the visual interface can be inspected.
    overlay = getattr(window, "_overlay", None)
    if overlay is not None:
        overlay.hide()
        window._overlay = None
    window._ready = True
    window._apply_state("LISTENING")

    for line in DEMO_LOG:
        window._log.append_log(line)

    phase = 0.0

    def animate_demo() -> None:
        nonlocal phase
        phase += 0.18
        level = 0.12 + (math.sin(phase) ** 2) * 0.55
        ui.set_audio_level(level)

    timer = QTimer(window)
    timer.timeout.connect(animate_demo)
    timer.start(55)
    window._preview_timer = timer

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
