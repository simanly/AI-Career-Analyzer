import re

# Bölmə başlıqları: CV-nin başlığı (vəzifə adı) bunlardan əvvəl gəlir.
SECTION_PATTERN = re.compile(
    r"\b(?:Summary|Professional Summary|Career Overview|Career Focus|Highlights|"
    r"Skills|Core Qualifications|Qualifications|Objective|Experience|Education)\b"
)

TITLE_MAX_CHARS = 120
TITLE_FALLBACK_CHARS = 80


def normalize_text(text: str) -> str:
    """Boşluqları və sətir keçidlərini təmizləyir (PDF/DOCX çıxarışı üçün)."""
    return re.sub(r"\s+", " ", str(text)).strip()


def extract_title(text: str) -> str:
    """CV-nin başlığını (adətən vəzifə adı) ilk bölmə başlığına qədər götürür."""
    text = normalize_text(text)
    head = SECTION_PATTERN.split(text, maxsplit=1)[0].strip()

    if len(head) > 3:
        return head[:TITLE_MAX_CHARS]

    return text[:TITLE_FALLBACK_CHARS]


def body_texts(texts):
    return [normalize_text(t) for t in texts]


def title_texts(texts):
    return [extract_title(t) for t in texts]
