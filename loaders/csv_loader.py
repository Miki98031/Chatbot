from loaders.file_loader import FileLoader
from langchain.document_loaders import CSVLoader

class CsvLoader(FileLoader):
    def load(self, file):
        loader = CSVLoader(file_path=file, encoding='utf-8')
        docs = loader.load()
        return docs
