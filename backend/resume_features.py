import re

import numpy as np
from sklearn.svm import LinearSVC

# Bölmə başlıqları: CV-nin başlığı (vəzifə adı) bunlardan əvvəl gəlir.
# Böyük/kiçik hərfə həssas deyil: real CV-lərdə "EDUCATION" və "Education" hər ikisi olur.
SECTION_PATTERN = re.compile(
    r"\b(?:Summary|Professional Summary|Career Overview|Career Focus|Highlights|Profile|About Me|"
    r"Skills|Core Qualifications|Qualifications|Objective|Experience|Work Experience|Work History|"
    r"Employment History|Education|Contact|Projects|Certifications|Languages)\b",
    re.IGNORECASE,
)

# Başlıqdan çıxarılan əlaqə məlumatları (ad bunlardan sonra gəlmir, amma e-poçt/telefon səs-küydür).
NOISE_PATTERN = re.compile(
    r"\S+@\S+|https?://\S+|www\.\S+|\+?\(?\d[\d\s().-]{6,}\d"
)

TITLE_MAX_CHARS = 120
TITLE_FALLBACK_CHARS = 80


def normalize_text(text: str) -> str:
    """Boşluqları və sətir keçidlərini təmizləyir (PDF/DOCX çıxarışı üçün)."""
    return re.sub(r"\s+", " ", str(text)).strip()


def extract_title(text: str) -> str:
    """CV-nin başlığını (adətən vəzifə adı) ilk bölmə başlığına qədər götürür."""
    text = normalize_text(text)
    head = SECTION_PATTERN.split(text, maxsplit=1)[0]
    head = normalize_text(NOISE_PATTERN.sub(" ", head))

    if len(head) > 3:
        return head[:TITLE_MAX_CHARS]

    return text[:TITLE_FALLBACK_CHARS]


def body_texts(texts):
    return [normalize_text(t) for t in texts]


def title_texts(texts):
    return [extract_title(t) for t in texts]


class ScaledLinearSVC(LinearSVC):
    """LinearSVC + softmax(decision * temperature) ilə ehtimal.

    CalibratedClassifierCV bu datada ehtimalları "yastılayır" və sıralamanı pozurdu
    (düzgün kateqoriya SVC-də birinci olsa da kalibrasiyadan sonra aşağı düşürdü).
    Burada sıralama SVC ilə eynidir, temperature isə train_model.py-də log-loss ilə seçilir.
    """

    temperature = 5.0

    def predict_proba(self, X):
        scores = self.decision_function(X) * self.temperature
        scores = scores - scores.max(axis=1, keepdims=True)
        exp = np.exp(scores)
        return exp / exp.sum(axis=1, keepdims=True)
