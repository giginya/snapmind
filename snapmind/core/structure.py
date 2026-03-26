from snapmind.storage.schema import Block


def structure_content(text: str):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    blocks = []

    for line in lines:
        if line.isupper():
            t = "heading"
        elif len(line) < 40:
            t = "short"
        else:
            t = "paragraph"

        blocks.append(Block(type=t, content=line))

    return blocks


def normalize_blocks(blocks):
    return [b for b in blocks if b.content.strip()]
