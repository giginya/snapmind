from dataclasses import dataclass, field
from typing import List, Dict
import uuid
import datetime


@dataclass
class Block:
    type: str
    content: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class ProcessingMetadata:
    detected_type: str
    confidence: float
    ocr_confidence: float
    processing_mode: str


@dataclass
class Note:
    id: str
    title: str
    summary: str
    blocks: List[Block]
    created_at: str
    updated_at: str
    type: str
    tags: List[str]
    image: Dict
    metadata: ProcessingMetadata

    @staticmethod
    def create():
        now = str(datetime.datetime.utcnow())

        return Note(
            id=str(uuid.uuid4()),
            title="",
            summary="",
            blocks=[],
            created_at=now,
            updated_at=now,
            type="",
            tags=[],
            image={},
            metadata=None,
        )


@dataclass
class User:
    email: str
    is_verified: bool
    otp: str
    otp_expiry: str
    created_at: str
