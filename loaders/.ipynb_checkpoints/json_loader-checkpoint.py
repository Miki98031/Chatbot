from loaders.file_loader import FileLoader
from langchain.document_loaders import JSONLoader

class CsvLoader(FileLoader):
    def load(self, file):
        loader = JSONLoader(file_path=file)
        docs = loader.load()
        return docs
