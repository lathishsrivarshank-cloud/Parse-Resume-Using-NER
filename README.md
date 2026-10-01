# Resume Parser using NER

## 1. What this project does
This project converts an uploaded resume image/PDF into structured information.

Pipeline:

Resume -> OpenCV preprocessing -> OCR -> Text -> spaCy NER + Regex/Keyword rules -> JSON

Although the topic is listed under **Computer Vision**, the project contains both:
- **Computer Vision:** image preprocessing before OCR
- **NLP:** Named Entity Recognition after OCR

## 2. Features
- Upload PDF/JPG/JPEG/PNG
- OCR for scanned resumes
- OpenCV grayscale, resize, denoise, and adaptive thresholding
- spaCy NER for PERSON, ORG, GPE/LOC, DATE, etc.
- Regex extraction for email and phone
- Keyword extraction for skills
- Education line extraction
- Download structured JSON
- Preprocessing preview

## 3. Windows setup in VS Code

### Step A - Install Python
Use Python 3.11 or 3.12 for the smoothest package compatibility.

### Step B - Open the project
In VS Code, open this folder.

### Step C - Create virtual environment
```powershell
python -m venv venv
```

Activate:
```powershell
.\venv\Scripts\activate
```

If PowerShell blocks activation, use:
```powershell
venv\Scripts\activate.bat
```

### Step D - Install Python packages
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step E - Install the spaCy English model
```powershell
python -m spacy download en_core_web_sm
```

### Step F - Install Tesseract OCR
Install Tesseract OCR for Windows, then make sure `tesseract.exe` is on PATH.

Common installation location:
`C:\Program Files\Tesseract-OCR\tesseract.exe`

If it is not on PATH, add this at the top of `ocr_engine.py`:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## 4. Run the project

First test the NER part without OCR:
```powershell
python run_demo.py
```

Then start the user interface:
```powershell
streamlit run app.py
```

A browser window will open. Upload a resume image/PDF.

## 5. Expected output
The application shows:
- Name
- Email
- Phone
- Links
- Skills
- Education
- Organizations
- Locations
- Dates
- All NER entities

## 6. How to explain the project in viva
**Why NER?**
NER identifies important entities in text, such as people, organizations, locations, and dates. A resume is mostly unstructured text, so NER helps convert it into structured information.

**Why Computer Vision?**
A scanned resume is an image. OpenCV improves the image quality before OCR converts it into text.

**Why OCR?**
OCR means Optical Character Recognition. It reads text from an image or scanned document.

**Why spaCy?**
spaCy provides a ready-to-use NER model and makes entity extraction simple.

**Why regex?**
Generic NER models do not reliably identify phone numbers and email addresses, so deterministic regex rules are used for those fields.

## 7. Limitations
- OCR quality depends on scan/image quality.
- Generic NER may miss unusual names or company names.
- Skill extraction currently uses a fixed keyword list.
- A production system would use a larger custom resume dataset and a custom-trained model.

## 8. Future enhancements
- Custom NER model trained on resumes
- PDF table/layout understanding
- Better skill taxonomy and synonyms
- Candidate-job matching
- REST API deployment
- Database storage
