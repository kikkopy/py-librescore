import re
import hashlib
from pathlib import Path
from typing import Optional

def escape_filename(filename: str) -> str:
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        name_clean = re.sub(r'[\s<>:{}"/\\|?*~\x00-\x1f]+', '_', name)
        return f"{name_clean}.{ext}"
    else:
        return re.sub(r'[\s<>:{}"/\\|?*~.\x00-\x1f]+', '_', filename)

def calculate_hash(data: bytes, algorithm: str = 'sha256') -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()

def validate_url(url: str) -> bool:
    pattern = re.compile(r'^(?:https?://)?(?:(?:s|www)\.)?musescore\.com/[^\s]+$')
    return bool(pattern.match(url))

def normalize_url(url: str) -> str:
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path