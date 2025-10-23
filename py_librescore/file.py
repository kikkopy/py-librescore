import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .types import FileType

@dataclass
class ScoreFile:
    file_type: FileType
    url: Optional[str] = None
    filename: Optional[str] = None
    data: Optional[bytes] = None
    sha256: Optional[str] = None
    md5: Optional[str] = None
    size: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def set_data(self, data: bytes):
        self.data = data
        self.size = len(data)
        self.sha256 = hashlib.sha256(data).hexdigest()
        self.md5 = hashlib.md5(data).hexdigest()
    
    def save(self, path: Path):
        if self.data is None:
            raise ValueError("No data to save")
        
        with open(path, 'wb') as f:
            f.write(self.data)
    
    def __repr__(self) -> str:
        return (f"ScoreFile(type={self.file_type.value}, "
                f"filename={self.filename}, "
                f"size={self.size}, "
                f"sha256={self.sha256[:16]}...)")