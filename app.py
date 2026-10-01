import json
from pathlib import Path

import pandas as pd
import streamlit as st

from ocr_engine import extract_text_from_file
from ner_parser import parse_resume

st.set_page_config(page_title="Resume Parser using NER", page_icon="📄", layout="wide")

st.title("📄 Resume Parser using NER")
st.write("Upload a resume image or PDF. The system performs OCR, preprocessing, and Named Entity Recognition (NER), then extracts structured information.")

with st.sidebar:
    st.header("Pipeline")
    st.write("1. Upload resume")
    st.write("2. OpenCV preprocessing")
    st.write("3. OCR text extraction")
    st.write("4. spaCy NER")
    st.write("5. Regex + keyword rules")
    st.write("6. Structured JSON output")
    st.info("For scanned documents, Tesseract OCR must be installed on Windows.")

uploaded = st.file_uploader("Upload resume", type=["pdf", "png", "jpg", "jpeg"])

if uploaded:
    suffix = Path(uploaded.name).suffix.lower()
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / uploaded.name
    temp_path.write_bytes(uploaded.getbuffer())

    try:
        with st.spinner("Reading and parsing resume..."):
            raw_text, debug_images = extract_text_from_file(temp_path)
            data = parse_resume(raw_text)

        st.success("Resume parsed successfully.")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Extracted Text")
            st.text_area("OCR / document text", raw_text, height=450)

        with c2:
            st.subheader("Structured Information")
            display = {}
            for key, value in data.items():
                display[key] = value
            st.json(display)

        st.subheader("Named Entities")
        if data["entities"]:
            df = pd.DataFrame(data["entities"])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No spaCy NER entities were detected. Regex/keyword fields may still be available.")

        st.subheader("Download Result")
        result_json = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            "⬇️ Download JSON",
            data=result_json,
            file_name="parsed_resume.json",
            mime="application/json",
        )

        if debug_images:
            with st.expander("Show preprocessing preview"):
                for img_path in debug_images:
                    st.image(str(img_path), caption=img_path.name, use_container_width=True)

    except Exception as exc:
        st.error(f"Error: {exc}")
        st.code("python -m spacy download en_core_web_sm")
else:
    st.info("Upload a resume PDF/image to start.")
