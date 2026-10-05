from pathlib import Path
import re
import tempfile

import cv2
import numpy as np
import pytesseract
import fitz

def preprocess_image(image_bgr):
    """Improve document readability before OCR."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.8, fy=1.8, interpolation=cv2.INTER_CUBIC)
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    threshold = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 11,
    )
    return threshold

def ocr_bgr(image_bgr):
    processed = preprocess_image(image_bgr)
    try:
        pytesseract.get_tesseract_version()
        text = pytesseract.image_to_string(processed, config="--psm 6")
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR is not installed or not in PATH. "
            "On Streamlit Cloud, ensure packages.txt includes tesseract-ocr and libtesseract0."
        )
    return text, processed

def extract_text_from_file(path: Path):
    """
    Returns:
        combined_text: extracted text
        debug_images: paths to temporary preprocessing images
    """
    debug_dir = Path(tempfile.mkdtemp(prefix="resume_ocr_"))
    debug_images = []

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        pdf = fitz.open(path)
        texts = []

        for i, page in enumerate(pdf):
            text = page.get_text("text").strip()
            if len(re.sub(r"\s+", "", text)) >= 30:
                texts.append(text)
                continue

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            ocr_text, processed = ocr_bgr(img)
            out = debug_dir / f"page_{i+1}_preprocessed.png"
            cv2.imwrite(str(out), processed)
            debug_images.append(out)
            texts.append(ocr_text)

        pdf.close()
        return "\n\n".join(texts), debug_images

    image = cv2.imread(str(path))
    if image is None:
        raise ValueError("Could not open the uploaded image.")
    text, processed = ocr_bgr(image)
    out = debug_dir / "preprocessed.png"
    cv2.imwrite(str(out), processed)
    debug_images.append(out)
    return text, debug_images
