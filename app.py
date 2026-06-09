import tempfile
import os
from pathlib import Path

import streamlit as st
import ocrmypdf

st.set_page_config(page_title="OCR-Generator", page_icon="🔍", layout="centered")

st.title("🔍 OCR-Generator für PDFs")
st.caption(
    "Lade eine gescannte PDF hoch – die App erzeugt eine durchsuchbare PDF mit eingebettetem Text."
)

uploaded_file = st.file_uploader(
    "PDF-Datei hierher ziehen oder auswählen",
    type=["pdf"],
    help="Unterstützt werden beliebige PDFs, auch gemischte (Seiten mit und ohne Text).",
)

lang = st.selectbox(
    "OCR-Sprache",
    options=["deu", "eng", "deu+eng"],
    format_func=lambda x: {"deu": "Deutsch", "eng": "Englisch", "deu+eng": "Deutsch + Englisch"}[x],
)

if uploaded_file is not None:
    original_name = Path(uploaded_file.name).stem
    output_filename = f"{original_name}_ocr.pdf"

    if st.button("OCR starten", type="primary"):
        with st.spinner("OCR läuft – das kann je nach PDF-Größe einige Sekunden dauern …"):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    input_path = os.path.join(tmpdir, "input.pdf")
                    output_path = os.path.join(tmpdir, "output.pdf")

                    with open(input_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    ocrmypdf.ocr(
                        input_path,
                        output_path,
                        language=lang,
                        skip_text=True,
                        progress_bar=False,
                    )

                    with open(output_path, "rb") as f:
                        result_bytes = f.read()

                st.success("Fertig! Die durchsuchbare PDF steht zum Download bereit.")
                st.download_button(
                    label="📥 PDF herunterladen",
                    data=result_bytes,
                    file_name=output_filename,
                    mime="application/pdf",
                )

            except ocrmypdf.exceptions.PriorOcrFoundError:
                st.warning(
                    "Die PDF enthält bereits vollständig erkannten Text – kein OCR notwendig. "
                    "Lade die Originaldatei direkt herunter."
                )
            except ocrmypdf.exceptions.InputFileError as e:
                st.error(f"Ungültige oder beschädigte PDF-Datei: {e}")
            except Exception as e:
                st.error(f"Fehler bei der OCR-Verarbeitung: {e}")
