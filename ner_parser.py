import re
import spacy

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp

    try:
        _nlp = spacy.load("en_core_web_sm")
    except OSError as exc:
        raise RuntimeError(
            "spaCy English model 'en_core_web_sm' is missing or failed to load. "
            "Install the model and redeploy."
        ) from exc

    return _nlp

SKILL_LIST = [
    "python", "java", "c", "c++", "sql", "mysql", "mongodb", "html", "css",
    "javascript", "react", "node.js", "flask", "django", "streamlit",
    "machine learning", "deep learning", "computer vision", "nlp",
    "data analytics", "pandas", "numpy", "matplotlib", "opencv",
    "tensorflow", "pytorch", "git", "github", "aws", "azure"
]

EDUCATION_WORDS = [
    "b.e", "b.tech", "m.e", "m.tech", "b.sc", "m.sc", "bca", "mca",
    "computer science", "information technology", "engineering",
    "bachelor", "master", "university", "college", "school"
]

def first_match(pattern, text, flags=re.I):
    match = re.search(pattern, text, flags)
    return match.group(0).strip() if match else ""

def extract_name(doc, text):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            candidate = ent.text.strip()
            if 2 <= len(candidate.split()) <= 5:
                return candidate
    for line in text.splitlines():
        line = re.sub(r"[^A-Za-z .'-]", "", line).strip()
        if 2 <= len(line.split()) <= 4 and line.isupper():
            return line.title()
    return ""

def extract_email(text):
    return first_match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)

def extract_phone(text):
    match = re.search(r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)", text)
    return re.sub(r"[\s-]+", "", match.group(0)) if match else ""

def extract_links(text):
    urls = re.findall(r"https?://[^\s]+|www\.[^\s]+", text, flags=re.I)
    return [u.rstrip(".,)") for u in urls]

def extract_skills(text):
    low = text.lower()
    found = []
    for skill in SKILL_LIST:
        pattern = rf"(?<!\w){re.escape(skill.lower())}(?!\w)"
        if re.search(pattern, low):
            found.append(skill)
    return sorted(found, key=str.lower)

def extract_education(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    hits = []
    for line in lines:
        low = line.lower()
        if any(word in low for word in EDUCATION_WORDS):
            hits.append(line)
    unique = []
    for x in hits:
        if x not in unique:
            unique.append(x)
    return unique[:10]

def parse_resume(text):
    nlp = get_nlp()
    doc = nlp(text)

    entities = [
        {"text": ent.text, "label": ent.label_, "description": spacy.explain(ent.label_) or ""}
        for ent in doc.ents
    ]

    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    locations = [ent.text for ent in doc.ents if ent.label_ in {"GPE", "LOC"}]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    return {
        "name": extract_name(doc, text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "links": extract_links(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "organizations": list(dict.fromkeys(organizations)),
        "locations": list(dict.fromkeys(locations)),
        "dates": list(dict.fromkeys(dates)),
        "entities": entities,
    }
