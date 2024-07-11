from loaders.file_loader import FileLoader
from langchain.document_loaders import Docx2txtLoader

class WordLoader(FileLoader):
    def load(self, file):
        loader = Docx2txtLoader(file_path=file)
        docs = loader.load()
        return docs
        