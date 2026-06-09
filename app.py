import tempfile
import os
from pathlib import Path

import streamlit as st
import ocrmypdf

st.set_page_config(page_title="OCR-Generator", page_icon="🔍", layout="centered")

st.title("🔍 OCR-Generator für PDFs")
st.caption(
    "Lade eine oder mehrere gescannte PDFs hoch – die App erzeugt durchsuchbare PDFs mit eingebettetem Text."
)

uploaded_files = st.file_uploader(
    "PDF-Dateien hierher ziehen oder auswählen",
    type=["pdf"],
    accept_multiple_files=True,
    help="Unterstützt werden beliebige PDFs, auch gemischte (Seiten mit und ohne Text).",
)

lang = st.selectbox(
    "OCR-Sprache",
    options=["deu", "eng", "deu+eng"],
    format_func=lambda x: {"deu": "Deutsch", "eng": "Englisch", "deu+eng": "Deutsch + Englisch"}[x],
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} Datei(en) ausgewählt.")

    if st.button("OCR starten", type="primary"):
        for uploaded_file in uploaded_files:
            original_name = Path(uploaded_file.name).stem
            output_filename = f"{original_name}_ocr.pdf"

            with st.spinner(f"Verarbeite **{uploaded_file.name}** …"):
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

                    st.success(f"**{uploaded_file.name}** fertig.")
                    st.download_button(
                        label=f"📥 {output_filename} herunterladen",
                        data=result_bytes,
                        file_name=output_filename,
                        mime="application/pdf",
                        key=output_filename,
                    )

                except ocrmypdf.exceptions.PriorOcrFoundError:
                    st.warning(
                        f"**{uploaded_file.name}** enthält bereits markierbaren Text – OCR übersprungen."
                    )
                except ocrmypdf.exceptions.InputFileError as e:
                    st.error(f"**{uploaded_file.name}**: Ungültige oder beschädigte Datei – {e}")
                except Exception as e:
                    st.error(f"**{uploaded_file.name}**: Fehler bei der OCR-Verarbeitung – {e}")
