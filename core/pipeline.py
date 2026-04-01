import utils.image

from core.ocr import extract_text
from core.structure import structure_content, normalize_blocks
from core.summarize import (
    summarize_content,
    build_processing_metadata,
    finalize_note,
)
from core.confidence import compute_confidence

from ml.features import extract_advanced_features
from ml.model import predict
from ml.router import route_pipeline

from storage.schema import Note, ProcessingMetadata


# 🔷 Specialized processors

def process_code(text):
    return structure_content(text)


def process_text(text):
    return structure_content(text)


def process_slide(text):
    return structure_content(text)


def process_visual(image):
    return []


def process_hybrid(text):
    return structure_content(text)


# 🔷 Failure handler

def handle_pipeline_failure(error):
    return Note(
        id="",
        title="Processing Error",
        summary=str(error),
        blocks=[],
        created_at="",
        updated_at="",
        type="error",
        tags=[],
        image={},
        metadata=ProcessingMetadata("error", 0, 0, "error"),
    )


# 🔷 MAIN PIPELINE

def run_pipeline(file, user_mode=None):
    try:
        utils.image.validate_image_input(file)

        image = utils.image.load_image(file)
        image = utils.image.preprocess_image(image)

        raw_text, ocr_conf = extract_text(image, "ocr")
        clean_text = utils.image.clean_extracted_text(raw_text)

        # 🔥 Feature extraction
        features = extract_advanced_features(image["file"], clean_text)

        # 🔥 Detection (ML or fallback)
        content_type = predict(features)

        # 🔥 Routing
        pipeline_type = route_pipeline(content_type)

        # 🔥 Execution
        if pipeline_type == "code_pipeline":
            blocks = process_code(clean_text)

        elif pipeline_type == "text_pipeline":
            blocks = process_text(clean_text)

        elif pipeline_type == "summary_pipeline":
            blocks = process_slide(clean_text)

        elif pipeline_type == "visual_pipeline":
            blocks = process_visual(image)

        else:
            blocks = process_hybrid(clean_text)

        blocks = normalize_blocks(blocks)

        note = summarize_content(blocks)

        metadata = build_processing_metadata(
            detected_type=content_type,
            confidence=0.8,
            ocr_conf=ocr_conf,
            mode=pipeline_type,
        )

        note = finalize_note(note, metadata)

        # 🔥 Confidence scoring
        result_dict = {
            "blocks": note.blocks,
            "summary": note.summary,
            "content_type": content_type,
        }

        note.metadata.confidence = compute_confidence(result_dict)

        return note

    except Exception as e:
        return handle_pipeline_failure(e)
