import hashlib
import re
from typing import Optional

class AuthManager:
    def __init__(self, session):
        self.session = session
        self.suffix_cache: Dict[str, str] = {}
    
    def get_api_auth(self, score_id: int, file_type: str, index: int, suffix: Optional[str] = None) -> str:
        if suffix:
            code = f"{score_id}{file_type}{index}{suffix}"
        else:
            code = f"{score_id}{file_type}{index}%3(3"
        return hashlib.md5(code.encode()).hexdigest()[:4]
    
    def extract_suffix_from_url(self, score_url: str) -> Optional[str]:
        if score_url in self.suffix_cache:
            return self.suffix_cache[score_url]
        
        try:
            response = self.session.get(score_url, timeout=30)
            html = response.text
            
            js_urls = re.findall(
                r'link.+?href=["\'](https://musescore\.com/static/public/build/musescore.*?(?:_es6)?/20.+?\.js)["\']',
                html
            )
            
            for url in js_urls:
                js_response = self.session.get(url, timeout=30)
                js_text = js_response.text
                
                match = re.search(r'"([^"]+)"\)\.substr\(0,4\)', js_text)
                if match:
                    suffix = match.group(1)
                    self.suffix_cache[score_url] = suffix
                    return suffix
        except:
            pass
        
        return None