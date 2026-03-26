# snapmind/core/confidence.py

def compute_confidence(result: dict):
    score = 0.0

    text_len = len(result.get("summary", ""))
    blocks = result.get("blocks", [])

    # signal 1: structure richness
    if len(blocks) > 3:
        score += 0.25

    # signal 2: summary strength
    if text_len > 100:
        score += 0.25

    # signal 3: block consistency
    types = set([b.type for b in blocks])
    if len(types) <= 3:
        score += 0.2

    # signal 4: content type confidence proxy
    if result.get("content_type") in ["document", "code"]:
        score += 0.2

    return max(0.0, min(score, 1.0))
