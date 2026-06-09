# OCR-Generator

Lokale Streamlit-App: gescannte PDFs hochladen → durchsuchbares PDF herunterladen.

---

## 1. Systemabhängigkeiten installieren (macOS / Homebrew)

```bash
brew install tesseract tesseract-lang ghostscript unpaper pngquant
```

| Paket | Zweck |
|---|---|
| `tesseract` + `tesseract-lang` | OCR-Engine inkl. Deutsch, Englisch etc. |
| `ghostscript` | PDF-Rendering und -Verarbeitung |
| `unpaper` | Optionale Bildbereinigung vor OCR |
| `pngquant` | Bildkompression für kleinere Ausgabe-PDFs |

---

## 2. Python-Umgebung einrichten

```bash
cd ocr-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. App starten

```bash
streamlit run app.py
```

Der Browser öffnet sich automatisch unter **http://localhost:8501**.

---

## Benutzung

1. PDF per Drag & Drop ins Upload-Feld ziehen (oder „Browse files" klicken)
2. OCR-Sprache wählen (Deutsch / Englisch / beides)
3. „OCR starten" klicken
4. Fertige PDF über den Download-Button speichern

**Hinweis:** PDFs, die bereits vollständig markierbaren Text enthalten, werden erkannt und übersprungen – kein unnötiger Durchlauf.
