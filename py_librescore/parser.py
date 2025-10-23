import re
from typing import Optional, Dict, Any
from .types import ScoreMetadata, Dimensions

class HTMLParser:
    @staticmethod
    def extract_score_id(html: str) -> Optional[int]:
        match = re.search(r'<meta property="al:ios:url" content="musescore://score/(\d+)">', html)
        return int(match.group(1)) if match else None
    
    @staticmethod
    def extract_title(html: str) -> Optional[str]:
        match = re.search(r'<meta property="og:title" content="(.*?)">', html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_base_url(html: str) -> Optional[str]:
        match = re.search(r'<meta property="og:image" content="(.+/)score_.*?">', html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_page_count(html: str) -> int:
        match = re.search(r'pages(?:&quot;|"):(\d+)', html)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def extract_thumbnail_url(html: str) -> Optional[str]:
        match = re.search(r'<link[^>]*?href="([^"]+)"[^>]*?rel="preload"[^>]*?as="image"', html)
        return match.group(1).split('@')[0] if match else None
    
    @staticmethod
    def extract_dimensions(html: str) -> Dimensions:
        match = re.search(r'dimensions(?:&quot;|"):(?:&quot;|")(\d+)x(\d+)(?:&quot;|")', html)
        if match:
            return Dimensions(width=int(match.group(1)), height=int(match.group(2)))
        return Dimensions(width=0, height=0)
    
    @staticmethod
    def is_official_score(html: str) -> bool:
        return bool(
            re.search(r'<meta property="musescore:author" content="Official Scores">', html) or
            re.search(r'<meta property="musescore:author" content="Official Author">', html)
        )
    
    @staticmethod
    def extract_composer(html: str) -> Optional[str]:
        match = re.search(r'<meta property="musescore:composer" content="(.*?)">', html)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_suffix(js_content: str) -> Optional[str]:
        match = re.search(r'"([^"]+)"\)\.substr\(0,4\)', js_content)
        return match.group(1) if match else None

    @staticmethod
    def parse_full_metadata(html: str) -> ScoreMetadata:
        score_id = HTMLParser.extract_score_id(html)
        title = HTMLParser.extract_title(html)
        base_url = HTMLParser.extract_base_url(html)
        page_count = HTMLParser.extract_page_count(html)
        thumbnail_url = HTMLParser.extract_thumbnail_url(html)
        dimensions = HTMLParser.extract_dimensions(html)
        is_official = HTMLParser.is_official_score(html)
        composer = HTMLParser.extract_composer(html)
        
        img_type = 'svg' if thumbnail_url and '.svg' in thumbnail_url else 'png'
        
        return ScoreMetadata(
            id=score_id or 0,
            title=title or f"score_{score_id}",
            subtitle=None,
            composer=composer,
            arranger=None,
            copyright=None,
            page_count=page_count,
            duration=None,
            view_count=None,
            is_official=is_official,
            has_custom_audio=False,
            base_url=base_url or "",
            thumbnail_url=thumbnail_url or "",
            dimensions=dimensions,
            img_type=img_type
        )