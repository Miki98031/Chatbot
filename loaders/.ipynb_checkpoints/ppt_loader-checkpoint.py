from loaders.file_loader import FileLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

class PPTLoader(FileLoader):
    def load(self, file):
        loader = UnstructuredPowerPointLoader(file)
        docs = loader.load()
        return docs