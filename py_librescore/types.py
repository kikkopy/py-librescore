from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class FileType(Enum):
    PDF = "pdf"
    MIDI = "midi"
    MP3 = "mp3"
    MSCZ = "mscz"
    MSCX = "mscx"
    MUSICXML = "musicxml"

@dataclass
class Dimensions:
    width: int
    height: int

@dataclass
class ScoreMetadata:
    id: int
    title: str
    subtitle: Optional[str]
    composer: Optional[str]
    arranger: Optional[str]
    copyright: Optional[str]
    page_count: int
    duration: Optional[int]
    view_count: Optional[int]
    is_official: bool
    has_custom_audio: bool
    base_url: str
    thumbnail_url: str
    dimensions: Dimensions
    img_type: str