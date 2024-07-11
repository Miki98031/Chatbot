from loaders.default_loader import DefaultLoader
from loaders.pdf_loader import PDFLoader
from loaders.csv_loader import CsvLoader
#from loaders.url_loader import URLLoader
from loaders.word_loader import WordLoader
#from loaders.audio_loader import AudioLoader
from loaders.image_loader import ImageLoader
from loaders.text_loader import TextLoader
from loaders.ppt_loader import PPTLoader

def load(files):
    loaders = {
        'pdf': PDFLoader(),
        'csv': CsvLoader(),
        'docx': WordLoader(),
        'txt': TextLoader(),
        **dict.fromkeys(['ppt', 'pptx'], PPTLoader()),
        #**dict.fromkeys(['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'], AudioLoader()),
        **dict.fromkeys(['jpg', 'jpeg', 'png', 'tiff'], ImageLoader())
    }

    returned_docs = []
    error_files = []
    
    for file in files:
        if file.startswith('http'):
            loader = URLLoader()
        else:
            file_extension = file.split('.')[-1].lower()
            loader = loaders.get(file_extension, DefaultLoader())
        
        try:
            returned_docs += loader.load(file)
        except ValueError as ve:
            print(f'Catched error: {ve}')
            error_files.append(file)
            continue
    
    return returned_docs, error_files