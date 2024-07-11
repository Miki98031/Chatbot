from loaders.file_loader import FileLoader
from langchain.document_loaders import WebBaseLoader
from loaders.audio_loader import AudioLoader
from loaders.image_loader import ImageLoader
from urllib.parse import urlparse
import html

class URLLoader(FileLoader):
    def is_valid_url(self, url):
        ALLOWED_PROTOCOLS = {'http', 'https'}
        try:
            result = urlparse(url)
            return all([result.scheme in ALLOWED_PROTOCOLS, result.netloc])
        except ValueError:
            return False

    def sanitize_url(self, url):
        sanitized_url = html.escape(url)
        return sanitized_url
    
    def load(self, file):
        advanced_loaders = {
            **dict.fromkeys(['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'], AudioLoader()),
            **dict.fromkeys(['jpg', 'jpeg', 'png', 'tiff'], ImageLoader())
        }
        
        if(self.is_valid_url(file) == False):
            raise ValueError('Invalid URL')
    
        url = self.sanitize_url(file)

        file_extension = url.split('.')[-1].lower()
        loader = advanced_loaders.get(file_extension, -1)

        if loader == -1:
            loader = WebBaseLoader(url)
            docs = loader.load()

        else:
            docs = loader.load(url)
        
        return docs
