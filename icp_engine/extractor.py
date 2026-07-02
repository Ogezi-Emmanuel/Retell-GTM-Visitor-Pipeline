# extractor.py
import urllib.request
import urllib.error
import socket
from html.parser import HTMLParser
from . import config

class DOMStripper(HTMLParser):
    """Safely tears down an HTML DOM into a raw text payload."""
    def __init__(self):
        super().__init__()
        self.text_data = []
        self.capture = True

    def handle_data(self, data):
        if self.capture and data.strip():
            self.text_data.append(data.strip())

    def handle_starttag(self, tag, attrs):
        # Drop non-semantic noise (scripts, styles, nav bars)
        if tag in ('script', 'style', 'nav', 'footer', 'noscript', 'meta', 'header'):
            self.capture = False

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'footer', 'noscript', 'meta', 'header'):
            self.capture = True

    def get_payload(self):
        return ' '.join(self.text_data)

def fetch_and_clean_url(domain: str, retries: int = config.MAX_RETRIES) -> str:
    """Fetches domain with exponential backoff and edge-case handling."""
    url = f"https://www.{domain}" if not domain.startswith('http') else domain

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=config.HEADERS)
            with urllib.request.urlopen(req, timeout=config.REQUEST_TIMEOUT) as response:
                html = response.read().decode('utf-8', errors='ignore')
                stripper = DOMStripper()
                stripper.feed(html)
                return stripper.get_payload()
                
        except urllib.error.HTTPError as e:
            if e.code in [403, 401]:
                return f"[ERROR] WAF/Bot Blocked ({e.code})"
            return f"[ERROR] HTTP {e.code}"
        except urllib.error.URLError:
            return "[ERROR] DNS/Network Error"
        except socket.timeout:
            if attempt == retries - 1:
                return "[ERROR] Connection Timed Out"
        except Exception as e:
            return f"[ERROR] Unhandled Exception: {str(e)}"
            
    return "[ERROR] Max retries exceeded"