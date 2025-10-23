import requests
from typing import Optional, Dict, Any
from .auth import AuthManager
from .exceptions import AuthenticationException, DownloadException

class MuseScoreAPI:
    BASE_URL = "https://musescore.com"
    API_ENDPOINT = "/api/jmuse"
    
    def __init__(self, session: requests.Session, auth_manager: AuthManager):
        self.session = session
        self.auth = auth_manager
    
    def get_file_url(self, score_id: int, file_type: str, index: int = 0, score_url: str = "") -> Optional[str]:
        api_url = f"{self.BASE_URL}{self.API_ENDPOINT}?id={score_id}&type={file_type}&index={index}"
        
        suffix = None
        if score_url:
            suffix = self.auth.extract_suffix_from_url(score_url)
        
        auth_token = self.auth.get_api_auth(score_id, file_type, index, suffix)
        
        try:
            response = self.session.get(
                api_url,
                headers={'Authorization': auth_token},
                timeout=30
            )
            
            if not response.ok:
                auth_token = self.auth.get_api_auth(score_id, file_type, index, None)
                response = self.session.get(
                    api_url,
                    headers={'Authorization': auth_token},
                    timeout=30
                )
            
            if response.ok:
                data = response.json()
                return data.get('info', {}).get('url')
            
            raise AuthenticationException(f"Failed to authenticate: {response.status_code}")
        
        except requests.RequestException as e:
            raise DownloadException(f"API request failed: {e}")
    
    def download_data(self, url: str) -> bytes:
        try:
            response = self.session.get(url, timeout=60, stream=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise DownloadException(f"Download failed: {e}")