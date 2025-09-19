import re

KEYWORDS_A = ['risk', 'safety', 'regulate', 'predictable', 'clinical', 'testing', 'harm']
KEYWORDS_B = ['freedom', 'autonomy', 'progress', 'creativity', 'philosophy', 'choice']

def sanitize_text(s: str) -> str:
    return re.sub(r'\s+', ' ', s.strip())

def score_argument(text: str) -> dict:
    """Return a simple keyword-based score for argument polarity."""
    t = text.lower()
    a = sum(t.count(k) for k in KEYWORDS_A)
    b = sum(t.count(k) for k in KEYWORDS_B)
    return {'safety_score': a, 'freedom_score': b}
