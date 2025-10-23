import requests
from typing import Optional, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from .api import MuseScoreAPI
from .auth import AuthManager
from .parser import HTMLParser
from .types import ScoreMetadata, FileType
from .file import ScoreFile
from .pdf import PDFGenerator
from .exceptions import ScoreNotFoundException, DownloadException

class ScoreDownloader:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def __init__(self, max_workers: int = 5):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'en-US;q=0.8'
        })
        self.auth_manager = AuthManager(self.session)
        self.api = MuseScoreAPI(self.session, self.auth_manager)
        self.max_workers = max_workers
    
    def fetch_metadata(self, url: str) -> ScoreMetadata:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            html = response.text
            
            metadata = HTMLParser.parse_full_metadata(html)
            
            if metadata.id == 0:
                raise ScoreNotFoundException(f"Score not found at URL: {url}")
            
            return metadata
        except requests.RequestException as e:
            raise DownloadException(f"Failed to fetch metadata: {e}")
    
    def download_midi(self, metadata: ScoreMetadata, score_url: str = "") -> ScoreFile:
        file_url = self.api.get_file_url(metadata.id, 'midi', 0, score_url)
        if not file_url:
            raise DownloadException("Could not get MIDI file URL")
        
        data = self.api.download_data(file_url)
        
        score_file = ScoreFile(
            file_type=FileType.MIDI,
            url=file_url,
            filename=f"{metadata.title}.mid"
        )
        score_file.set_data(data)
        
        return score_file
    
    def download_mp3(self, metadata: ScoreMetadata, score_url: str = "") -> ScoreFile:
        file_url = self.api.get_file_url(metadata.id, 'mp3', 0, score_url)
        if not file_url:
            raise DownloadException("Could not get MP3 file URL")
        
        data = self.api.download_data(file_url)
        
        score_file = ScoreFile(
            file_type=FileType.MP3,
            url=file_url,
            filename=f"{metadata.title}.mp3"
        )
        score_file.set_data(data)
        
        return score_file
    
    def download_pdf(
        self, 
        metadata: ScoreMetadata, 
        score_url: str = "",
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> ScoreFile:
        if metadata.page_count == 0:
            raise DownloadException("Invalid page count")
        
        image_urls = []
        
        for i in range(metadata.page_count):
            if i == 0:
                image_urls.append(metadata.thumbnail_url)
            else:
                img_url = self.api.get_file_url(metadata.id, 'img', i, score_url)
                if img_url:
                    image_urls.append(img_url)
        
        def download_image(url: str) -> bytes:
            return self.api.download_data(url)
        
        image_data_list = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(download_image, url): i for i, url in enumerate(image_urls)}
            
            results = [None] * len(image_urls)
            
            for future in as_completed(future_to_url):
                index = future_to_url[future]
                results[index] = future.result()
                
                if progress_callback:
                    completed = sum(1 for r in results if r is not None)
                    progress_callback(completed, len(image_urls))
        
        image_data_list = results
        
        pdf_data = PDFGenerator.generate_from_images(
            image_data_list,
            metadata.dimensions,
            progress_callback
        )
        
        score_file = ScoreFile(
            file_type=FileType.PDF,
            filename=f"{metadata.title}.pdf"
        )
        score_file.set_data(pdf_data)
        
        return score_file