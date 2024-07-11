from loaders.file_loader import FileLoader
from langchain.document_loaders import UnstructuredFileLoader

class TextLoader(FileLoader):
    def load(self, file):
        loader = UnstructuredFileLoader(file)
        docs = loader.load_data(file=file)
        return docs