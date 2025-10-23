from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
from .types import FileType, ScoreMetadata
from .file import ScoreFile
from .downloader import ScoreDownloader
from .utils import normalize_url, validate_url, escape_filename, ensure_dir
from .exceptions import LibreScoreException

class Score:
    def __init__(self, metadata: ScoreMetadata, downloader: ScoreDownloader, url: str):
        self.metadata = metadata
        self._downloader = downloader
        self.url = url
        self._files: Dict[FileType, ScoreFile] = {}
    
    @property
    def id(self) -> int:
        return self.metadata.id
    
    @property
    def title(self) -> str:
        return self.metadata.title
    
    @property
    def page_count(self) -> int:
        return self.metadata.page_count
    
    @property
    def is_official(self) -> bool:
        return self.metadata.is_official
    
    def download(
        self, 
        file_type: FileType,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> ScoreFile:
        if file_type in self._files:
            return self._files[file_type]
        
        if file_type == FileType.MIDI:
            score_file = self._downloader.download_midi(self.metadata, self.url)
        elif file_type == FileType.MP3:
            score_file = self._downloader.download_mp3(self.metadata, self.url)
        elif file_type == FileType.PDF:
            score_file = self._downloader.download_pdf(self.metadata, self.url, progress_callback)
        else:
            raise LibreScoreException(f"Unsupported file type: {file_type}")
        
        self._files[file_type] = score_file
        return score_file
    
    def download_all(
        self,
        file_types: Optional[List[FileType]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[FileType, ScoreFile]:
        if file_types is None:
            file_types = [FileType.PDF, FileType.MIDI, FileType.MP3]
        
        results = {}
        for ft in file_types:
            try:
                results[ft] = self.download(ft, progress_callback)
            except Exception as e:
                print(f"Failed to download {ft.value}: {e}")
        
        return results
    
    def save(self, file_type: FileType, output_dir: Path):
        if file_type not in self._files:
            raise LibreScoreException(f"File type {file_type.value} not downloaded yet")
        
        score_file = self._files[file_type]
        ensure_dir(output_dir)
        
        if score_file.filename and '.' in score_file.filename:
            filename = escape_filename(score_file.filename)
        else:
            base_name = escape_filename(score_file.filename or f"{self.title}_{file_type.value}")
            extension = file_type.value
            filename = f"{base_name}.{extension}"
        
        filepath = output_dir / filename
        score_file.save(filepath)
        
        return filepath
    
    def __repr__(self) -> str:
        return f"Score(id={self.id}, title='{self.title}', pages={self.page_count})"

class MuseScore:
    def __init__(self, max_workers: int = 5):
        self._downloader = ScoreDownloader(max_workers=max_workers)
    
    def get_score(self, url: str) -> Score:
        normalized_url = normalize_url(url)
        
        if not validate_url(normalized_url):
            raise LibreScoreException(f"Invalid MuseScore URL: {url}")
        
        metadata = self._downloader.fetch_metadata(normalized_url)
        
        return Score(metadata, self._downloader, normalized_url)